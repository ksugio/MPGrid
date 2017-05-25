#ifndef _DEBUG

#include "MPGLGrid.h"
#include <numpy/arrayobject.h>

static PyObject *FuncObj;

static void IdleFunc(void)
{
	PyObject_CallObject(FuncObj, NULL);
}

static PyObject *PyGridWindow(PyObject *self, PyObject *args, PyObject *kwds)
{
	MP_GridData *data;
	MPGL_GridDrawData *draw;
	MPGL_Colormap *cmp;
	MPGL_Scene *scene;
	MPGL_Model *model;
	int width, height;
	PyObject *func = NULL;
	static char *kwlist[] = { "grid", "draw", "cmp", "scene", "model", "width", "height", "func", NULL };
	int argc = 0;
	char *argv[1];

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO!O!O!O!ii|O", kwlist, &data, 
		&MPGL_GridDrawDataPyType, &draw, &MPGL_ColormapPyType, &cmp,
		&MPGL_ScenePyType, &scene, &MPGL_ModelPyType, &model, &width, &height,
		&PyTuple_Type, &func)) {
		return NULL;
	}
	if (func == NULL) {
		MPGL_GridWindow(data, draw, cmp, scene, model, width, height, NULL, argc, argv);
	}
	else {
		if (!PyCallable_Check(func)) {
			PyErr_SetString(PyExc_TypeError, "func must be callable");
			return NULL;
		}
		FuncObj = func;
		MPGL_GridWindow(data, draw, cmp, scene, model, width, height, IdleFunc, argc, argv);
	}
	Py_RETURN_NONE;
}

static PyObject *PyGridImage(PyObject *self, PyObject *args, PyObject *kwds)
{
	MP_GridData *data;
	MPGL_GridDrawData *draw;
	MPGL_Colormap *cmp;
	MPGL_Scene *scene;
	MPGL_Model *model;
	int width, height;
	static char *kwlist[] = { "grid", "draw", "cmp", "scene", "model", "width", "height", NULL };
	npy_intp dims[1];
	PyArrayObject *buffer_arr;
	unsigned char *buffer;
	int argc = 0;
	char *argv[1];

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO!O!O!O!ii", kwlist, &data, 
		&MPGL_GridDrawDataPyType, &draw, &MPGL_ColormapPyType, &cmp,
		&MPGL_ScenePyType, &scene, &MPGL_ModelPyType, &model, &width, &height)) {
		return NULL;
	}
	dims[0] = 3 * width * height;
	buffer_arr = (PyArrayObject *)PyArray_SimpleNew(1, dims, NPY_UBYTE);
	buffer = (unsigned char *)PyArray_DATA(buffer_arr);
	MPGL_GridImage(data, draw, cmp, scene, model, width, height, buffer, argc, argv);
	return (PyObject *)buffer_arr;
}

static PyObject *PyGridPostRedisplay(PyObject *self, PyObject *args)
{
	glutPostRedisplay();
	Py_RETURN_NONE;
}

static PyObject *PyGridTextBitmap(PyObject *self, PyObject *args, PyObject *kwds)
{
	const char *string;
	int font_type;
	static char *kwlist[] = { "string", "font_type", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "si", kwlist, &string, &font_type)) {
		return NULL;
	}
	MPGL_TextBitmap(string, font_type);
	Py_RETURN_NONE;
}

static PyMethodDef MPGLGridPyMethods[] = {
	{ "window", (PyCFunction)PyGridWindow, METH_VARARGS | METH_KEYWORDS,
	"window(grid, cmp, scene, model, kind, width, height, [range], [func]) : create window for grid data" },
	{ "image", (PyCFunction)PyGridImage, METH_VARARGS | METH_KEYWORDS,
	"image(grid, cmp, scene, model, kind, width, height, [range]) : create image for grid data" },
	{ "post_redisplay", (PyCFunction)PyGridPostRedisplay, METH_NOARGS,
	"post_redisplay() : post_redisplay" },
	{ "text_bitmap", (PyCFunction)PyGridTextBitmap, METH_VARARGS | METH_KEYWORDS,
	"text_bitmap(string, font_type) : draw text" },
	{ NULL }  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC initMPGLGrid(void)
{
	PyObject *m;

	if (PyType_Ready(&MPGL_GridDrawDataPyType) < 0) return;
	if (PyType_Ready(&MPGL_ModelPyType) < 0) return;
	if (PyType_Ready(&MPGL_ColormapPyType) < 0) return;
	if (PyType_Ready(&MPGL_ScenePyType) < 0) return;
	m = Py_InitModule3("MPGLGrid", MPGLGridPyMethods, "MPGLGrid extention");
	if (m == NULL) return;
	import_array();
	Py_INCREF(&MPGL_GridDrawDataPyType);
	PyModule_AddObject(m, "draw", (PyObject *)&MPGL_GridDrawDataPyType);
	Py_INCREF(&MPGL_ModelPyType);
	PyModule_AddObject(m, "model", (PyObject *)&MPGL_ModelPyType);
	Py_INCREF(&MPGL_ColormapPyType);
	PyModule_AddObject(m, "colormap", (PyObject *)&MPGL_ColormapPyType);
	Py_INCREF(&MPGL_ScenePyType);
	PyModule_AddObject(m, "scene", (PyObject *)&MPGL_ScenePyType);
}

#endif /* _DEBUG */