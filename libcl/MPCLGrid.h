#ifndef _MPGRIDCL_H
#define _MPGRIDCL_H

#ifdef __cplusplus
extern "C" {
#endif

#ifndef _MPGRID_H
#include <MPGrid.h>
#endif

#include <CL/cl.h>

#define MPCL_PLATFORM_MAX 32

typedef struct MPCL_GridKernelData {
#ifndef _DEBUG
	PyObject_HEAD
#endif
	cl_context context;
	cl_command_queue queue;
	cl_program program;
	cl_kernel kernels[2];
	cl_mem element;
	cl_mem type;
	cl_mem update;
	cl_mem val;
	cl_mem buf;
	cl_mem inter_x, inter_y, inter_z;
	cl_mem coef_x, coef_y, coef_z;
	cl_mem rhoc;
	cl_mem bound;
	cl_mem cx, cy, cz;
	int local_coef;
} MPCL_GridKernelData;

void MPCL_GridPlatformInfo();
void MPCL_GridKernelInit(MPCL_GridKernelData *gkd, MP_GridData *data, int platform_id);
void MPCL_GridKernelFinal(MPCL_GridKernelData *gkd);
double MPCL_GridKernelSolve(MPCL_GridKernelData *gkd, MP_GridData *data, double dt, int nloop);

#ifdef __cplusplus
}
#endif

#endif /* _MPGRIDCL_H */