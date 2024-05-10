#include <gsi/libsys/assert.h>
#include <gsi/libsys.h>
#include <gsi/libgal.h>
#include <gsi/gal-fast-funcs.h>
#include <gsi/libgvml_memory.h>

#include <gsi/libgvml_iv.h>
#include <gsi/libgvml_element_wise.h>
#include <gsi/libgvml_min_max.h>
#include <gsi/libgvml_get_marked_data.h>
#include <gsi/libgvml_debug.h>

#include "gsi_device_lab_3.h"
#include "gsi_device_lab_3_dma.h"

static struct {
	uint32_t num_support_vectors;
	uint32_t num_features;
	enum gvml_vr16 vr_weights;
	enum gvml_vr16 vr_gamma;
	enum gvml_vr16 vr_intercept;
} g_SVM_data = {
	.num_support_vectors = 0,
	.num_features = 0
};

static int load_SVM(struct gd_load_SVM *load_SVM_data)
{
	if (load_SVM_data->num_features > GD_LAB_3_MAX_NUM_FEATURES) {
		gsi_error("number of features (%u) must not exceed %d", (unsigned )load_SVM_data->num_features, GD_LAB_3_MAX_NUM_FEATURES);
		return gsi_status(EINVAL);
	}

	if (load_SVM_data->num_support_vectors > GD_LAB_3_MAX_NUM_RECORDS_IN_DB) {
		gsi_error("number of records (%u) must not exceed %d", (unsigned )load_SVM_data->num_support_vectors, GD_LAB_3_MAX_NUM_RECORDS_IN_DB);
		return gsi_status(EINVAL);
	}

	g_SVM_data.num_features = load_SVM_data->num_features;
	g_SVM_data.num_support_vectors = load_SVM_data->num_support_vectors;

	uint16_t *ptr_in = gal_mem_handle_to_apu_ptr(load_SVM_data->supportVectors);
	const uint16_t *weights = gal_mem_handle_to_apu_ptr(load_SVM_data->weights);
	enum gvml_vr16 vr_intercept = GVML_VR16_4;
	enum gvml_vr16 vr_weights = GVML_VR16_5;
	enum gvml_vr16 vr_gamma = GVML_VR16_6;
	enum gvml_mrks_n_flgs marker = GVML_MRK1;
	enum gvml_vr16 vr_idx;

	g_SVM_data.vr_weights = vr_weights;
	g_SVM_data.vr_gamma = vr_gamma;
	g_SVM_data.vr_intercept = vr_intercept;

	gal_set_l2dma_dma_mode(GAL_L2DMA_MODE_DIRECT);

	//put the weight values into a vr
	gvml_cpy_imm_16(vr_weights,0);
	gal_set_l2dma_dma_mode(GAL_L2DMA_MODE_DIRECT);
    direct_dma_l4_to_l1_32k(GVML_VM_1, weights);
	gvml_load_16(vr_weights, GVML_VM_1);
	//use this marker vr to make all entries except for zeroNumber spaces
	//from the head of the vr 0 beacuse some of them are not going to be after
	//during the SVM calculation
	gvml_create_index_16(vr_idx);
	//alright here lt means indexes less than some number will be marked in the VR EXTREMELY HELPFUL!!
	gvml_lt_imm_u16(marker, vr_idx, (uint16_t)load_SVM_data->num_support_vectors);
	gvml_not_m(marker,marker);
	gvml_cpy_imm_16_mrk(vr_weights, 0, marker);
	//put the gamma and intercept
	gvml_cpy_imm_16(vr_gamma, load_SVM_data->gamma);
	gvml_cpy_imm_16(vr_intercept, load_SVM_data->intercept);
	
	//take each feature and store into VMR (L1) parts (only a max of 48 here)
	for (uint32_t f = 0; f < load_SVM_data->num_features; ++f) {
		direct_dma_l4_to_l1_32k(f, &ptr_in[f * GD_LAB_3_MAX_NUM_RECORDS_IN_DB]);
	}

	return 0;
}

static int do_classification(struct gd_classify_testData *classify_data)
{
	enum gvml_vr16 vr_distances = GVML_VR16_1;
	enum gvml_vr16 vr_supportVectors = GVML_VR16_2;
	enum gvml_vr16 vr_testData = GVML_VR16_3;
	enum gvml_vr16 vr_intercept = g_SVM_data.vr_intercept;
	enum gvml_vr16 vr_weights = g_SVM_data.vr_weights;
	enum gvml_vr16 vr_gamma = g_SVM_data.vr_gamma;
	enum gvml_vr16 vr_temp = GVML_VR16_7;

	const uint16_t *testInputs = gal_mem_handle_to_apu_ptr(classify_data->testData);
	//gsi_info("gal_mem_handle size: %i, location pointer %x",sizeof(testInputs),testInputs);
	uint16_t *outputValues = gal_mem_handle_to_apu_ptr(classify_data->classification);
	uint32_t shiftNumber = 1;
	uint32_t shiftNumberChange = 0;
	uint32_t verdict = g_SVM_data.num_support_vectors;
	uint16_t a = 0;
	uint16_t b = 0;

	//get this value for determining log add
	while(verdict){
		verdict>>=1;
		shiftNumber*=2;
	}
	shiftNumber>>=3;
	
	//start code
	for (uint32_t q = 0; q < classify_data->num_testData; ++q, testInputs += g_SVM_data.num_features) {
		gvml_reset_16(vr_distances);
		gvml_reset_16(vr_temp);
		for (uint32_t f = 0; f < g_SVM_data.num_features; ++f) {
			//copy one value into all spots
			gvml_cpy_imm_16(vr_testData, testInputs[f]);
			//get vmr data and put into supportVectors vr
			gvml_load_16(vr_supportVectors, f);
			//get difference in points
			gvml_sub_f16(vr_supportVectors, vr_supportVectors, vr_testData);
			//square term
			gvml_mul_f16(vr_supportVectors, vr_supportVectors, vr_supportVectors);
			//add value to distance
			gvml_add_f16(vr_distances, vr_distances, vr_supportVectors);
		}

			
		//mult by gamma
		gvml_mul_f16(vr_distances, vr_distances, vr_gamma);
		//exponential
		gvml_exp_f16(vr_distances, vr_distances);
		//multiply by weights
		gvml_mul_f16(vr_distances, vr_distances, vr_weights);

		//now log sum the vr
		shiftNumberChange = 512;
		while(shiftNumberChange){
			//gvml_shift_head_imm_16_m1_g32k(vr_temp, vr_distances, shiftNumberChange);
			gvml_shift_head_imm_16_m1_g2k(vr_temp, vr_distances, shiftNumberChange);
			gvml_add_f16(vr_distances, vr_distances, vr_temp);
			shiftNumberChange>>=1;
		}
		
		
		//now need to add the last 4 values
		a = gvml_get_entry_16(vr_distances, 4096);
		b = gvml_get_entry_16(vr_distances, 4097);
		gvml_set_entry_16(vr_distances, 4, a);
		gvml_set_entry_16(vr_distances, 5, b);
		a = gvml_get_entry_16(vr_distances, 4098);
                b = gvml_get_entry_16(vr_distances, 4099);
                gvml_set_entry_16(vr_distances, 6, a);
                gvml_set_entry_16(vr_distances, 7, b);

		a = gvml_get_entry_16(vr_distances, 8192);
                b = gvml_get_entry_16(vr_distances, 8193);
                gvml_set_entry_16(vr_distances, 8, a);
                gvml_set_entry_16(vr_distances, 9, b);
                a = gvml_get_entry_16(vr_distances, 8194);
                b = gvml_get_entry_16(vr_distances, 8195);
                gvml_set_entry_16(vr_temp, 0, a);
                gvml_set_entry_16(vr_temp, 1, b);

		a = gvml_get_entry_16(vr_distances, 12288);
                b = gvml_get_entry_16(vr_distances, 12289);
                gvml_set_entry_16(vr_temp, 2, a);
                gvml_set_entry_16(vr_temp, 3, b);
                a = gvml_get_entry_16(vr_distances, 12290);
                b = gvml_get_entry_16(vr_distances, 12291);
                gvml_set_entry_16(vr_temp, 4, a);
                gvml_set_entry_16(vr_temp, 5, b);

		a = gvml_get_entry_16(vr_distances, 16384);
                b = gvml_get_entry_16(vr_distances, 16385);
                gvml_set_entry_16(vr_temp, 6, a);
                gvml_set_entry_16(vr_temp, 7, b);
                a = gvml_get_entry_16(vr_distances, 16386);
                b = gvml_get_entry_16(vr_distances, 16387);
                gvml_set_entry_16(vr_temp, 8, a);
                gvml_set_entry_16(vr_temp, 9, b);


		gvml_add_f16(vr_distances,vr_distances,vr_temp);

		a = gvml_get_entry_16(vr_distances, 5);
                b = gvml_get_entry_16(vr_distances, 6);
                gvml_set_entry_16(vr_temp, 0, a);
                gvml_set_entry_16(vr_temp, 1, b);
                a = gvml_get_entry_16(vr_distances, 7);
                b = gvml_get_entry_16(vr_distances, 8);
                gvml_set_entry_16(vr_temp, 2, a);
                gvml_set_entry_16(vr_temp, 3, b);
		a = gvml_get_entry_16(vr_distances, 9);
		gvml_set_entry_16(vr_temp, 4, a);

		gvml_add_f16(vr_distances, vr_distances, vr_temp);


		a = gvml_get_entry_16(vr_distances, 3);
                b = gvml_get_entry_16(vr_distances, 4);
                gvml_set_entry_16(vr_temp, 0, a);
                gvml_set_entry_16(vr_temp, 1, b);
		gvml_set_entry_16(vr_temp, 2, 0);

                gvml_add_f16(vr_distances, vr_distances, vr_temp);


		a = gvml_get_entry_16(vr_distances, 2);
                gvml_set_entry_16(vr_temp, 0, a);
		gvml_set_entry_16(vr_temp, 1, 0);

                gvml_add_f16(vr_distances, vr_distances, vr_temp);


		a = gvml_get_entry_16(vr_distances, 1);
                gvml_set_entry_16(vr_temp, 0, a);

                gvml_add_f16(vr_distances, vr_distances, vr_temp);

		//add the intercept
		gvml_add_f16(vr_distances, vr_distances, vr_intercept);


		//last value in first position
		verdict = gvml_get_entry_16(vr_distances, 0);

		//determine class
		//if negative, class 0
		if(verdict & 0x8000){
			//*(outputValues+q) = 0;
			*(outputValues+q) = verdict;
		}
		else{
			//*(outputValues+q) = 1;
			*(outputValues+q) = verdict;
		}
	}
	return 0;
}
/*
if(q==2){
	gvml_get_16_32k(outputValues,vr_distances);
	return 0;
}
*/

GAL_TASK_ENTRY_POINT(gd_lab_3, in, out)
{
	struct gd_lab_3_cmd *cmd = (struct gd_lab_3_cmd *)in;
	int ret;

	switch (cmd->cmd) {
	case GD_CMD_LOAD_SVM:
		gvml_init_once();
		ret = load_SVM(&cmd->load_SVM_data);
		break;
	case GD_CLASSIFY_TESTDATA:
		ret = do_classification(&cmd->classify_data);
		break;
	default:
		gsi_fatal("%s: unknown command %d\n", __func__, (int )cmd->cmd); /* aborts execution */
		break;
	}

	return ret;
}
