#include "MPCLGrid.h"

#define MAX_LOG_SIZE 65536

void MPCL_GridPlatformInfo()
{
	cl_platform_id platforms[MPCL_PLATFORM_MAX];
	cl_uint nplatforms;
	cl_int status;
	int i;
	char buffer[1024];

	status = clGetPlatformIDs(MPCL_PLATFORM_MAX, platforms, &nplatforms);
	if (status != CL_SUCCESS) {
		printf("clGetPlatformIds failed with status %d\n", status);
		return;
	}
	printf("Number of platform(s) : %d\n", nplatforms);
	for (i = 0; i < (int)nplatforms; i++) {
		clGetPlatformInfo(platforms[i], CL_PLATFORM_PROFILE, sizeof(buffer)-1, buffer, NULL);
		printf("Platform %d profile    : %s\n", i, buffer);
		clGetPlatformInfo(platforms[i], CL_PLATFORM_VERSION, sizeof(buffer)-1, buffer, NULL);
		printf("Platform %d version    : %s\n", i, buffer);
		clGetPlatformInfo(platforms[i], CL_PLATFORM_NAME, sizeof(buffer)-1, buffer, NULL);
		printf("Platform %d name       : %s\n", i, buffer);
		clGetPlatformInfo(platforms[i], CL_PLATFORM_VENDOR, sizeof(buffer)-1, buffer, NULL);
		printf("Platform %d vendor     : %s\n", i, buffer);
		clGetPlatformInfo(platforms[i], CL_PLATFORM_EXTENSIONS, sizeof(buffer)-1, buffer, NULL);
		printf("Platform %d extensions : %s\n", i, buffer);
	}
}

static void PrintError(char msg[], cl_int status)
{
	switch (status) {
	case CL_BUILD_PROGRAM_FAILURE: fprintf(stderr, "Error : %s : Build program failure\n", msg); break;
	case CL_COMPILER_NOT_AVAILABLE: fprintf(stderr, "Error : %s : Compiler not available\n", msg); break;
	case CL_DEVICE_NOT_AVAILABLE: fprintf(stderr, "Error : %s : Device not available\n", msg); break;
	case CL_DEVICE_NOT_FOUND: fprintf(stderr, "Error : %s : Device not found\n", msg); break;
	case CL_IMAGE_FORMAT_NOT_SUPPORTED: fprintf(stderr, "Error : %s : Image format not supported\n", msg); break;
	case CL_IMAGE_FORMAT_MISMATCH: fprintf(stderr, "Error : %s : Image format mismatch\n", msg); break;
	case CL_INVALID_ARG_INDEX: fprintf(stderr, "Error : %s : Invalid arg index\n", msg); break;
	case CL_INVALID_ARG_SIZE: fprintf(stderr, "Error : %s : Invalid arg size\n", msg); break;
	case CL_INVALID_ARG_VALUE: fprintf(stderr, "Error : %s : Invalid arg value\n", msg); break;
	case CL_INVALID_BINARY: fprintf(stderr, "Error : %s : Invalid binary\n", msg); break;
	case CL_INVALID_BUFFER_SIZE: fprintf(stderr, "Error : %s : Invalid buffer size\n", msg); break;
	case CL_INVALID_BUILD_OPTIONS: fprintf(stderr, "Error : %s : Invalid build options\n", msg); break;
	case CL_INVALID_COMMAND_QUEUE: fprintf(stderr, "Error : %s : Invalid command queue\n", msg); break;
	case CL_INVALID_CONTEXT: fprintf(stderr, "Error : %s : Invalid context\n", msg); break;
	case CL_INVALID_DEVICE: fprintf(stderr, "Error : %s : Invalid device\n", msg); break;
	case CL_INVALID_DEVICE_TYPE: fprintf(stderr, "Error : %s : Invalid device type\n", msg); break;
	case CL_INVALID_EVENT: fprintf(stderr, "Error : %s : Invalid event\n", msg); break;
	case CL_INVALID_EVENT_WAIT_LIST: fprintf(stderr, "Error : %s : Invalid event wait list\n", msg); break;
	case CL_INVALID_GL_OBJECT: fprintf(stderr, "Error : %s : Invalid GL object\n", msg); break;
	case CL_INVALID_GLOBAL_OFFSET: fprintf(stderr, "Error : %s : Invalid global offset\n", msg); break;
	case CL_INVALID_HOST_PTR: fprintf(stderr, "Error : %s : Invalid host ptr\n", msg); break;
	case CL_INVALID_IMAGE_FORMAT_DESCRIPTOR: fprintf(stderr, "Error : %s : Invalid image format descriptor\n", msg); break;
	case CL_INVALID_IMAGE_SIZE: fprintf(stderr, "Error : %s : Invalid image size\n", msg); break;
	case CL_INVALID_KERNEL: fprintf(stderr, "Error : %s : Invalid kernel\n", msg); break;
	case CL_INVALID_KERNEL_ARGS: fprintf(stderr, "Error : %s : Invalid kernel args\n", msg); break;
	case CL_INVALID_KERNEL_DEFINITION: fprintf(stderr, "Error : %s : Invalid kernel definition\n", msg); break;
	case CL_INVALID_KERNEL_NAME: fprintf(stderr, "Error : %s : Invalid kernel name\n", msg); break;
	case CL_INVALID_MEM_OBJECT: fprintf(stderr, "Error : %s : Invalid mem object\n", msg); break;
	case CL_INVALID_MIP_LEVEL: fprintf(stderr, "Error : %s : Invalid mip level\n", msg); break;
	case CL_INVALID_OPERATION: fprintf(stderr, "Error : %s : Invalid operation\n", msg); break;
	case CL_INVALID_PLATFORM: fprintf(stderr, "Error : %s : Invalid platform\n", msg); break;
	case CL_INVALID_PROGRAM: fprintf(stderr, "Error : %s : Invalid program\n", msg); break;
	case CL_INVALID_PROGRAM_EXECUTABLE: fprintf(stderr, "Error : %s : Invalid program executable\n", msg); break;
	case CL_INVALID_QUEUE_PROPERTIES: fprintf(stderr, "Error : %s : Invalid queue properties\n", msg); break;
	case CL_INVALID_SAMPLER: fprintf(stderr, "Error : %s : Invalid sampler\n", msg); break;
	case CL_INVALID_VALUE: fprintf(stderr, "Error : %s : Invalid value\n", msg); break;
	case CL_INVALID_WORK_DIMENSION: fprintf(stderr, "Error : %s : Invalid work dimension\n", msg); break;
	case CL_INVALID_WORK_GROUP_SIZE: fprintf(stderr, "Error : %s : Invalid work group size\n", msg); break;
	case CL_INVALID_WORK_ITEM_SIZE: fprintf(stderr, "Error : %s : Invalid work item size\n", msg); break;
	case CL_MAP_FAILURE: fprintf(stderr, "Error : %s : Map failure\n", msg); break;
	case CL_MEM_COPY_OVERLAP: fprintf(stderr, "Error : %s : Mem copy overlap\n", msg); break;
	case CL_MEM_OBJECT_ALLOCATION_FAILURE: fprintf(stderr, "Error : %s : Mem object allocation failure\n", msg); break;
	case CL_OUT_OF_HOST_MEMORY: fprintf(stderr, "Error : %s : Out of host memory\n", msg); break;
	case CL_OUT_OF_RESOURCES: fprintf(stderr, "Error : %s : Out of resources\n", msg); break;
	case CL_PROFILING_INFO_NOT_AVAILABLE: fprintf(stderr, "Error : %s : Profiling info not available\n", msg); break;
	case CL_SUCCESS: break;
	default: fprintf(stderr, "Error : %s : %d\n", msg, status); break;
	}
}

static void PrintBuildLog(cl_program program, cl_device_id device)
{
	cl_int status;
	size_t size_ret;
	char buffer[MAX_LOG_SIZE];

	status = clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, MAX_LOG_SIZE, buffer, &size_ret);
	if (status == CL_SUCCESS) {
		buffer[size_ret] = '\0';
		fprintf(stderr, "--- Build log ---\n");
		fprintf(stderr, "%s\n", buffer);
		fprintf(stderr, "--- End of build log ---\n");
	}
	else {
		PrintError("clGetProgramBuildInfo failed", status);
	}
}

static const char *Sources[] = {
	"#pragma OPENCL EXTENSION cl_khr_fp64: enable\n\
	enum { MP_GridBoundInsulate, MP_GridBoundPeriodic };\n\
	enum { MP_GridInterCond, MP_GridInterTrans };\n\
	__kernel void ElementFlow(\
	__global const double *element,\
	const int ntype,\
	__global const short *type,\
	__global const short *update,\
	__global const double *val,\
	__global double *buf,\
	__global const double *rhoc,\
	__global const int *bound,\
	__global const int *inter_x,\
	__global const int *inter_y,\
	__global const int *inter_z,\
	__global const double *coef_x,\
	__global const double *coef_y,\
	__global const double *coef_z,\
	const double dt)\n\
	{\
		int x = get_global_id(0);\n\
		int y = get_global_id(1);\n\
		int z = get_global_id(2);\n\
		int nx = get_global_size(0);\n\
		int ny = get_global_size(1);\n\
		int nz = get_global_size(2);\n\
		int id0 = x + y*nx + z*nx*ny;\n\
		if (!update[id0]) {\n\
			buf[id0] = val[id0];\n\
			return;\n\
		}\n\
		int id1, cid;\n\
		double xl, xu, yl, yu, zl, zu;\n\
		if (x == 0) {\n\
			if (bound[0] == MP_GridBoundInsulate) xl = 0.0;\n\
			else {\n\
				id1 = nx-1 + y*nx + z*nx*ny;\n\
				cid = type[id0] + type[id1]*ntype;\n\
				if (inter_x[cid] == MP_GridInterCond) xl = coef_x[cid] / element[0] * (val[id0] - val[id1]);\n\
				else if (inter_x[cid] == MP_GridInterTrans) xl = coef_x[cid] * (val[id0] - val[id1]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x-1 + y*nx + z*nx*ny;\n\
			cid = type[id0] + type[id1]*ntype;\n\
			if (inter_x[cid] == MP_GridInterCond) xl = coef_x[cid] / element[0] * (val[id0] - val[id1]);\n\
			else if (inter_x[cid] == MP_GridInterTrans) xl = coef_x[cid] * (val[id0] - val[id1]);\n\
		}\n\
		if (x == nx-1) {\n\
			if (bound[3] == MP_GridBoundInsulate) xu = 0.0;\n\
			else {\n\
				id1 = y*nx + z*nx*ny;\n\
				cid = type[id1] + type[id0]*ntype;\n\
				if (inter_x[cid] == MP_GridInterCond) xu = coef_x[cid] / element[0] * (val[id1] - val[id0]);\n\
				else if (inter_x[cid] == MP_GridInterTrans) xu = coef_x[cid] * (val[id1] - val[id0]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x+1 + y*nx + z*nx*ny;\n\
			cid = type[id1] + type[id0]*ntype;\n\
			if (inter_x[cid] == MP_GridInterCond) xu = coef_x[cid] / element[0] * (val[id1] - val[id0]);\n\
			else if (inter_x[cid] == MP_GridInterTrans) xu = coef_x[cid] * (val[id1] - val[id0]);\n\
		}\n\
		if (y == 0) {\n\
			if (bound[1] == MP_GridBoundInsulate) yl = 0.0;\n\
			else {\n\
				id1 = x + (ny-1)*nx + z*nx*ny;\n\
				cid = type[id0] + type[id1]*ntype;\n\
				if (inter_y[cid] == MP_GridInterCond) yl = coef_y[cid] / element[1] * (val[id0] - val[id1]);\n\
				else if (inter_y[cid] == MP_GridInterTrans) yl = coef_y[cid] * (val[id0] - val[id1]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + (y-1)*nx + z*nx*ny;\n\
			cid = type[id0] + type[id1]*ntype;\n\
			if (inter_y[cid] == MP_GridInterCond) yl = coef_y[cid] / element[1] * (val[id0] - val[id1]);\n\
			else if (inter_y[cid] == MP_GridInterTrans) yl = coef_y[cid] * (val[id0] - val[id1]);\n\
		}\n\
		if (y == ny - 1) {\n\
			if (bound[4] == MP_GridBoundInsulate) yu = 0.0;\n\
			else {\n\
				id1 = x + z*nx*ny;\n\
				cid = type[id1] + type[id0]*ntype;\n\
				if (inter_y[cid] == MP_GridInterCond) yu = coef_y[cid] / element[1] * (val[id1] - val[id0]);\n\
				else if (inter_y[cid] == MP_GridInterTrans) yu = coef_y[cid] * (val[id1] - val[id0]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + (y+1)*nx + z*nx*ny;\n\
			cid = type[id1] + type[id0]*ntype;\n\
			if (inter_y[cid] == MP_GridInterCond) yu = coef_y[cid] / element[1] * (val[id1] - val[id0]);\n\
			else if (inter_y[cid] == MP_GridInterTrans) yu = coef_y[cid] * (val[id1] - val[id0]);\n\
		}\n\
		if (z == 0) {\n\
			if (bound[2] == MP_GridBoundInsulate) zl = 0.0;\n\
			else {\n\
				id1 = x + y*nx + (nz-1)*nx*ny;\n\
				cid = type[id0] + type[id1]*ntype;\n\
				if (inter_z[cid] == MP_GridInterCond) zl = coef_z[cid] / element[2] * (val[id0] - val[id1]);\n\
				else if (inter_z[cid] == MP_GridInterTrans) zl = coef_z[cid] * (val[id0] - val[id1]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + y*nx + (z-1)*nx*ny;\n\
			cid = type[id0] + type[id1]*ntype;\n\
			if (inter_z[cid] == MP_GridInterCond) zl = coef_z[cid] / element[2] * (val[id0] - val[id1]);\n\
			else if (inter_z[cid] == MP_GridInterTrans) zl = coef_z[cid] * (val[id0] - val[id1]);\n\
		}\n\
		if (z == nz - 1) {\n\
			if (bound[5] == MP_GridBoundInsulate) zu = 0.0;\n\
			else {\n\
				id1 = x + y*nx;\n\
				cid = type[id1] + type[id0]*ntype;\n\
				if (inter_z[cid] == MP_GridInterCond) zu = coef_z[cid] / element[2] * (val[id1] - val[id0]);\n\
				else if (inter_z[cid] == MP_GridInterTrans) zu = coef_z[cid] * (val[id1] - val[id0]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + y*nx + (z+1)*nx*ny;\n\
			cid = type[id1] + type[id0]*ntype;\n\
			if (inter_z[cid] == MP_GridInterCond) zu = coef_z[cid] / element[2] * (val[id1] - val[id0]);\n\
			else if (inter_z[cid] == MP_GridInterTrans) zu = coef_z[cid] * (val[id1] - val[id0]);\n\
		}\n\
		double f = ((xu-xl)/element[0] + (yu-yl)/element[1] + (zu-zl)/element[2]) / rhoc[type[id0]];\n\
		buf[id0] = val[id0] + f*dt;\n\
	}",
	"__kernel void ElementFlowLocalCoef(\
	__global const double *element,\
	const int ntype,\
	__global const short *type,\
	__global const short *update,\
	__global const double *val,\
	__global double *buf,\
	__global const double *rhoc,\
	__global const int *bound,\
	__global const double *cx,\
	__global const double *cy,\
	__global const double *cz,\
	const double dt)\n\
	{\
		int x = get_global_id(0);\n\
		int y = get_global_id(1);\n\
		int z = get_global_id(2);\n\
		int nx = get_global_size(0);\n\
		int ny = get_global_size(1);\n\
		int nz = get_global_size(2);\n\
		int id0 = x + y*nx + z*nx*ny;\n\
		if (!update[id0]) {\n\
			buf[id0] = val[id0];\n\
			return;\n\
		}\n\
		int id1;\n\
		double xl, xu, yl, yu, zl, zu;\n\
		if (x == 0) {\n\
			if (bound[0] == MP_GridBoundInsulate) xl = 0.0;\n\
			else {\n\
				id1 = nx-1 + y*nx + z*nx*ny;\n\
				xl = cx[id1] * (val[id0] - val[id1]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x-1 + y*nx + z*nx*ny;\n\
			xl = cx[id1] * (val[id0] - val[id1]);\n\
		}\n\
		if (x == nx-1) {\n\
			if (bound[3] == MP_GridBoundInsulate) xu = 0.0;\n\
			else {\n\
				id1 = y*nx + z*nx*ny;\n\
				xu = cx[id0] * (val[id1] - val[id0]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x+1 + y*nx + z*nx*ny;\n\
			xu = cx[id0] * (val[id1] - val[id0]);\n\
		}\n\
		if (y == 0) {\n\
			if (bound[1] == MP_GridBoundInsulate) yl = 0.0;\n\
			else {\n\
				id1 = x + (ny-1)*nx + z*nx*ny;\n\
				yl = cy[id1] * (val[id0] - val[id1]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + (y-1)*nx + z*nx*ny;\n\
			yl = cy[id1] * (val[id0] - val[id1]);\n\
		}\n\
		if (y == ny - 1) {\n\
			if (bound[4] == MP_GridBoundInsulate) yu = 0.0;\n\
			else {\n\
				id1 = x + z*nx*ny;\n\
				yu = cy[id0] * (val[id1] - val[id0]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + (y+1)*nx + z*nx*ny;\n\
			yu = cy[id0] * (val[id1] - val[id0]);\n\
		}\n\
		if (z == 0) {\n\
			if (bound[2] == MP_GridBoundInsulate) zl = 0.0;\n\
			else {\n\
				id1 = x + y*nx + (nz-1)*nx*ny;\n\
				zl = cz[id1] * (val[id0] - val[id1]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + y*nx + (z-1)*nx*ny;\n\
			zl = cz[id1] * (val[id0] - val[id1]);\n\
		}\n\
		if (z == nz - 1) {\n\
			if (bound[5] == MP_GridBoundInsulate) zu = 0.0;\n\
			else {\n\
				id1 = x + y*nx;\n\
				zu = cz[id0] * (val[id1] - val[id0]);\n\
			}\n\
		}\n\
		else {\n\
			id1 = x + y*nx + (z+1)*nx*ny;\n\
			zu = cz[id0] * (val[id1] - val[id0]);\n\
		}\n\
		double f = ((xu-xl)/element[0] + (yu-yl)/element[1] + (zu-zl)/element[2]) / rhoc[type[id0]];\n\
		buf[id0] = val[id0] + f*dt;\n\
	}",
	"__kernel void ElementUpdate(\
	__global double *val,\
	__global const double *buf)\n\
	{\n\
		int x = get_global_id(0);\n\
		int y = get_global_id(1);\n\
		int z = get_global_id(2);\n\
		int nx = get_global_size(0);\n\
		int ny = get_global_size(1);\n\
		int nz = get_global_size(2);\n\
		int id0 = x + y*nx + z*nx*ny;\n\
		val[id0] = buf[id0];\n\
	}"
};

void MPCL_GridKernelInit(MPCL_GridKernelData *gkd, MP_GridData *data, int platform_id)
{
	cl_int status;
	cl_platform_id platforms[MPCL_PLATFORM_MAX];
	cl_uint nplatforms;
	cl_device_id device;
	cl_uint ndevice;

	gkd->local_coef = data->local_coef;
	status = clGetPlatformIDs(MPCL_PLATFORM_MAX, platforms, &nplatforms);
	if (status != CL_SUCCESS) {
		PrintError("clGetPlatformIDs failed", status);
		return;
	}
	status = clGetDeviceIDs(platforms[platform_id], CL_DEVICE_TYPE_DEFAULT, 1, &device, &ndevice);
	if (status != CL_SUCCESS) {
		PrintError("clGetDeviceIDs failed", status);
		return;
	}
	gkd->context = clCreateContext(NULL, 1, &device, NULL, NULL, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateContext failed", status);
		return;
	}
	gkd->queue = clCreateCommandQueue(gkd->context, device, 0, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateCommandQueue failed", status);
		return;
	}
	gkd->program = clCreateProgramWithSource(gkd->context, 3, (const char**)&Sources, NULL, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateProgramWithSource failed", status);
		return;
	}
	status = clBuildProgram(gkd->program, 1, &device, NULL, NULL, NULL);
	if (status != CL_SUCCESS) {
		PrintError("clBuildProgram failed", status);
		PrintBuildLog(gkd->program, device);
		return;
	}
	clUnloadCompiler();
	if (!gkd->local_coef) {
		gkd->kernels[0] = clCreateKernel(gkd->program, "ElementFlow", &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateKernel failed", status);
			return;
		}
	}
	else {
		gkd->kernels[0] = clCreateKernel(gkd->program, "ElementFlowLocalCoef", &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateKernel failed", status);
			return;
		}
	}
	gkd->kernels[1] = clCreateKernel(gkd->program, "ElementUpdate", &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateKernel failed", status);
		return;
	}
	gkd->element = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
		sizeof(cl_double)* 3, data->element, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateBuffer failed", status);
		return;
	}
	gkd->type = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
		sizeof(cl_short)*data->ntot, data->type, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateBuffer failed", status);
		return;
	}
	gkd->update = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
		sizeof(cl_short)*data->ntot, data->update, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateBuffer failed", status);
		return;
	}
	gkd->val = clCreateBuffer(gkd->context, CL_MEM_READ_WRITE,
		sizeof(cl_double)*data->ntot, NULL, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateBuffer failed", status);
		return;
	}
	gkd->buf = clCreateBuffer(gkd->context, CL_MEM_READ_WRITE,
		sizeof(cl_double)*data->ntot, NULL, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateBuffer failed", status);
		return;
	}
	gkd->rhoc = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
		sizeof(cl_double)*data->ntype, data->rhoc, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateBuffer failed", status);
		return;
	}
	gkd->bound = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
		sizeof(cl_int) * 6, data->bound, &status);
	if (status != CL_SUCCESS) {
		PrintError("clCreateBuffer failed", status);
		return;
	}
	if (!gkd->local_coef) {
		gkd->inter_x = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_int)*data->ntype*data->ntype, data->inter_x, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
		gkd->inter_y = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_int)*data->ntype*data->ntype, data->inter_y, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
		gkd->inter_z = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_int)*data->ntype*data->ntype, data->inter_z, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
		gkd->coef_x = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_double)*data->ntype*data->ntype, data->coef_x, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
		gkd->coef_y = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_double)*data->ntype*data->ntype, data->coef_y, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
		gkd->coef_z = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_double)*data->ntype*data->ntype, data->coef_z, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
	}
	else {
		gkd->cx = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_double)*data->ntot, data->cx, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
		gkd->cy = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_double)*data->ntot, data->cy, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
		gkd->cz = clCreateBuffer(gkd->context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
			sizeof(cl_double)*data->ntot, data->cz, &status);
		if (status != CL_SUCCESS) {
			PrintError("clCreateBuffer failed", status);
			return;
		}
	}
}

void MPCL_GridKernelFinal(MPCL_GridKernelData *gkd)
{
	clReleaseMemObject(gkd->element);
	clReleaseMemObject(gkd->type);
	clReleaseMemObject(gkd->update);
	clReleaseMemObject(gkd->val);
	clReleaseMemObject(gkd->buf);
	clReleaseMemObject(gkd->rhoc);
	clReleaseMemObject(gkd->bound);
	if (!gkd->local_coef) {
		clReleaseMemObject(gkd->inter_x);
		clReleaseMemObject(gkd->inter_y);
		clReleaseMemObject(gkd->inter_z);
		clReleaseMemObject(gkd->coef_x);
		clReleaseMemObject(gkd->coef_y);
		clReleaseMemObject(gkd->coef_z);
	}
	else {
		clReleaseMemObject(gkd->cx);
		clReleaseMemObject(gkd->cy);
		clReleaseMemObject(gkd->cz);
	}
	clReleaseKernel(gkd->kernels[0]);
	clReleaseKernel(gkd->kernels[1]);
	clReleaseProgram(gkd->program);
	clReleaseCommandQueue(gkd->queue);
	clReleaseContext(gkd->context);
}

double MPCL_GridKernelSolve(MPCL_GridKernelData *gkd, MP_GridData *data, double dt, int nloop)
{
	cl_int status;
	size_t size[3];
	double dvtot = 0.0;
	int n = 0;
	int i;

	size[0] = data->size[0];
	size[1] = data->size[1];
	size[2] = data->size[2];
	status = clSetKernelArg(gkd->kernels[0], 0, sizeof(cl_mem), (void *)&(gkd->element));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[0], 1, sizeof(int), &(data->ntype));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[0], 2, sizeof(cl_mem), (void *)&(gkd->type));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[0], 3, sizeof(cl_mem), (void *)&(gkd->update));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[0], 4, sizeof(cl_mem), (void *)&(gkd->val));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[0], 5, sizeof(cl_mem), (void *)&(gkd->buf));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[0], 6, sizeof(cl_mem), (void *)&(gkd->rhoc));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[0], 7, sizeof(cl_mem), (void *)&(gkd->bound));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	if (!gkd->local_coef) {
		status = clSetKernelArg(gkd->kernels[0], 8, sizeof(cl_mem), (void *)&(gkd->inter_x));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 9, sizeof(cl_mem), (void *)&(gkd->inter_y));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 10, sizeof(cl_mem), (void *)&(gkd->inter_z));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 11, sizeof(cl_mem), (void *)&(gkd->coef_x));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 12, sizeof(cl_mem), (void *)&(gkd->coef_y));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 13, sizeof(cl_mem), (void *)&(gkd->coef_z));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 14, sizeof(double), &dt);
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
	}
	else {
		status = clSetKernelArg(gkd->kernels[0], 8, sizeof(cl_mem), (void *)&(gkd->cx));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 9, sizeof(cl_mem), (void *)&(gkd->cy));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 10, sizeof(cl_mem), (void *)&(gkd->cz));
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
		status = clSetKernelArg(gkd->kernels[0], 11, sizeof(double), &dt);
		if (status != CL_SUCCESS) {
			PrintError("clSetKernelArg failed", status);
			return 0.0;
		}
	}
	status = clSetKernelArg(gkd->kernels[1], 0, sizeof(cl_mem), (void *)&(gkd->val));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clSetKernelArg(gkd->kernels[1], 1, sizeof(cl_mem), (void *)&(gkd->buf));
	if (status != CL_SUCCESS) {
		PrintError("clSetKernelArg failed", status);
		return 0.0;
	}
	status = clEnqueueWriteBuffer(gkd->queue, gkd->val, CL_TRUE, 0,
		sizeof(cl_double)*data->ntot, data->val, 0, NULL, NULL);
	if (status != CL_SUCCESS) {
		PrintError("clEnqueueWriteBuffer failed", status);
		return 0.0;
	}
	status = clEnqueueWriteBuffer(gkd->queue, gkd->buf, CL_TRUE, 0,
		sizeof(cl_double)*data->ntot, data->buf, 0, NULL, NULL);
	if (status != CL_SUCCESS) {
		PrintError("clEnqueueWriteBuffer failed", status);
		return 0.0;
	}
	while (TRUE) {
		status = clEnqueueNDRangeKernel(gkd->queue, gkd->kernels[0], 3, NULL, size, 0, 0, NULL, NULL);
		if (status != CL_SUCCESS) {
			PrintError("clEnqueueNDRangeKernel failed", status);
			return 0.0;
		}
		status = clEnqueueBarrier(gkd->queue);
		if (status != CL_SUCCESS) {
			PrintError("clEnqueueBarrier failed", status);
			return 0.0;
		}
		(data->step)++;
		if (++n < nloop) {
			status = clEnqueueNDRangeKernel(gkd->queue, gkd->kernels[1], 3, NULL, size, 0, 0, NULL, NULL);
			if (status != CL_SUCCESS) {
				PrintError("clEnqueueNDRangeKernel failed", status);
				return 0.0;
			}
			status = clEnqueueBarrier(gkd->queue);
			if (status != CL_SUCCESS) {
				PrintError("clEnqueueBarrier failed", status);
				return 0.0;
			}
		}
		else {
			status = clEnqueueReadBuffer(gkd->queue, gkd->val, CL_TRUE, 0,
				sizeof(cl_double)*data->ntot, data->val, 0, NULL, NULL);
			if (status != CL_SUCCESS) {
				PrintError("clEnqueueReadBuffer failed", status);
				return 0.0;
			}
			status = clEnqueueReadBuffer(gkd->queue, gkd->buf, CL_TRUE, 0,
				sizeof(cl_double)*data->ntot, data->buf, 0, NULL, NULL);
			if (status != CL_SUCCESS) {
				PrintError("clEnqueueReadBuffer failed", status);
				return 0.0;
			}
			for (i = 0, dvtot = 0.0; i < data->ntot; i++) {
				if (data->update[i]) {
					dvtot += fabs(data->buf[i] - data->val[i]);
					data->val[i] = data->buf[i];
				}
			}
			break;
		}
	}
	return dvtot / data->ntot;
}
