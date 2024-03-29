#include <gsi/libsys/assert.h>
#include <gsi/libsys.h>
#include <gsi/libgal.h>
#include <gsi/gal-fast-funcs.h>
#include <gsi/libgvml_memory.h>

#include "gsi_device_lab_3_dma.h"

static void direct_dma_l4_to_l2_16k(int32_t apc_id, const void *l4_src, uint64_t num_512b_chunks)
{
	struct gal_fast_l2dma_l4_l2_transaction txn = {
		.num_steps = 1,
		.step_size_num_512b_chunk = num_512b_chunks,
		.l4_addr = (void *)l4_src,
		.l2_mode = GAL_L2T_MODE_64,
		.l2_col_group = 0,
	};
	gal_fast_l2dma_mem_to_l2_start(apc_id, 1, &txn, GAL_L2DMA_L2_READY_SET);
}

static void dma_l2_to_l1_32k(enum gvml_vm_reg vmr)
{
	gal_fast_l2dma_l2_ready_rst_all();
	for (uint8_t bank = 0; bank < 4; bank++) {
		gvml_load_vmr_16(vmr, bank, bank == (4 - 1), bank * 2);
	}
}

static void dma_l2_sync(void)
{
	gal_fast_l2dma_async_memcpy_end(GAL_L2DMA_APC_ID_0);
	gal_fast_l2dma_async_memcpy_end(GAL_L2DMA_APC_ID_1);
}

void direct_dma_l4_to_l1_32k(enum gvml_vm_reg vmr, const void *l4_src)
{
	const uint64_t num_512b_chunks_in_32k_16b_elements = sizeof(uint16_t) * 32 * 1024 / 512;
	direct_dma_l4_to_l2_16k(GAL_L2DMA_APC_ID_0, l4_src, num_512b_chunks_in_32k_16b_elements / 2);
	direct_dma_l4_to_l2_16k(GAL_L2DMA_APC_ID_1, l4_src + 32 * 1024, num_512b_chunks_in_32k_16b_elements / 2);
	dma_l2_sync();
	dma_l2_to_l1_32k(vmr);
}

static void direct_dma_l2_to_l4_16k(int32_t apc_id, void *l4_dst, uint64_t num_512b_chunks)
{
	struct gal_fast_l2dma_l4_l2_transaction txn = {
		.num_steps = 1,
		.step_size_num_512b_chunk = num_512b_chunks,
		.l4_addr = l4_dst,
		.l2_mode = GAL_L2T_MODE_64,
		.l2_col_group = 0,
	};
	gal_fast_l2dma_l2_to_mem_start(apc_id, 1, &txn, GAL_L2DMA_L2_READY_SET);
}

static void dma_l1_to_l2_32k(enum gvml_vm_reg vmr)
{
	gal_fast_l2dma_l2_ready_rst_all();
	for (uint8_t bank = 0; bank < 4; bank++) {
		gvml_store_vmr_16(vmr, bank, bank == (4 - 1), bank * 2);
	}
}

void direct_dma_l1_to_l4_32k(void *l4_dst, enum gvml_vm_reg vmr)
{
	dma_l1_to_l2_32k(vmr);
	const uint64_t num_512b_chunks_in_32k_16b_elements = sizeof(uint16_t) * 32 * 1024 / 512;
	direct_dma_l2_to_l4_16k(GAL_L2DMA_APC_ID_0, l4_dst, num_512b_chunks_in_32k_16b_elements / 2);
	direct_dma_l2_to_l4_16k(GAL_L2DMA_APC_ID_1, l4_dst + 32 * 1024, num_512b_chunks_in_32k_16b_elements / 2);
	dma_l2_sync();
}
