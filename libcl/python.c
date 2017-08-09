#ifndef _DEBUG

#include "MPCLGrid.h"

static void PyGridKernelDealloc(MPCL_GridKernelData* self)
{
	MPCL_GridKernelFinal(self);
	self->ob_type->tp_free((PyObject*)self);
}

static PyObject *PyGridKernelNew(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	MPCL_GridKernelData *self;

	self = (MPCL_GridKernelData *)type->tp_alloc(type, 0);
	return (PyObject *)self;
}

static int PyGridKernelNewInit(MPCL_GridKernelData *self, PyObject *args, PyObject *kwds)
{
	MP_GridData *data;
	int platform_id;
	static char *kwlist[] = { "grid", "id", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oi", kwlist, &data, &platform_id)) {
		return -1;
	}
	MPCL_GridKernelInit(self, data, platform_id);
	return 0;
}

static PyMemberDef PyGridKernelMembers[] = {
	{ NULL }  /* Sentinel */
};

static PyObject *PyGridKernelSolve(MPCL_GridKernelData *self, PyObject *args, PyObject *kwds)
{
	MP_GridData *data;
	double dt;
	int nloop;
	static char *kwlist[] = { "grid", "dt", "nloop", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "Odi", kwlist, &data, &dt, &nloop)) {
		return NULL;
	}
	return Py_BuildValue("d", MPCL_GridKernelSolve(self, data, dt, nloop));
}

static PyMethodDef PyGridKernelMethods[] = {
	{ "solve", (PyCFunction)PyGridKernelSolve, METH_VARARGS | METH_KEYWORDS,
	"solve(grid, dt, nloop) : solve" },
	{ NULL }  /* Sentinel */
};

static PyTypeObject MPCLGridNewPyType = {
	PyObject_HEAD_INIT(NULL)
	0,							/*ob_size*/
	"MPCLGrid.new",				/*tp_name*/
	sizeof(MPCL_GridKernelData),/*tp_basicsize*/
	0,							/*tp_itemsize*/
	(destructor)PyGridKernelDealloc,	/*tp_dealloc*/
	0,							/*tp_print*/
	0,							/*tp_getattr*/
	0,							/*tp_setattr*/
	0,							/*tp_compare*/
	0,							/*tp_repr*/
	0,							/*tp_as_number*/
	0,							/*tp_as_sequence*/
	0,							/*tp_as_mapping*/
	0,							/*tp_hash */
	0,							/*tp_call*/
	0,							/*tp_str*/
	0,							/*tp_getattro*/
	0,							/*tp_setattro*/
	0,							/*tp_as_buffer*/
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,	/*tp_flags*/
	"new(grid, id)",			/* tp_doc */
	0,							/* tp_traverse */
	0,							/* tp_clear */
	0,							/* tp_richcompare */
	0,							/* tp_weaklistoffset */
	0,							/* tp_iter */
	0,							/* tp_iternext */
	PyGridKernelMethods,		/* tp_methods */
	PyGridKernelMembers,		/* tp_members */
	0,							/* tp_getset */
	0,							/* tp_base */
	0,							/* tp_dict */
	0,							/* tp_descr_get */
	0,							/* tp_descr_set */
	0,							/* tp_dictoffset */
	(initproc)PyGridKernelNewInit,	/* tp_init */
	0,							/* tp_alloc */
	PyGridKernelNew,			/* tp_new */
};

static PyObject *PyGridPlatformNum(PyObject *self)
{
	cl_platform_id platforms[MPCL_PLATFORM_MAX];
	cl_uint nplatforms;
	cl_int status;

	status = clGetPlatformIDs(MPCL_PLATFORM_MAX, platforms, &nplatforms);
	if (status != CL_SUCCESS) {
		return Py_BuildValue("si", "clGetPlatformIDs failed", status);
	}
	return Py_BuildValue("i", nplatforms);
}

static PyObject *PyGridPlatformInfo(PyObject *self, PyObject *args, PyObject *kwds)
{	
	int id;
	static char *kwlist[] = { "id", NULL };
	cl_platform_id platforms[MPCL_PLATFORM_MAX];
	cl_uint nplatforms;
	cl_int status;
	char profile[256], version[256], name[256], vendor[256], extensions[256];

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "i", kwlist, &id)) {
		return NULL;
	}
	status = clGetPlatformIDs(MPCL_PLATFORM_MAX, platforms, &nplatforms);
	if (status != CL_SUCCESS) {
		return Py_BuildValue("si", "clGetPlatformIDs failed", status);
	}
	clGetPlatformInfo(platforms[id], CL_PLATFORM_PROFILE, sizeof(profile)-1, profile, NULL);
	clGetPlatformInfo(platforms[id], CL_PLATFORM_VERSION, sizeof(version)-1, version, NULL);
	clGetPlatformInfo(platforms[id], CL_PLATFORM_NAME, sizeof(name)-1, name, NULL);
	clGetPlatformInfo(platforms[id], CL_PLATFORM_VENDOR, sizeof(vendor)-1, vendor, NULL);
	clGetPlatformInfo(platforms[id], CL_PLATFORM_EXTENSIONS, sizeof(extensions)-1, extensions, NULL);
	return Py_BuildValue("sssss", profile, version, name, vendor, extensions);
}

static PyMethodDef MPCLGridPyMethods[] = {
	{ "platform_num", (PyCFunction)PyGridPlatformNum, METH_NOARGS,
	"platform_num() : number of platform" },
	{ "platform_info", (PyCFunction)PyGridPlatformInfo, METH_VARARGS | METH_KEYWORDS,
	"platform_info(id) : platform information" },
	{ NULL }  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC initMPCLGrid(void)
{
	PyObject *m;

	if (PyType_Ready(&MPCLGridNewPyType) < 0) return;
	m = Py_InitModule3("MPCLGrid", MPCLGridPyMethods, "MPCLGrid extention");
	if (m == NULL) return;
	Py_INCREF(&MPCLGridNewPyType);
	PyModule_AddObject(m, "new", (PyObject *)&MPCLGridNewPyType);
}

#endif /* _DEBUG */