#ifndef GSI_DEVICE_LAB_3_H
#define GSI_DEVICE_LAB_3_H

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#include <stdint.h>

enum {
	GD_LAB_3_MAX_NUM_RECORDS_IN_DB = 32 * 1024,
	GD_LAB_3_MAX_NUM_FEATURES = 48,
};

enum gd_lab_3_cmd_type {
	GD_CMD_LOAD_SVM,
	GD_CLASSIFY_TESTDATA,
	GD_LAB_3_NUM_CMDS
};

static inline uint64_t gd_lab_3_get_preprocessed_db_size(uint32_t num_features)
{//here max number of support vectors is 32,768
	return sizeof(uint16_t) * num_features * GD_LAB_3_MAX_NUM_RECORDS_IN_DB;
}

static inline void gd_lab_3_preprocess_db(uint16_t dst_f16[], const uint16_t src_f16[], uint32_t num_features, uint32_t num_records)
{
	for (uint32_t f = 0; f < num_features; ++f) {
		for (uint32_t r = 0; r < num_records; ++r) {
			dst_f16[GD_LAB_3_MAX_NUM_RECORDS_IN_DB * f + r] = src_f16[r * num_features + f];
		}
		/* For valgrind */
		//fill the rest with 0s
		for (uint32_t r = num_records; r < GD_LAB_3_MAX_NUM_RECORDS_IN_DB; ++r) {
			dst_f16[GD_LAB_3_MAX_NUM_RECORDS_IN_DB * f + r] = 0;
		}
	}
}

struct gd_lab_3_idx_val {
	uint16_t idx;
	uint16_t val;
} __attribute__((packed));

struct gd_load_SVM {
	uint64_t supportVectors;		/* gdl_mem_handle_t(host) / gal_mem_handle_t(dev) */
	uint64_t weights;
	uint32_t gamma;
	uint32_t intercept;
	uint32_t num_features;
	uint32_t num_support_vectors;
} __attribute__((packed));

struct gd_classify_testData {
	uint64_t classification;	/* gdl_mem_handle_t(host) / gal_mem_handle_t(dev) */
	uint64_t testData;	/* gdl_mem_handle_t(host) / gal_mem_handle_t(dev) */
	uint32_t num_testData;
} __attribute__((packed));

struct gd_lab_3_cmd {
	uint32_t cmd;
	int32_t  pad_for_64bit_alignment;
	union 	{
		struct gd_load_SVM	load_SVM_data;
		struct gd_classify_testData	classify_data;
	} __attribute__((packed));
} __attribute__((packed));

#ifdef __cplusplus
}
#endif /* __cplusplus */

#endif /* GSI_DEVICE_LAB_3_H */
