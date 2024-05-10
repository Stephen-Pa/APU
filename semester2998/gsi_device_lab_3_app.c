#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <stdlib.h>

#include <gsi/libgdl.h>
#include <gsi/libsys.h>
#include <refgvml.h>
#include <refgvml_element_wise.h>

#include <gsi/gsi_sim_config.h>

GDL_TASK_DECLARE(gd_lab_3);
#include "gsi_device_lab_3.h"

static struct {
	struct timespec startDataTransferDevice;
	struct timespec stopDataTransferDevice;
	struct timespec startClassificationDevice;
	struct timespec stopClassificationDevice;
} APU_Timing;

//GO THROUGH ALL OF THIS AND FREE MEMEORY ACCORDINGLY
static int load_SVM(
	//here are the arguments
	gdl_context_handle_t ctx_id,
	uint16_t supportVectors[],
	uint16_t weights[],
	uint32_t gamma,
	uint32_t intercept,
	uint32_t num_supportVectors,
	uint32_t num_features)
{
	int ret;
	gdl_mem_handle_t dev_cmd_buf = GDL_MEM_HANDLE_NULL, dev_supportVector_buf = GDL_MEM_HANDLE_NULL;
	uint16_t *pre_processed_SVM = NULL;
	uint64_t pre_processed_SVM_size = gd_lab_3_get_preprocessed_db_size(num_features);
	uint64_t weight_size = gd_lab_3_get_preprocessed_db_size(1);
	uint64_t total_size = weight_size + pre_processed_SVM_size;

	pre_processed_SVM = malloc(pre_processed_SVM_size);
	if (NULL == pre_processed_SVM) {
		gsi_error("malloc() failed to allocate %lu bytes", pre_processed_SVM_size);
		ret = gsi_status(ENOMEM);
		goto CLEAN_UP;
	}

	gd_lab_3_preprocess_db(pre_processed_SVM, supportVectors, num_features, num_supportVectors);

	dev_supportVector_buf = gdl_mem_alloc_aligned(ctx_id, total_size, GDL_CONST_MAPPED_POOL, GDL_ALIGN_32);
	if (gdl_mem_handle_is_null(dev_supportVector_buf)) {
		gsi_error("gdl_mem_alloc() failed to allocate %lu bytes", pre_processed_SVM_size);
		ret = gsi_status(ENOMEM);
		goto CLEAN_UP;
	}

	ret = gdl_mem_cpy_to_dev(dev_supportVector_buf, pre_processed_SVM, pre_processed_SVM_size);
	if (ret) {
		gsi_error("gdl_mem_cpy_to_dev() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}

	struct gd_lab_3_cmd cmd = {
		.cmd = GD_CMD_LOAD_SVM,
		.load_SVM_data = {
			.supportVectors = dev_supportVector_buf,
			.gamma = gamma,
			.intercept = intercept,
			.num_support_vectors = num_supportVectors,
			.num_features = num_features
		}
	};


	//get memory handle for weights and copy weights to it
	ret = gdl_add_to_mem_handle(&cmd.load_SVM_data.weights, cmd.load_SVM_data.supportVectors, pre_processed_SVM_size);
	if (ret) {
		gsi_error("gdl_add_to_mem_handle() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}

	ret = gdl_mem_cpy_to_dev(cmd.load_SVM_data.weights, weights, weight_size);
	if (ret) {
		gsi_error("gdl_mem_cpy_to_dev() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}

	uint64_t cmd_buf_size = sizeof(cmd);
	dev_cmd_buf = gdl_mem_alloc_aligned(ctx_id, cmd_buf_size, GDL_CONST_MAPPED_POOL, GDL_ALIGN_32);
	if (gdl_mem_handle_is_null(dev_cmd_buf)) {
		gsi_error("gdl_mem_alloc() failed to allocate %lu bytes", cmd_buf_size);
		ret = gsi_status(ENOMEM);
		goto CLEAN_UP;
	}

	ret = gdl_mem_cpy_to_dev(dev_cmd_buf, &cmd, cmd_buf_size);
	if (ret) {
		gsi_error("gdl_mem_cpy_to_dev() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}
	clock_gettime(CLOCK_REALTIME, &APU_Timing.startDataTransferDevice);
	ret = gdl_run_task_timeout(
			ctx_id,              /* @ctx_handler - the id of a hardware context previously allocated */
			GDL_TASK(gd_lab_3),  /* @code_offset - the code offset of the function that the task should execute */
			dev_cmd_buf,         /* @inp - input memory handle */
			GDL_MEM_HANDLE_NULL, /* @outp - output memory handle */
			GDL_TEMPORARY_DEFAULT_MEM_BUF,      /* @mem_buf - an array of previously allocated memory handles and their sizes */
			GDL_TEMPORARY_DEFAULT_MEM_BUF_SIZE, /* @buf_size - the length of the mem_buf array */
			GDL_TEMPORARY_DEFAULT_CORE_INDEX,   /* @apuc_idx - the apuc that the task should be executed on */
			NULL,              /* @comp - if task was successfully scheduled, and @comp is provided, the task completion status, or any error is returned in comp. */
			0,                 /* @ms_timeout - the time in mili-seconds a task should wait for completion before aborting (0 indicates waiting indefinitely) */
			GDL_USER_MAPPING); /* @map_type - determine the mapping type for the specific task */
	clock_gettime(CLOCK_REALTIME, &APU_Timing.stopDataTransferDevice);

	if (ret) {
		gsi_error("gdl_run_task_timeout() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}

CLEAN_UP:
	gdl_mem_free(dev_cmd_buf);
	gdl_mem_free(dev_supportVector_buf);
	free(pre_processed_SVM);

	return ret;
}

static float convertFloat16Back(int a){
    int fraction = a & 0x3ff;
    int exponent = (a&0x7c00)>>10;
    int sign = (a&0x8000)<<16;
    float* ptr = NULL;
    exponent = (exponent - 15) +127;
    fraction = (sign | (exponent<<23) | (fraction<<13));
    ptr = (float*)&fraction;
    return *ptr;
}

static int do_classification(
	gdl_context_handle_t ctx_id,
	uint16_t classVector[],
	uint16_t testData[],
	uint32_t num_testData,
	uint32_t num_features,
	uint32_t num_supportVectors)
{
	int ret;
	gdl_mem_handle_t dev_cmd_buf = GDL_MEM_HANDLE_NULL, io_dev_bufs = GDL_MEM_HANDLE_NULL;
	
	uint64_t testData_size = sizeof(*testData) * num_testData * num_features;
	//the only reason this is multiplied by 2 is because there is a weird error on the APU
	//when feeding in more than 6500 testData points with the Gamma dataset
	uint64_t output_size = sizeof(*classVector)* num_testData;

	uint64_t io_dev_buf_size = testData_size + output_size;
	
	//allocate all the memory you will need for all input and output you have
	//in this case, need space for testData and output
	io_dev_bufs = gdl_mem_alloc_aligned(ctx_id, io_dev_buf_size, GDL_CONST_MAPPED_POOL, GDL_ALIGN_32);
	if (gdl_mem_handle_is_null(io_dev_bufs)) {
		gsi_error("gdl_mem_alloc() failed to allocate %lu bytes", io_dev_buf_size);
		ret = gsi_status(ENOMEM);
		goto CLEAN_UP;
	}

	//use the start pointer for io_dev_buf and consider as start point for testData
	//with this, copy in testData into the buffer up to the size of the test data
	ret = gdl_mem_cpy_to_dev(io_dev_bufs, testData, testData_size);
	if (ret) {
		gsi_error("gdl_mem_cpy_to_dev() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}

	//here, we are assigning the beinging pointer of io_dev_buf to testData
	struct gd_lab_3_cmd cmd = {
		.cmd = GD_CLASSIFY_TESTDATA,
		.classify_data = {
			.testData = io_dev_bufs,
			.num_testData = num_testData,
		}
	};

	//same concept as above, but now testData_size away and new pointer is the classification output
	//no mem copy becuase this pointer is where we are going to store out output
	ret = gdl_add_to_mem_handle(&cmd.classify_data.classification, cmd.classify_data.testData, testData_size);
	if (ret) {
		gsi_error("gdl_add_to_mem_handle() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}
	
	uint64_t cmd_buf_size = sizeof(cmd);
	dev_cmd_buf = gdl_mem_alloc_aligned(ctx_id, cmd_buf_size, GDL_CONST_MAPPED_POOL, GDL_ALIGN_32);
	if (gdl_mem_handle_is_null(dev_cmd_buf)) {
		gsi_error("gdl_mem_alloc() failed to allocate %lu bytes", cmd_buf_size);
		ret = gsi_status(ENOMEM);
		goto CLEAN_UP;
	}

	ret = gdl_mem_cpy_to_dev(dev_cmd_buf, &cmd, cmd_buf_size);
	if (ret) {
		gsi_error("gdl_mem_cpy_to_dev() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}
	clock_gettime(CLOCK_REALTIME, &APU_Timing.startClassificationDevice);
	ret = gdl_run_task_timeout(
			ctx_id,              /* @ctx_handler - the id of a hardware context previously allocated */
			GDL_TASK(gd_lab_3),  /* @code_offset - the code offset of the function that the task should execute */
			dev_cmd_buf,         /* @inp - input memory handle */
			GDL_MEM_HANDLE_NULL, /* @outp - output memory handle */
			GDL_TEMPORARY_DEFAULT_MEM_BUF,      /* @mem_buf - an array of previously allocated memory handles and their sizes */
			GDL_TEMPORARY_DEFAULT_MEM_BUF_SIZE, /* @buf_size - the length of the mem_buf array */
			GDL_TEMPORARY_DEFAULT_CORE_INDEX,   /* @apuc_idx - the apuc that the task should be executed on */
			NULL,              /* @comp - if task was successfully scheduled, and @comp is provided, the task completion status, or any error is returned in comp. */
			0,                 /* @ms_timeout - the time in mili-seconds a task should wait for completion before aborting (0 indicates waiting indefinitely) */
			GDL_USER_MAPPING); /* @map_type - determine the mapping type for the specific task */
	clock_gettime(CLOCK_REALTIME, &APU_Timing.stopClassificationDevice);
	
	if (ret) {
		gsi_error("gdl_run_task_timeout() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}

	ret = gdl_mem_cpy_from_dev(classVector, cmd.classify_data.classification, output_size);
	if (ret) {
		gsi_error("gdl_mem_cpy_from_dev() failed: %s", gsi_status_errorstr(ret));
		goto CLEAN_UP;
	}

	FILE *fileOut = fopen("./output.txt", "w");
	for(int i = 0; i < num_testData; i++){
		fprintf(fileOut,"%f\n",convertFloat16Back(classVector[i]));//this is debug
		//fprintf(fileOut,"%x\n",classVector[i]);
	}
	printf("Finished checking results\n");
	

CLEAN_UP:
	gdl_mem_free(dev_cmd_buf);
	gdl_mem_free(io_dev_bufs);

	return ret;
}

static int convertGSIFloat(float a){
    int* ptr = (int*)&a;
    int value = *ptr;
    int fracBits = (value>>14)&0x1ff;
    int exponent = (value>>23)&0xff;
    int sign = (value>>31);
    exponent -= 127;
    exponent+=31;
    exponent = (exponent&0x3f)<<9;
    return ((sign<<15)&0x8000)|(exponent)|fracBits;
    
}

static float convertGSIFloatBack(int a){
    int fraction = (a&0x1ff)<<14;
    int exponent = (a&0x7e00)>>9;
    int sign = (a&0x8000)<<16;
    int finalValue = 0;
    float* ptr = NULL;
    exponent -= 31;
    exponent += 127;
    exponent = (exponent&0xff)<<23;
    finalValue = (sign|exponent|fraction);
    ptr = (float*)&finalValue;
    return *ptr;
}

static int convertFloat16(float a){
	int* ptr = (int*)&a;
	unsigned int fltInt32 = *ptr;
	unsigned short fltInt16;

	fltInt16 = (fltInt32 >> 31) << 5;
	unsigned short tmp = (fltInt32 >> 23) & 0xff;
	tmp = (tmp - 0x70) & ((unsigned int)((int)(0x70 - tmp) >> 4) >> 27);
	fltInt16 = (fltInt16 | tmp) << 10;
	fltInt16 |= (fltInt32 >> 13) & 0x3ff;
	return fltInt16;
}

static void getSupportVectorsAndWeights(uint16_t* vector, uint16_t* weights, uint32_t* gamma, uint32_t* intercept, uint32_t numVectors, uint32_t numFeatures, char* SVMPath){
	//gets support vectors and weights for each
	float dummy = 0;
	char buf[100];
	strcpy(buf,SVMPath);
	FILE *fileVectors = fopen(strcat(buf,"/supportVectors.txt"), "r");
	strcpy(buf,SVMPath);
	FILE *fileWeights = fopen(strcat(buf,"/supportWeights.txt"), "r");
	strcpy(buf,SVMPath);
	FILE *fileGamma = fopen(strcat(buf,"/supportGamma.txt"), "r");
	strcpy(buf,SVMPath);
	FILE *fileIntercept = fopen(strcat(buf,"/supportIntercept.txt"), "r");
	//Read data from file
    for (uint32_t i = 0; i < numVectors; i++) {
        for (uint32_t j = 0; j < numFeatures; j++) {
            if (fscanf(fileVectors, "%f", &dummy) != 1) {
                fprintf(stderr, "Error reading support vectors file, at line %i, element: %i\n",i,j);
				exit(69);
            }
			vector[(i*numFeatures)+j] = convertFloat16(dummy);
        }
        if (fscanf(fileWeights, "%f", &dummy) != 1) {
                fprintf(stderr, "Error reading weights file, at line %i\n",i);
				exit(69);
        }
		weights[i] = convertFloat16(dummy);

    }
    fclose(fileVectors);
	fclose(fileWeights);

	//get the two one value parameters
    if(fscanf(fileGamma, "%f", &dummy) != 1){
        fprintf(stderr, "Error reading Gamma file\n");
		exit(69);
    }
	*gamma = convertFloat16(dummy);
    if(fscanf(fileIntercept, "%f", &dummy) != 1){
        fprintf(stderr, "Error reading Intercept file\n");
		exit(69);
    }
	*intercept = convertFloat16(dummy);
    fclose(fileGamma);
    fclose(fileIntercept);
}

static void getTestDataAndOthers(uint16_t* testData, uint32_t numTestData, uint32_t numFeatures, char* SVMPath){
	float dummy = 0;
	FILE *fileTestData = fopen(strcat(SVMPath,"/supportTestData.txt"), "r");
	//Read test data from file
    for (uint32_t i = 0; i < numTestData; i++) {
        for (uint32_t j = 0; j < numFeatures; j++) {
            if (fscanf(fileTestData, "%f", &dummy) != 1) {
                fprintf(stderr, "Error reading file, at line %i\n",i);
            }
			testData[(i*numFeatures)+j] = convertFloat16(dummy);
        }
    }
    fclose(fileTestData);
}

struct lab_3_args {
	uint32_t num_support_vectors;
	uint32_t num_features;
	uint32_t num_testData;
};

static int parse_args(struct lab_3_args *args, int argc, char *argv[])
{
	if (5 != argc) {
		gsi_error("usage: %s num_support_vectors num_features num_testData SVM_Parameter_Directory", argv[0]);
		return gsi_status(EINVAL);
	}

	args->num_support_vectors = atoi(argv[1]);
	args->num_features = atoi(argv[2]);
	args->num_testData = atoi(argv[3]);

	return 0;
}


// For Simulator:
enum { NUM_CTXS = 1 };
static struct gsi_sim_contexts g_ctxs[NUM_CTXS] = {
	{
		.apu_count = 1,
		.apucs_per_apu = 4,
		.mem_size = 0x40000000,
	}
};

int main(int argc, char *argv[])
{
	struct lab_3_args args;
	int ret = parse_args(&args, argc, argv);
	if (ret) {
		gsi_fatal("parse_args() failed");
	}
	
	//allocate memory
	struct timespec startEntire, startDataTransfer, stopDataTransfer, startDataTransferDevice, stopDataTransferDevice;
	struct timespec startClassification, stopClassification, startClassificationDevice, stopClassificationDevice;
	double totalTime = 0;
	uint16_t *supportVectors= NULL, *testData = NULL, *weights = NULL, *classVector = NULL;
	uint32_t gamma = 0.0, intercept = 0.0;
	supportVectors = malloc(sizeof(uint16_t) * args.num_support_vectors * args.num_features);
	weights = malloc(sizeof(uint16_t) * args.num_support_vectors);
	testData = malloc(sizeof(uint16_t) * args.num_testData * args.num_features);
	classVector = malloc(sizeof(uint16_t) * args.num_testData);

	const long long unsigned int const_mapped_size_req = 3L * 1024L * 1024L * 1024L;
	long long unsigned int const_mapped_size_recv, dynamic_mapped_size_recv;

	if (NULL == supportVectors || NULL == testData || NULL == weights || classVector == NULL) {
		gsi_error("malloc failed");
		ret = gsi_status(ENOMEM);
		goto CLEAN_UP;
	}

	gsi_libsys_init(
		argv[0], /* program name */
		true);   /* log_to_screen */

	gsi_sim_create_simulator(NUM_CTXS, g_ctxs);

	uint32_t num_ctxs;
	struct gdl_context_desc contexts_desc[GDL_MAX_NUM_CONTEXTS];

	clock_gettime(CLOCK_REALTIME, &startEntire);
	gdl_init();
	gdl_context_count_get(&num_ctxs);
	gdl_context_desc_get(contexts_desc, num_ctxs);

	/* Use first available context */
	gdl_context_handle_t valid_ctx_id;
	uint32_t ctx;
	for (ctx = 0; ctx < num_ctxs; ++ctx) {
		if (contexts_desc[ctx].status == GDL_CONTEXT_READY) {
			valid_ctx_id = contexts_desc[ctx].ctx_id;
			break;
		}
	}

	if (ctx == num_ctxs) {
		gsi_fatal("Failed to find valid context");
	}

	ret = gdl_context_alloc(valid_ctx_id, const_mapped_size_req, &const_mapped_size_recv, &dynamic_mapped_size_recv);
	if (ret) {
		gsi_fatal("gdl_context_alloc failed: %s", gsi_status_errorstr(ret));
	}

	//load support vectors, weights, gamma, and intercept from files
	getSupportVectorsAndWeights(supportVectors, weights, &gamma, &intercept, args.num_support_vectors, args.num_features, argv[4]);

	clock_gettime(CLOCK_REALTIME, &startDataTransfer);
	ret = load_SVM(valid_ctx_id, supportVectors, weights, gamma, intercept, args.num_support_vectors, args.num_features);
	if (ret) {
		gsi_error("load_SVM() failed with %d", ret);
		goto CLEAN_UP;
	}
	clock_gettime(CLOCK_REALTIME, &stopDataTransfer);

	//load test data to make inference on from file
	getTestDataAndOthers(testData, args.num_testData, args.num_features, argv[4]);
	clock_gettime(CLOCK_REALTIME, &startClassification);
	ret = do_classification(valid_ctx_id, classVector, testData, args.num_testData, args.num_features, args.num_support_vectors);
		if (ret) {
			gsi_error("do_search() failed with %d", ret);
			goto CLEAN_UP;
		}
	//this clock is the entire operation
	clock_gettime(CLOCK_REALTIME, &stopClassification);
	//get time for entire, data transfer with overhead, data transfer without overheaad, classification with overhead, classification without overhead

	//Entire Execution
	printf("%lf\n",((double)(stopClassification.tv_sec - startEntire.tv_sec)) + ((double)(stopClassification.tv_nsec - startEntire.tv_nsec)) / 1000000000L);
	//Data Transfer with Overhead
	printf("%lf\n",((double)(stopDataTransfer.tv_sec - startDataTransfer.tv_sec)) + ((double)(stopDataTransfer.tv_nsec - startDataTransfer.tv_nsec)) / 1000000000L);
	//Data Transfer without Overhead
	printf("%lf\n",((double)(APU_Timing.stopDataTransferDevice.tv_sec - APU_Timing.startDataTransferDevice.tv_sec)) + ((double)(APU_Timing.stopDataTransferDevice.tv_nsec - APU_Timing.startDataTransferDevice.tv_nsec)) / 1000000000L);
	//Classification with Overhead
	printf("%lf\n",((double)(stopClassification.tv_sec - startClassification.tv_sec)) + ((double)(stopClassification.tv_nsec - startClassification.tv_nsec)) / 1000000000L);
	//Classification without Overhead
	printf("%lf\n",((double)(APU_Timing.stopClassificationDevice.tv_sec - APU_Timing.startClassificationDevice.tv_sec)) + ((double)(APU_Timing.stopClassificationDevice.tv_nsec - APU_Timing.startClassificationDevice.tv_nsec)) / 1000000000L);



CLEAN_UP:
	free(testData);
	free(weights);
	free(classVector);
	free(supportVectors);

	gdl_context_free(valid_ctx_id);
	gdl_exit();

	gsi_libsys_exit();
	if (ret != 0) {
		printf("\nFailure\n");
	}
	return ret;
}
