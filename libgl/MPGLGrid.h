#ifndef _MPGLGRID_H
#define _MPGLGRID_H

#ifdef __cplusplus
extern "C" {
#endif

#ifndef FALSE
#define FALSE 0
#endif
#ifndef TRUE
#define TRUE 1
#endif
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

#ifndef _MPGRID_H
#include <MPGrid.h>
#endif

#include <GL/gl.h>
#include <GL/glu.h>

/*--------------------------------------------------
  model typedef and functions
*/
typedef struct MPGL_Model {
#ifndef _DEBUG
	PyObject_HEAD
#endif
	float mat[4][4];
	float center[3];
	float scale;
	float mat_inv[4][4];
} MPGL_Model;

#ifndef _DEBUG
PyTypeObject MPGL_ModelPyType;
#endif

void MPGL_ModelInit(MPGL_Model *model);
void MPGL_ModelZoom(MPGL_Model *model, float s);
void MPGL_ModelTranslateZ(MPGL_Model *model, float mz);
void MPGL_ModelTranslateY(MPGL_Model *model, float my);
void MPGL_ModelTranslateX(MPGL_Model *model, float mx);
void MPGL_ModelRotateZ(MPGL_Model *model, float az);
void MPGL_ModelRotateY(MPGL_Model *model, float ay);
void MPGL_ModelRotateX(MPGL_Model *model, float ax);
void MPGL_ModelInverse(MPGL_Model *model);
void MPGL_ModelSetDirection(MPGL_Model *model, float dir[6]);
void MPGL_ModelGetDirection(MPGL_Model *model, float dir[6]);
void MPGL_ModelSetAngle(MPGL_Model *model, float angle[3]);
void MPGL_ModelGetAngle(MPGL_Model *model, float angle[3]);
void MPGL_ModelFitCenter(MPGL_Model *model, float region[]);
void MPGL_ModelFitScale(MPGL_Model *model, float region[], float aspect);
void MPGL_ModelTransform(MPGL_Model *model);

/*--------------------------------------------------
  text functions
*/
enum { MPGL_TextHelvetica10, MPGL_TextHelvetica12, MPGL_TextHelvetica18 };

void MPGL_TextBitmap(const char s[], int font_type);

/*--------------------------------------------------
  colormap typedef and functions
*/
#define MPGL_COLORMAP_MAX 16

enum { MPGL_ColormapStep, MPGL_ColormapGrad };

typedef struct MPGL_Colormap {
#ifndef _DEBUG
	PyObject_HEAD
#endif
	int mode;
	char title[32];
	int nstep;
	float step_color[MPGL_COLORMAP_MAX][3];
	char label[MPGL_COLORMAP_MAX][32];
	int ngrad;
	float grad_color[MPGL_COLORMAP_MAX][3];
	int nscale;
	double range[2];
	float size[2];
	int font_type;
	float font_color[3];
} MPGL_Colormap;

#ifndef _DEBUG
PyTypeObject MPGL_ColormapPyType;
#endif

void MPGL_ColormapInit(MPGL_Colormap *colormap);
void MPGL_ColormapColor(MPGL_Colormap *colormap);
void MPGL_ColormapGrayscale(MPGL_Colormap *colormap);
void MPGL_ColormapStepColor(MPGL_Colormap *colormap, int id, float color[]);
void MPGL_ColormapGradColor(MPGL_Colormap *colormap, double value, float color[]);
void MPGL_ColormapDraw(MPGL_Colormap *colormap);

/*--------------------------------------------------
  scene typedef and functions
*/
enum { MPGL_ProjFrustum, MPGL_ProjOrtho };

typedef struct MPGL_SceneAttr {
	short disp;
	float color[3];
	float width;
	int font;
} MPGL_SceneAttr;

typedef struct MPGL_SceneLight {
	float position[4];
	float specular[4];
	float diffuse[4];
	float ambient[4];
} MPGL_SceneLight;

typedef struct MPGL_Scene {
#ifndef _DEBUG
	PyObject_HEAD
#endif
	int proj;
	double znear, zfar;
	float lookat[9];
	float mat_specular[4];
	float mat_shininess;
	float mat_emission[4];
	float clear_color[4];
	int nlight;
	MPGL_SceneLight light[8];
} MPGL_Scene;

#ifndef _DEBUG
PyTypeObject MPGL_ScenePyType;
#endif

void MPGL_SceneInit(MPGL_Scene *scene);
MPGL_SceneLight *MPGL_SceneLightAdd(MPGL_Scene *scene, float x, float y, float z, float w);
void MPGL_SceneSetup(MPGL_Scene *scene);
void MPGL_SceneResize(MPGL_Scene *scene, int width, int height);

/*--------------------------------------------------
  grid functions
*/
#define MPGL_GRID_TYPE_MAX 256

#define MPGL_GRID_QUADS_LIST0 101
#define MPGL_GRID_QUADS_LIST1 102
#define MPGL_GRID_QUADS_LIST2 103
#define MPGL_GRID_QUADS_LIST3 104
#define MPGL_GRID_QUADS_LIST4 105
#define MPGL_GRID_QUADS_LIST5 106
#define MPGL_GRID_CUBE_LIST 107
#define MPGL_GRID_CYLINDER_LIST 108

enum { MPGL_DrawMethodQuads, MPGL_DrawMethodCubes };
enum { MPGL_DrawKindType, MPGL_DrawKindUpdate, MPGL_DrawKindVal, MPGL_DrawKindCx, MPGL_DrawKindCy, MPGL_DrawKindCz };

typedef struct MPGL_GridDrawData {
#ifndef _DEBUG
	PyObject_HEAD
#endif
	int method;
	int kind;
	int disp[MPGL_GRID_TYPE_MAX];
	int range[6];
} MPGL_GridDrawData;

#ifndef _DEBUG
PyTypeObject MPGL_GridDrawDataPyType;
#endif

void MPGL_GridDrawInit(MPGL_GridDrawData *draw);
void MPGL_GridDrawList(void);
void MPGL_GridDrawColormapRange(MPGL_GridDrawData *draw, MP_GridData *data, MPGL_Colormap *colormap);
void MPGL_GridDraw(MPGL_GridDrawData *draw, MP_GridData *data, MPGL_Colormap *colormap);
void MPGL_GridDrawAxis(int size[]);
void MPGL_GridDrawFit(MPGL_GridDrawData *draw, MP_GridData *data, int width, int height, MPGL_Model *model);

#ifdef __cplusplus
}
#endif

#endif /* _MPGLGRID_H */
