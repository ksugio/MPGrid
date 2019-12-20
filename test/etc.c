#include <MPGrid.h>


double CalETC(MP_GridData* data)
{
	int id0, id1, cid;
	double v12, vlr;
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
	return data->coef_x[cid] * v12 * (nx - 1) / vlr;
}

int main(int argc, char* argv[])
{
	int i, nloop;
	double dt, findv, dv;
	MP_GridData data;

	if (argc != 6) {
		fprintf(stderr, "etc [in_file] [nloop] [dt] [findv] [out_file] : calculate ETC in X dir. if dt <= 0, estimate dt.\n");
		return 0;
	}
	if (!MP_GridRead(&data, argv[1], 2)) {
		return 0;
	}
	nloop = atoi(argv[2]);
	if (atof(argv[3]) <= 0.0) {
		dt = MP_GridEstimateDt(&data, 1.0);
	}
	else {
		dt = atof(argv[3]);
	}
	findv = atof(argv[4]);
	printf("file = %s, nloop = %d, dt = %e, findv = %e\n", argv[1], nloop, dt, findv);
	printf("step, dv, mean_flow, ETC\n");
	while (1) {
		dv = MP_GridSolve(&data, dt, nloop);
		if (isnan(dv)) {
			printf("NaN appear\n");
			break;
		}
		printf("%d, %e, %e, %e\n", data.step, dv, MP_GridMeanFlow(&data), CalETC(&data));
		if (dv < findv) break;
	}
	MP_GridWrite(&data, argv[5], 8);
	MP_GridFree(&data);
}