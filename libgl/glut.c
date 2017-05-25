#include "MPGLGrid.h"

enum { ButtonUp, LButtonDown, RButtonDown };
enum { MotionRotate, MotionTranslate, MotionZoom };

static MP_GridData *Data;
static MPGL_GridDrawData *Draw;
static MPGL_Colormap *Colormap;
static MPGL_Scene *Scene;
static MPGL_Model *Model;
static unsigned char *CaptureBuffer;

static int ButtonState = ButtonUp;
static int Motion = MotionRotate;
static int MotionX, MotionY;
static int Width, Height;

static void DisplayFunc(void)
{
	char s[32];

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	/* grid draw */
	glPushMatrix();
	MPGL_ModelTransform(Model);
	MPGL_GridDraw(Draw, Data, Colormap);
	glTranslatef(-2.0f, -2.0f, -2.0f);
	MPGL_GridDrawAxis(Data->size);
	glPopMatrix();
	/* colormap draw */
	glPushMatrix();
	glTranslated((2.0 - Width) / Height, -Colormap->size[1] / 2, Scene->znear - 1.0e-6);
	MPGL_ColormapDraw(Colormap);
	glPopMatrix();
	/* step */
	sprintf(s, "%d step", Data->step);
	glPushAttrib(GL_LIGHTING_BIT);
	glDisable(GL_LIGHTING);
	glRasterPos3d((2.0 * 10 - Width) / Height, 2.0*(Height - 20) / Height - 1.0, Scene->znear - 1.0e-6);
	glColor3fv(Colormap->font_color);
	MPGL_TextBitmap(s, Colormap->font_type);
	glPopAttrib();
	glutSwapBuffers();
}

static void ReshapeFunc(int width, int height)
{
	Width = width, Height = height;
	MPGL_SceneResize(Scene, Width, Height);
}

static void MouseFunc(int button, int state, int x, int y)
{
	if (button ==  GLUT_LEFT_BUTTON) {
		if (state == GLUT_DOWN) {
			ButtonState = LButtonDown;
			MotionX = x;
			MotionY = y;
		}
		else if (state == GLUT_UP) {
			MPGL_ModelInverse(Model);
			ButtonState = ButtonUp;
		}
	}	
}

static void MotionFunc(int x, int y)
{
	int w, h;
	int dx, dy;
	int cx, cy;
	float ax, ay, az;
	float mx, my, mz;
	float s;

	if (ButtonState == LButtonDown) {
		w = Width, h = Height;
		dx = x - MotionX;
		dy = y - MotionY;
		if (Motion == MotionRotate) {
			if (glutGetModifiers() == GLUT_ACTIVE_CTRL) {
				cx = w / 2, cy = h / 2;
				if (x <= cx && y <= cy) az = (float)M_PI * (-dx + dy) / h;
				else if (x > cx && y <= cy) az = (float)M_PI * (-dx - dy) / h;
				else if (x <= cx && y > cy) az = (float)M_PI * (dx + dy) / h;
				else if (x > cx && y > cy) az = (float)M_PI * (dx - dy) / h;
				MPGL_ModelRotateZ(Model, -az);
			}
			else {
				ay = (float)M_PI * dx / h;
				MPGL_ModelRotateY(Model, -ay);
				ax = (float)M_PI * dy / h;
				MPGL_ModelRotateX(Model, -ax);
			}
		}
		else if (Motion == MotionTranslate) {
			if (glutGetModifiers() == GLUT_ACTIVE_CTRL) {
				mz = 2 * (float)dy / h;
				MPGL_ModelTranslateZ(Model, -mz);
			}
			else {
				mx = 2 * (float)dx / h;
				MPGL_ModelTranslateX(Model, mx);
				my = 2 * (float)dy / h;
				MPGL_ModelTranslateY(Model, -my);
			}
		}
		else if (Motion == MotionZoom) {
			s = 1 - (float)dy / h;
			MPGL_ModelZoom(Model, s);
		}
		MotionX = x;
		MotionY = y;
		glutPostRedisplay();
	}
}

static void SubMenu1(int value)
{
	if (value == 1) Motion = MotionRotate;
	else if (value == 2) Motion = MotionTranslate;
	else if (value == 3) Motion = MotionZoom;
}

static void SubMenu2(int value)
{
	if (value == 1) {
		MPGL_GridDrawFit(Draw, Data, Width, Height, Model);
		glutPostRedisplay();
	}
	else if (value == 2) {
		MPGL_ModelInit(Model);
		glutPostRedisplay();
	}
}

static void SubMenu3(int value)
{
	if (value == 1) Draw->kind  = MP_GridKindType;
	else if (value == 2) Draw->kind = MP_GridKindUpdate;
	else if (value == 3) Draw->kind = MP_GridKindVal;
	glutPostRedisplay();
}

void MPGL_GridWindow(MP_GridData *data, MPGL_GridDrawData *draw,
	MPGL_Colormap *colormap, MPGL_Scene *scene, MPGL_Model *model,
	int width, int height, void(*func)(void), int argc, char **argv)
{
	int sub1, sub2, sub3;

	glutInit(&argc, argv);
	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
	glutInitWindowSize(width, height);
	glutCreateWindow("MPGL_GridWindow");
	glutDisplayFunc(DisplayFunc);
	glutReshapeFunc(ReshapeFunc);
	glutMouseFunc(MouseFunc);
	glutMotionFunc(MotionFunc);
	if (func != NULL) glutIdleFunc(func);
	MPGL_SceneSetup(scene);
	MPGL_GridDrawList();
	// menu
	sub1 = glutCreateMenu(SubMenu1);
	glutAddMenuEntry("Rotate", 1);
	glutAddMenuEntry("Translate", 2);
	glutAddMenuEntry("Zoom", 3);
	sub2 = glutCreateMenu(SubMenu2);
	glutAddMenuEntry("Fit", 1);
	glutAddMenuEntry("Init", 2);
	sub3 = glutCreateMenu(SubMenu3);
	glutAddMenuEntry("Type", 1);
	glutAddMenuEntry("Updata", 2);
	glutAddMenuEntry("Value", 3);
	glutCreateMenu(NULL);
	glutAddSubMenu("Mouse", sub1);
	glutAddSubMenu("Transform", sub2);
	glutAddSubMenu("Kind", sub3);
	glutAttachMenu(GLUT_RIGHT_BUTTON);
	// main loop
	Data = data;
	Draw = draw;
	Colormap = colormap;
	Scene = scene;
	Model = model;
	glutMainLoop();
}

void CaptureFunc(void)
{
	glReadPixels(0, 0, Width, Height, GL_RGB, GL_UNSIGNED_BYTE, CaptureBuffer);
	glutLeaveMainLoop();
}

void MPGL_GridImage(MP_GridData *data, MPGL_GridDrawData *draw,
	MPGL_Colormap *colormap, MPGL_Scene *scene, MPGL_Model *model,
	int width, int height, unsigned char *buffer, int argc, char **argv)
{
	glutInit(&argc, argv);
	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
	glutInitWindowSize(width, height);
	glutCreateWindow("MPGL_GridImage");
	glutDisplayFunc(DisplayFunc);
	glutReshapeFunc(ReshapeFunc);
	glutIdleFunc(CaptureFunc);
	MPGL_SceneSetup(scene);
	MPGL_GridDrawList();
	// set pointer
	Data = data;
	Draw = draw;
	Colormap = colormap;
	Scene = scene;
	Model = model;
	CaptureBuffer = buffer;
	// main loop
	glutMainLoop();
}
