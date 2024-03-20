#include <gsi/libsys/assert.h>
#include <gsi/libsys.h>
#include <gsi/libgal.h>
#include <gsi/gal-fast-funcs.h>
#include <gsi/libgvml_memory.h>

#include <gsi/libgvml_iv.h>              /* gvml_create_index_16() */
#include <gsi/libgvml_element_wise.h>    /* gvml_add_f16() */
#include <gsi/libgvml_min_max.h>         /* gvml_mark_kmin_idxval_u16_mrk_g32k() */
#include <gsi/libgvml_get_marked_data.h> /* gvml_get_marked_data_xv() */
#include <gsi/libgvml_debug.h>

#include "gsi_device_lab_3.h"
#include "gsi_device_lab_3_dma.h"

static struct {
	uint32_t num_support_vectors;
	uint32_t num_features;
} g_SVM_data = {
	.num_support_vectors = 0,
	.num_features = 0,
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
	//exempt for now
	//gvml_lt_imm_u16(g_db_data.mrk_num_records, g_db_data.vr_idx, (uint16_t)g_db_data.num_records);

	uint16_t *ptr_in = gal_mem_handle_to_apu_ptr(load_SVM_data->supportVectors);

	gal_set_l2dma_dma_mode(GAL_L2DMA_MODE_DIRECT);

	//take each feature and store into VMR (L1) parts (only a max of 48 here)
	for (uint32_t f = 0; f < load_SVM_data->num_features; ++f) {
		direct_dma_l4_to_l1_32k(f, &ptr_in[f * GD_LAB_3_MAX_NUM_RECORDS_IN_DB]);
	}

	return 0;
}

static int do_classification(struct gd_classify_testData *classify_data)
{
	//Concerns:
	// 1. is setting the GAL_L2DMA_MODE_DIRECT will mess things up
	// 2. 
	enum gvml_vr16 vr_distances = GVML_VR16_1;
	enum gvml_vr16 vr_supportVectors = GVML_VR16_2;
	enum gvml_vr16 vr_testData = GVML_VR16_3;
	enum gvml_vr16 vr_intercept = GVML_VR16_4;
	enum gvml_vr16 vr_weights = GVML_VR16_5;
	enum gvml_vr16 vr_gamma = GVML_VR16_6;
	enum gvml_vr16 vr_ones = GVML_VR16_7;
	enum gvml_vr16 vr_temp = GVML_VR16_8;

	const uint16_t *testInputs = gal_mem_handle_to_apu_ptr(classify_data->testData);
	const uint16_t *weights = gal_mem_handle_to_apu_ptr(classify_data->weights);
	uint16_t *outputValues = gal_mem_handle_to_apu_ptr(classify_data->classification);
	uint32_t shiftNumber = (g_SVM_data.num_support_vectors%4)?((uint32_t)(g_SVM_data.num_support_vectors/4)):((g_SVM_data.num_support_vectors/4)-1);
	uint16_t verdict = 0;

	gal_set_l2dma_dma_mode(GAL_L2DMA_MODE_DIRECT);
    direct_dma_l4_to_l1_32k(GVML_VM_47, weights);
	gvml_load_16(vr_weights, GVML_VM_47);

	//before calc
	gvml_cpy_imm_16(vr_gamma, classify_data->gamma);
	gvml_cpy_imm_16(vr_intercept, classify_data->intercept);
	gvml_cpy_imm_16(vr_ones, 1);
	//put the weights into the vr...


	for (uint32_t q = 0; q < classify_data->num_testData; ++q, testInputs += g_SVM_data.num_features) {
		gvml_reset_16(vr_distances);
		for (uint32_t f = 0; f < g_SVM_data.num_features; ++f) {
			//copy one value into all spots
			gvml_cpy_imm_16(vr_testData, testInputs[f]);
			//i think this is load values from a numbered VMR into vr
			//*(outputValues) = testInputs[f];
			gvml_load_16(vr_supportVectors, f);
			//*(outputValues) = gvml_get_entry_16(vr_supportVectors, 0);
			//get difference in points
			gvml_sub_gf16(vr_supportVectors, vr_supportVectors, vr_testData);
			//*(outputValues) = gvml_get_entry_16(vr_supportVectors, 0);
			//square term
			gvml_mul_gf16(vr_supportVectors, vr_supportVectors, vr_supportVectors);
			*(outputValues) = gvml_get_entry_16(vr_supportVectors, 0);
			//add value to distance
			gvml_add_gf16(vr_distances, vr_distances, vr_supportVectors);
			//*(outputValues) = gvml_get_entry_16(vr_supportVectors, 0);
			if(f==0){
				return 0;
			}
		}
		//*(outputValues) = gvml_get_entry_16(vr_distances, 0);
		return 0;
		//TESTING PURPOSES ONLY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		/*
		for(uint32_t i = 0; i < g_SVM_data.num_support_vectors; i++){
			*(outputValues+i) = gvml_get_entry_16(vr_distances, i);
		}
		return 0;
		*/
		//TESTING PURPOSES ONLY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		//mult by gamma
		gvml_mul_gf16(vr_distances, vr_distances, vr_gamma);
		//now do sudo exponential (1/(x+1))
		//there is the function gvml_exp_f16() -> but for regular float
		//consider this later
		gvml_add_gf16(vr_distances, vr_distances, vr_ones);
		gvml_reciprocal_gf16(vr_distances, vr_distances);
		//multiply by weights
		gvml_mul_gf16(vr_distances, vr_distances, vr_weights);
		
		//now summ the vr
		for(uint32_t i = 0; i < shiftNumber; i++){
			//shifts by 4 positions
			gvml_shift_head_imm_16_m1_g32k(vr_temp, vr_distances, shiftNumber);
			gvml_add_gf16(vr_distances, vr_distances, vr_temp);
		}
		//now need to add the last 4 values
		gvml_shift_head_imm_16_grp(vr_testData, vr_distances, 2, 2, vr_temp);
		gvml_add_gf16(vr_testData, vr_distances, vr_testData);
		gvml_shift_head_imm_16_grp(vr_distances, vr_testData, 1, 1, vr_temp);
		gvml_add_gf16(vr_distances, vr_distances, vr_testData);
		gvml_add_gf16(vr_distances, vr_distances, vr_intercept);
		//last value in first position
		verdict = gvml_get_entry_16(vr_distances, 0);

		//determine class
		//if negative, class 0
		if(verdict & 0x8000){
			*(outputValues+q) = 0;
		}
		else{
			*(outputValues+q) = 1;
		}
		
	}

	return 0;
}


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
