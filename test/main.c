#include <MPGrid.h>
#include <MPCLGrid.h>

void GlutWindow(MP_GridData* data, int width, int height, int argc, char** argv);

void GridAl(MP_GridData *data)
{
	MP_GridAlloc(data, 100, 100, 1, 1, FALSE);
	MP_GridFillUpdate(data, 0, 0, 0, 0, 0, 99, 0);
	MP_GridFillUpdate(data, 0, 99, 0, 0, 99, 99, 0);
	MP_GridFillVal(data, 300.0, 1, 0, 0, 99, 99, 0);
	MP_GridFillVal(data, 300.0 + 10.0, 0, 0, 0, 0, 99, 0);
	data->element[0] = 1.0e-4;
	data->element[1] = 1.0e-4;
	data->element[2] = 1.0e-4;
	MP_GridSetCoef1(data, 236.0, 0, 0);
	data->rhoc[0] = 2465.1;
}

void GridAl10C(MP_GridData *data)
{
	// Calculated ETC 2.591297e2
	double lam_al[] = { 236.0, 236.0, 236.0 };
	double lam_c[] = { 1200.0, 1200.0, 1200.0 };
	double lam_al_c[] = { 394.4289694, 394.4289694, 394.4289694 };

	MP_GridAlloc(data, 100, 10, 20, 2, TRUE);
	MP_GridFillUpdate(data, 0, 0, 0, 0, 0, 9, 19);
	MP_GridFillUpdate(data, 0, 99, 0, 0, 99, 9, 19);
	MP_GridFillType(data, 1, 44, 0, 0, 54, 9, 19);
	MP_GridFillVal(data, 300.0, 1, 0, 0, 99, 9, 19);
	MP_GridFillVal(data, 300.0 + 10.0, 0, 0, 0, 0, 9, 19);
	data->element[0] = 1.0e-4;
	data->element[1] = 1.0e-4;
	data->element[2] = 1.0e-4;
	MP_GridSetCoef3(data, lam_al, 0, 0);
	MP_GridSetCoef3(data, lam_al_c, 0, 1);
	MP_GridSetCoef3(data, lam_al_c, 1, 0);
	MP_GridSetCoef3(data, lam_c, 1, 1);
	MP_GridRefLocalCoef(data);
	data->rhoc[0] = 2465.1;
	data->rhoc[1] = 855.6;
}

void GridAl10CTrans(MP_GridData *data)
{
	// Calculated ETC 2.624888e2
	int inter_cond[] = { MP_GridInterCond, MP_GridInterCond, MP_GridInterCond };
	int inter_trans[] = { MP_GridInterTrans, MP_GridInterTrans, MP_GridInterTrans };
	double lam_al[] = { 236.0, 236.0, 236.0 };
	double lam_c[] = { 1200.0, 1200.0, 1200.0 };
	double h_al_c[] = { 110113846.7, 110113846.7, 110113846.7 };

	MP_GridAlloc(data, 100, 100, 1, 2, FALSE);
	MP_GridFillUpdate(data, 0, 0, 0, 0, 0, 99, 0);
	MP_GridFillUpdate(data, 0, 99, 0, 0, 99, 99, 0);
	MP_GridFillType(data, 1, 44, 0, 0, 54, 99, 0);
	MP_GridFillVal(data, 300.0, 1, 0, 0, 99, 99, 0);
	MP_GridFillVal(data, 300.0 + 10.0, 0, 0, 0, 0, 99, 0);
	data->element[0] = 1.0e-4;
	data->element[1] = 1.0e-4;
	data->element[2] = 1.0e-4;
	MP_GridSetInterCoef3(data, inter_cond, lam_al, 0, 0);
	MP_GridSetInterCoef3(data, inter_trans, h_al_c, 0, 1);
	MP_GridSetInterCoef3(data, inter_trans, h_al_c, 1, 0);
	MP_GridSetInterCoef3(data, inter_cond, lam_c, 1, 1);
	data->rhoc[0] = 2465.1;
	data->rhoc[1] = 855.6;
}

double CalSigma(MP_GridData* data)
{
	int id0, id1, cid;
	double v12, vlr, sigma;
	int nx = data->size[0];
	int ny = data->size[1];
	int nz = data->size[2];

	v12 = MP_GridAveVal(data, 1, 0, 0, 1, ny - 1, nz - 1)
		- MP_GridAveVal(data, 2, 0, 0, 2, ny - 1, nz - 1);
	vlr = MP_GridAveVal(data, 0, 0, 0, 0, ny - 1, nz - 1)
		- MP_GridAveVal(data, nx - 1, 0, 0, nx - 1, ny - 1, nz - 1);
	id0 = MP_GRID_INDEX(data, 1, 0, 0);
	id1 = MP_GRID_INDEX(data, 2, 0, 0);
	cid = MP_GRID_COEF_INDEX(data, data->type[id0], data->type[id1]);
	sigma = data->coef_x[cid] * v12 * (nx - 1) / vlr;
	return sigma;
}

void Solve(MP_GridData* data)
{
	double dt, findv, dv;

	dt = MP_GridEstimateDt(data, 1.0);
	findv = 1.0e-12;
	printf("Start size = %e, dt = %e, findv = %e\n", data->element[0], dt, findv);
	while (1) {
		dv = MP_GridSolve(data, dt, 10000);
		if (isnan(dv)) {
			printf("NaN appear\n");
			break;
		}
		printf("%d, %e, %e\n", data->step, dv, CalSigma(data));
		if (dv < findv) break;
	}
}

void SolveCL(MP_GridData* data)
{
	MPCL_GridKernelData gkd;
	double dt, findv, dv;

	MPCL_GridPlatformInfo();
	MPCL_GridKernelInit(&gkd, data, 0);
	dt = MP_GridEstimateDt(data, 1.0);
	findv = 1.0e-12;
	printf("Start size = %e, dt = %e, findv = %e\n", data->element[0], dt, findv);
	while (1) {
		dv = MPCL_GridKernelSolve(&gkd, data, dt, 10000);
		if (isnan(dv)) {
			printf("NaN appear\n");
			break;
		}
		printf("%d, %e, %e\n", data->step, dv, CalSigma(data));
		if (dv < findv) break;
	}
	MPCL_GridKernelFinal(&gkd);
}

main(int argc, char *argv[])
{
	MP_GridData data;

	//GridAl(&data);
	//GridAl10C(&data);
	GridAl10CTrans(&data);
	//Solve(&data);
	//SolveCL(&data);
	fprintf(stderr, "overall_coef_x %e\n", MP_GridOverallCoef(&data, 0, 1.0e7));
	fprintf(stderr, "overall_coef_y %e\n", MP_GridOverallCoef(&data, 1, 1.0e7));
	fprintf(stderr, "overall_coef_z %e\n", MP_GridOverallCoef(&data, 2, 1.0e7));
	GlutWindow(&data, 800, 600, argc, argv);
	MP_GridFree(&data);
}

