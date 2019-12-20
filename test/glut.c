#include <MPGLGrid.h>
#include <GL/freeglut.h>

static MP_GridData *Data;
static MPGL_GridDrawData Draw;
static MPGL_Colormap Colormap;
static MPGL_Scene Scene;
static MPGL_Model Model;

static void DisplayFunc(void)
{
	char s[32];

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	/* grid draw */
	glPushMatrix();
	MPGL_ModelTransform(&Model);
	MPGL_GridDraw(&Draw, Data, &Colormap);
	glTranslatef(-2.0f, -2.0f, -2.0f);
	MPGL_GridDrawAxis(Data->size);
	glPopMatrix();
	/* colormap draw */
	glPushMatrix();
	glRotated(90.0, 0.0, 0.0, 1.0);
	glRotated(90.0, 1.0, 0.0, 0.0);
	glTranslated((2.0 - Scene.width) / Scene.height, -Colormap.size[1] / 2, Scene.znear - 1.0e-6);
	MPGL_ColormapDraw(&Colormap);
	glPopMatrix();
	/* step */
	glPushAttrib(GL_LIGHTING_BIT);
	glDisable(GL_LIGHTING);
	sprintf(s, "%d step", Data->step);
	MPGL_SceneFrontText(&Scene, 10, 20, s, Colormap.font_type);
	glPopAttrib();
	glutSwapBuffers();
}

static void ReshapeFunc(int width, int height)
{
	MPGL_SceneResize(&Scene, width, height);
}

static void MouseFunc(int button, int state, int x, int y)
{
	if (button == GLUT_LEFT_BUTTON) {
		if (state == GLUT_DOWN) {
			MPGL_ModelButton(&Model, x, y, TRUE);
		}
		else if (state == GLUT_UP) {
			MPGL_ModelButton(&Model, x, y, FALSE);
		}
	}
}

static void MotionFunc(int x, int y)
{
	int ctrl;

	if (glutGetModifiers() == GLUT_ACTIVE_CTRL) ctrl = TRUE;
	else ctrl = FALSE;
	if (MPGL_ModelMotion(&Model, &Scene, x, y, ctrl)) {
		glutPostRedisplay();
	}
}

static void SubMenu1(int value)
{
	if (value == 1) Model.button_mode = MPGL_ModelModeRotate;
	else if (value == 2) Model.button_mode = MPGL_ModelModeTranslate;
	else if (value == 3) Model.button_mode = MPGL_ModelModeZoom;
}

static void SubMenu2(int value)
{
	if (value == 1) {
		MPGL_ModelFit(&Model);
		glutPostRedisplay();
	}
	else if (value == 2) {
		MPGL_ModelReset(&Model);
		glutPostRedisplay();
	}
}

static void SubMenu3(int value)
{
	if (value == 1) Draw.kind  = MPGL_DrawKindType;
	else if (value == 2) Draw.kind = MPGL_DrawKindUpdate;
	else if (value == 3) {
		Draw.kind = MPGL_DrawKindVal;
		MPGL_GridDrawColormapRange(&Draw, Data, &Colormap);
	}
	else if (value == 4) {
		Draw.kind = MPGL_DrawKindCx;
		MPGL_GridDrawColormapRange(&Draw, Data, &Colormap);
	}
	else if (value == 5) {
		Draw.kind = MPGL_DrawKindCy;
		MPGL_GridDrawColormapRange(&Draw, Data, &Colormap);
	}
	else if (value == 6) {
		Draw.kind = MPGL_DrawKindCz;
		MPGL_GridDrawColormapRange(&Draw, Data, &Colormap);
	}
	glutPostRedisplay();
}

void GlutWindow(MP_GridData *data, int width, int height, int argc, char** argv)
{
	int sub1, sub2, sub3;
	float init_dir[] = { 0.0, 0.0, 1.0, 0.0, 1.0, 0.0 };
	float region[6];

	glutInit(&argc, argv);
	glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH);
	glutInitWindowSize(width, height);
	glutCreateWindow("MPGL_GridWindow");
	glutDisplayFunc(DisplayFunc);
	glutReshapeFunc(ReshapeFunc);
	glutMouseFunc(MouseFunc);
	glutMotionFunc(MotionFunc);
	MPGL_GridDrawInit(&Draw);
	MPGL_ColormapInit(&Colormap);
	MPGL_SceneInit(&Scene);
	MPGL_SceneSetup(&Scene);
	MPGL_GridDrawRegion(&Draw, data, region);
	MPGL_ModelInit(&Model, init_dir, region);
	MPGL_GridDrawList();
	Data = data;
	// menu
	sub1 = glutCreateMenu(SubMenu1);
	glutAddMenuEntry("Rotate", 1);
	glutAddMenuEntry("Translate", 2);
	glutAddMenuEntry("Zoom", 3);
	sub2 = glutCreateMenu(SubMenu2);
	glutAddMenuEntry("Fit", 1);
	glutAddMenuEntry("Reset", 2);
	sub3 = glutCreateMenu(SubMenu3);
	glutAddMenuEntry("Type", 1);
	glutAddMenuEntry("Update", 2);
	glutAddMenuEntry("Value", 3);
	glutAddMenuEntry("Cx", 4);
	glutAddMenuEntry("Cy", 5);
	glutAddMenuEntry("Cz", 6);
	glutCreateMenu(NULL);
	glutAddSubMenu("Mouse", sub1);
	glutAddSubMenu("Model", sub2);
	glutAddSubMenu("Kind", sub3);
	glutAttachMenu(GLUT_RIGHT_BUTTON);
	// main loop
	glutMainLoop();
}
