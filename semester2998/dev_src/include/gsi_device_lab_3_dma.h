#ifndef __GSI_DEVICE_LAB_3_DMA_H__
#define __GSI_DEVICE_LAB_3_DMA_H__

#include <stdint.h>
#include <gsi/libgvml_memory.h>

void direct_dma_l4_to_l1_32k(enum gvml_vm_reg vmr, const void *l4_src);

void direct_dma_l1_to_l4_32k(void *l4_dst, enum gvml_vm_reg vmr);

#endif /* __GSI_DEVICE_LAB_3_DMA_H__ */
