#include "MPGrid.h"
#include <time.h>

int MP_GridAlloc(MP_GridData *data, int nx, int ny, int nz, int ntype)
{
	int ntot;
	int i;
	time_t timer;

	data->size[0] = nx, data->size[1] = ny, data->size[2] = nz;
	for (i = 0;i < 3;i++) data->element[i] = 1.0;
	ntot = data->ntot = nx * ny * nz;
	data->ntype = ntype;
	data->type = (short *) malloc(ntot*sizeof(short));
	data->update = (short *) malloc(ntot*sizeof(short));
	data->val = (double *)malloc(ntot*sizeof(double));
	data->buf = (double *)malloc(ntot*sizeof(double));
	data->inter_x = (int *)malloc(ntype*ntype*sizeof(int));
	data->inter_y = (int *)malloc(ntype*ntype*sizeof(int));
	data->inter_z = (int *)malloc(ntype*ntype*sizeof(int));
	data->coef_x = (double *)malloc(ntype*ntype*sizeof(double));
	data->coef_y = (double *)malloc(ntype*ntype*sizeof(double));
	data->coef_z = (double *)malloc(ntype*ntype*sizeof(double));
	data->rhoc = (double *)malloc(ntype*sizeof(double));
	if (data->type == NULL || data->update == NULL || data->val == NULL || data->buf == NULL
		|| data->inter_x == NULL || data->inter_y == NULL || data->inter_z == NULL
		|| data->coef_x == NULL || data->coef_y == NULL || data->coef_z == NULL
		|| data->rhoc == NULL) return FALSE;
	for (i = 0; i < ntot; i++) {
		data->type[i] = 0;
		data->update[i] = TRUE;
		data->val[i] = 0.0;
		data->buf[i] = 0.0;
	}
	for (i = 0; i < ntype*ntype; i++) {
		data->inter_x[i] = MP_GridInterCond;
		data->inter_y[i] = MP_GridInterCond;
		data->inter_z[i] = MP_GridInterCond;
		data->coef_x[i] = 0.0;
		data->coef_y[i] = 0.0;
		data->coef_z[i] = 0.0;
	}
	for (i = 0; i < ntype; i++) {
		data->rhoc[i] = 1.0;
	}
	for (i = 0;i < 6;i++) data->bound[i] = MP_GridBoundInsulate;
	data->step = 0;
	data->rand_seed = (long)time(&timer);
	return TRUE;
}

void MP_GridFree(MP_GridData *data)
{
	free(data->type);
	free(data->update);
	free(data->val);
	free(data->buf);
	free(data->inter_x);
	free(data->inter_y);
	free(data->inter_z);
	free(data->coef_x);
	free(data->coef_y);
	free(data->coef_z);
	free(data->rhoc);
}

static void GridElementFlow(MP_GridData *data, int x, int y, int z, double dt)
{
	double xl, xu, yl, yu, zl, zu;
	double f;
	double dx, dy, dz;
	int nx, ny, nz;
	int id0, id1;
	int cid;

	id0 = MP_GRID_INDEX(data, x, y, z);
	if (id0 > data->ntot || !data->update[id0]) return;
	nx = data->size[0], ny = data->size[1], nz = data->size[2];
	dx = data->element[0], dy = data->element[1], dz = data->element[2];
	// x lower
	if (x == 0) {
		if (data->bound[0] == MP_GridBoundInsulate) xl = 0.0;
		else {
			id1 = MP_GRID_INDEX(data, nx-1, y, z);
			cid = MP_GRID_COEF_INDEX(data, data->type[id0], data->type[id1]);
			if (data->inter_x[cid] == MP_GridInterCond) xl = data->coef_x[cid]*(data->val[id0]-data->val[id1])/dx;
			else if (data->inter_x[cid] == MP_GridInterTrans) xl = data->coef_x[cid]*(data->val[id0]-data->val[id1]);
		}
	}
	else {
		id1 = MP_GRID_INDEX(data, x-1, y, z);
		cid = MP_GRID_COEF_INDEX(data, data->type[id0], data->type[id1]);
		if (data->inter_x[cid] == MP_GridInterCond) xl = data->coef_x[cid]*(data->val[id0]-data->val[id1])/dx;
		else if (data->inter_x[cid] == MP_GridInterTrans) xl = data->coef_x[cid]*(data->val[id0]-data->val[id1]);
	}
	// x upper
	if (x == nx-1) {
		if (data->bound[3] == MP_GridBoundInsulate) xu = 0.0;
		else {
			id1 = MP_GRID_INDEX(data, 0, y, z);
			cid = MP_GRID_COEF_INDEX(data, data->type[id1], data->type[id0]);
			if (data->inter_x[cid] == MP_GridInterCond) xu = data->coef_x[cid]*(data->val[id1]-data->val[id0])/dx;
			else if (data->inter_x[cid] == MP_GridInterTrans)	xu = data->coef_x[cid]*(data->val[id1]-data->val[id0]);
		}
	}
	else {
		id1 = MP_GRID_INDEX(data, x+1, y, z);
		cid = MP_GRID_COEF_INDEX(data, data->type[id1], data->type[id0]);
		if (data->inter_x[cid] == MP_GridInterCond) xu = data->coef_x[cid]*(data->val[id1]-data->val[id0])/dx;
		else if (data->inter_x[cid] == MP_GridInterTrans) xu = data->coef_x[cid]*(data->val[id1]-data->val[id0]);
	}
	// y lower
	if (y == 0) {
		if (data->bound[1] == MP_GridBoundInsulate) yl = 0.0;
		else {
			id1 = MP_GRID_INDEX(data, x, ny-1, z);
			cid = MP_GRID_COEF_INDEX(data, data->type[id0], data->type[id1]);
			if (data->inter_y[cid] == MP_GridInterCond) yl = data->coef_y[cid]*(data->val[id0]-data->val[id1])/dy;
			else if (data->inter_y[cid] == MP_GridInterTrans) yl = data->coef_y[cid]*(data->val[id0]-data->val[id1]);
		}
	}
	else {
		id1 = MP_GRID_INDEX(data, x, y-1, z);
		cid = MP_GRID_COEF_INDEX(data, data->type[id0], data->type[id1]);
		if (data->inter_y[cid] == MP_GridInterCond) yl = data->coef_y[cid]*(data->val[id0]-data->val[id1])/dy;
		else if (data->inter_y[cid] == MP_GridInterTrans) yl = data->coef_y[cid]*(data->val[id0]-data->val[id1]);
	}
	// y upper
	if (y == ny-1) {
		if (data->bound[4] == MP_GridBoundInsulate) yu = 0.0;
		else {
			id1 = MP_GRID_INDEX(data, x, 0, z);
			cid = MP_GRID_COEF_INDEX(data, data->type[id1], data->type[id0]);
			if (data->inter_y[cid] == MP_GridInterCond) yu = data->coef_y[cid]*(data->val[id1]-data->val[id0])/dy;
			else if (data->inter_y[cid] == MP_GridInterTrans) yu = data->coef_y[cid]*(data->val[id1]-data->val[id0]);
		}
	}
	else {
		id1 = MP_GRID_INDEX(data, x, y+1, z);
		cid = MP_GRID_COEF_INDEX(data, data->type[id1], data->type[id0]);
		if (data->inter_y[cid] == MP_GridInterCond) yu = data->coef_y[cid]*(data->val[id1]-data->val[id0])/dy;
		else if (data->inter_y[cid] == MP_GridInterTrans) yu = data->coef_y[cid]*(data->val[id1]-data->val[id0]);
	}
	// z lower
	if (z == 0) {
		if (data->bound[2] == MP_GridBoundInsulate) zl = 0.0;
		else {
			id1 = MP_GRID_INDEX(data, x, y, nz-1);
			cid = MP_GRID_COEF_INDEX(data, data->type[id0], data->type[id1]);
			if (data->inter_z[cid] == MP_GridInterCond) zl = data->coef_z[cid]*(data->val[id0]-data->val[id1])/dz;
			else if (data->inter_z[cid] == MP_GridInterTrans) zl = data->coef_z[cid]*(data->val[id0]-data->val[id1]);
		}
	}
	else {
		id1 = MP_GRID_INDEX(data, x, y, z-1);
		cid = MP_GRID_COEF_INDEX(data, data->type[id0], data->type[id1]);
		if (data->inter_z[cid] == MP_GridInterCond) zl = data->coef_z[cid]*(data->val[id0]-data->val[id1])/dz;
		else if (data->inter_z[cid] == MP_GridInterTrans) zl = data->coef_z[cid]*(data->val[id0]-data->val[id1]);
	}
	// z upper
	if (z == nz-1) {
		if (data->bound[5] == MP_GridBoundInsulate) zu = 0.0;
		else {
			id1 = MP_GRID_INDEX(data, x, y, 0);
			cid = MP_GRID_COEF_INDEX(data, data->type[id1], data->type[id0]);
			if (data->inter_z[cid] == MP_GridInterCond) zu = data->coef_z[cid]*(data->val[id1]-data->val[id0])/dz;
			else if (data->inter_z[cid] == MP_GridInterTrans) zu = data->coef_z[cid]*(data->val[id1]-data->val[id0]);
		}
	}
	else {
		id1 = MP_GRID_INDEX(data, x, y, z+1);
		cid = MP_GRID_COEF_INDEX(data, data->type[id1], data->type[id0]);
		if (data->inter_z[cid] == MP_GridInterCond) zu = data->coef_z[cid]*(data->val[id1]-data->val[id0])/dz;
		else if (data->inter_z[cid] == MP_GridInterTrans) zu = data->coef_z[cid]*(data->val[id1]-data->val[id0]);
	}
	f = ((xu - xl) / dx + (yu - yl) / dy + (zu - zl) / dz) / data->rhoc[data->type[id0]];
	data->buf[id0] = data->val[id0] + f*dt;
}

double MP_GridSolve(MP_GridData *data, double dt, int nloop)
{
	int x, y, z;
	double dvtot;
	int n = 0;
	int i;

	while (TRUE) {
		for (z = 0; z < data->size[2]; z++) {
			for (y = 0; y < data->size[1]; y++) {
				for (x = 0; x < data->size[0]; x++) {
					GridElementFlow(data, x, y, z, dt);
				}
			}
		}
		data->step++;
		if (++n >= nloop) {
			for (i = 0, dvtot = 0.0; i < data->ntot; i++) {
				if (data->update[i]) {
					dvtot += fabs(data->buf[i] - data->val[i]);
					data->val[i] = data->buf[i];
				}
			}
			break;
		}
		else {
			for (i = 0; i < data->ntot; i++) {
				if (data->update[i]) data->val[i] = data->buf[i];
			}
		}
	}
	return dvtot/data->ntot;
}

double MP_GridEstimateDt(MP_GridData *data, double ratio)
{
	int i, j;
	int cid;
	double f;
	double f_max = -1.0e32;
	double dt0, si, ji;
	int *ex = (int *)malloc(data->ntype*sizeof(int));

	for (i = 0; i < data->ntype; i++) ex[i] = 0;
	for (i = 0; i < data->ntype; i++) {
		for (j = 0; j < data->ntot; j++) {
			if (i == data->type[j]) {
				ex[i] = 1;
				break;
			}
		}
	}
	for (i = 0; i < data->ntype; i++) {
		if (ex[i]) {
			for (j = 0; j < data->ntype; j++) {
				if (ex[j]) {
					cid = MP_GRID_COEF_INDEX(data, i, j);
					// x
					if (data->inter_x[cid] == MP_GridInterCond) {
						f = data->coef_x[cid] / data->element[0] / data->element[0] / data->rhoc[i];
					}
					else if (data->inter_x[cid] == MP_GridInterTrans) {
						f = data->coef_x[cid] / data->element[0] / data->rhoc[i];
					}
					if (f > f_max) f_max = f;
					// y
					if (data->inter_y[cid] == MP_GridInterCond) {
						f = data->coef_y[cid] / data->element[1] / data->element[1] / data->rhoc[i];
					}
					else if (data->inter_y[cid] == MP_GridInterTrans) {
						f = data->coef_y[cid] / data->element[1] / data->rhoc[i];
					}
					if (f > f_max) f_max = f;
					// z
					if (data->inter_z[cid] == MP_GridInterCond) {
						f = data->coef_z[cid] / data->element[2] / data->element[2] / data->rhoc[i];
					}
					else if (data->inter_z[cid] == MP_GridInterTrans) {
						f = data->coef_z[cid] / data->element[2] / data->rhoc[i];
					}
					if (f > f_max) f_max = f;
				}
			}
		}
	}
	free(ex);
	dt0 = 1.0 / (2.0 * ratio * f_max);
	si = pow(10.0, floor(log10(dt0)));
	ji = floor(dt0 / si);
	return ji*si;
}

void MP_GridSetInter1(MP_GridData *data, int inter, int i, int j)
{
	int id = MP_GRID_COEF_INDEX(data, i, j);

	if (id >= 0 && id < data->ntype*data->ntype) {
		data->inter_x[id] = inter;
		data->inter_y[id] = inter;
		data->inter_z[id] = inter;
	}
}

void MP_GridSetInter3(MP_GridData *data, int inter[], int i, int j)
{
	int id = MP_GRID_COEF_INDEX(data, i, j);

	if (id >= 0 && id < data->ntype*data->ntype) {
		data->inter_x[id] = inter[0];
		data->inter_y[id] = inter[1];
		data->inter_z[id] = inter[2];
	}
}

void MP_GridSetCoef1(MP_GridData *data, double coef, int i, int j)
{
	int id = MP_GRID_COEF_INDEX(data, i, j);

	if (id >= 0 && id < data->ntype*data->ntype) {
		data->coef_x[id] = coef;
		data->coef_y[id] = coef;
		data->coef_z[id] = coef;
	}
}

void MP_GridSetCoef3(MP_GridData *data, double coef[], int i, int j)
{
	int id = MP_GRID_COEF_INDEX(data, i, j);
	
	if (id >= 0 && id < data->ntype*data->ntype) {
		data->coef_x[id] = coef[0];
		data->coef_y[id] = coef[1];
		data->coef_z[id] = coef[2];
	}
}

void MP_GridSetInterCoef1(MP_GridData *data, int inter, double coef, int i, int j)
{
	int id = MP_GRID_COEF_INDEX(data, i, j);

	if (id >= 0 && id < data->ntype*data->ntype) {
		data->inter_x[id] = inter;
		data->inter_y[id] = inter;
		data->inter_z[id] = inter;
		data->coef_x[id] = coef;
		data->coef_y[id] = coef;
		data->coef_z[id] = coef;
	}
}

void MP_GridSetInterCoef3(MP_GridData *data, int inter[], double coef[], int i, int j)
{
	int id = MP_GRID_COEF_INDEX(data, i, j);

	if (id >= 0 && id < data->ntype*data->ntype) {
		data->inter_x[id] = inter[0];
		data->inter_y[id] = inter[1];
		data->inter_z[id] = inter[2];
		data->coef_x[id] = coef[0];
		data->coef_y[id] = coef[1];
		data->coef_z[id] = coef[2];
	}
}

int MP_GridFillType(MP_GridData *data, short type,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int x, y, z, id;
	int count = 0;

	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot) {
					data->type[id] = type;
					count++;
				}
			}
		}
	}
	return count;
}

int MP_GridFillUpdate(MP_GridData *data, short update,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int x, y, z, id;
	int count = 0;

	for (z = z0;z <= z1;z++) {
		for (y = y0;y <= y1;y++) {
			for (x = x0;x <= x1;x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot) {
					data->update[id] = update;
					count++;
				}
			}
		}
	}
	return count;
}

int MP_GridFillVal(MP_GridData *data, double val,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int x, y, z, id;
	int count = 0;

	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot) {
					data->val[id] = val;
					count++;
				}
			}
		}
	}
	return count;
}

static void ShapeData(int x0, int y0, int z0, int x1, int y1, int z1, double margin, double shape[])
{
	shape[0] = (x0 + x1) / 2.0;
	shape[1] = (y0 + y1) / 2.0;
	shape[2] = (z0 + z1) / 2.0;
	shape[3] = (x1 - x0) / 2.0 + margin;
	shape[4] = (y1 - y0) / 2.0 + margin;
	shape[5] = (z1 - z0) / 2.0 + margin;
}

static int EllipsoidCheck(MP_GridData *data, int x, int y, int z, double shape[])
{
	double dx, dy, dz, dr;

	dx = (double)x - shape[0];
	dy = (double)y - shape[1];
	dz = (double)z - shape[2];
	dr = dx*dx / (shape[3]*shape[3]) + dy*dy / (shape[4]*shape[4]) + dz*dz / (shape[5]*shape[5]);
	if (dr < 1.0) {
		return TRUE;
	}
	return FALSE;
}

int MP_GridEllipsoidType(MP_GridData *data, short type,
	int x0, int y0, int z0, int x1, int y1, int z1, double margin)
{
	double shape[6];
	int x, y, z, id;
	int count = 0;

	ShapeData(x0, y0, z0, x1, y1, z1, margin, shape);
	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot && EllipsoidCheck(data, x, y, z, shape)) {
					data->type[id] = type;
					count++;
				}
			}
		}
	}
	return count;
}

int MP_GridEllipsoidUpdate(MP_GridData *data, short update,
	int x0, int y0, int z0, int x1, int y1, int z1, double margin)
{
	double shape[6];
	int x, y, z, id;
	int count = 0;

	ShapeData(x0, y0, z0, x1, y1, z1, margin, shape);
	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot && EllipsoidCheck(data, x, y, z, shape)) {
					data->update[id] = update;
					count++;
				}
			}
		}
	}
	return count;
}

int MP_GridEllipsoidVal(MP_GridData *data, double val,
	int x0, int y0, int z0, int x1, int y1, int z1, double margin)
{
	double shape[6];
	int x, y, z, id;
	int count = 0;

	ShapeData(x0, y0, z0, x1, y1, z1, margin, shape);
	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot && EllipsoidCheck(data, x, y, z, shape)) {
					data->val[id] = val;
					count++;
				}
			}
		}
	}
	return count;
}

static int CylinderCheck(MP_GridData *data, int x, int y, int z, int dir, double shape[])
{
	double dx, dy, dz, dr;

	dx = (double)x - shape[0];
	dy = (double)y - shape[1];
	dz = (double)z - shape[2];
	if (dir == 0) {
		dr = dy*dy / (shape[4] * shape[4]) + dz*dz / (shape[5] * shape[5]);
	}
	else if (dir == 1) {
		dr = dx*dx / (shape[3] * shape[3]) + dz*dz / (shape[5] * shape[5]);
	}
	else if (dir == 2) {
		dr = dx*dx / (shape[3] * shape[3]) + dy*dy / (shape[4] * shape[4]);
	}
	if (dr < 1.0) {
		return TRUE;
	}
	return FALSE;
}

int MP_GridCylinderType(MP_GridData *data, short type,
	int x0, int y0, int z0, int x1, int y1, int z1, int dir, double margin)
{
	double shape[6];
	int x, y, z, id;
	int count = 0;

	ShapeData(x0, y0, z0, x1, y1, z1, margin, shape);
	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot && CylinderCheck(data, x, y, z, dir, shape)) {
					data->type[id] = type;
					count++;
				}
			}
		}
	}
	return count;
}

int MP_GridCylinderUpdate(MP_GridData *data, short update,
	int x0, int y0, int z0, int x1, int y1, int z1, int dir, double margin)
{
	double shape[6];
	int x, y, z, id;
	int count = 0;

	ShapeData(x0, y0, z0, x1, y1, z1, margin, shape);
	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot && CylinderCheck(data, x, y, z, dir, shape)) {
					data->update[id] = update;
					count++;
				}
			}
		}
	}
	return count;
}

int MP_GridCylinderVal(MP_GridData *data, double val,
	int x0, int y0, int z0, int x1, int y1, int z1, int dir, double margin)
{
	double shape[6];
	int x, y, z, id;
	int count = 0;

	ShapeData(x0, y0, z0, x1, y1, z1, margin, shape);
	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot && CylinderCheck(data, x, y, z, dir, shape)) {
					data->val[id] = val;
					count++;
				}
			}
		}
	}
	return count;
}

double MP_GridAveVal(MP_GridData *data,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int x, y, z, id;
	double vtot = 0.0;
	int ntot = 0;

	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot) {
					vtot += data->val[id];
					ntot++;
				}
			}
		}
	}
	if (ntot > 0) return vtot / ntot;
	else return 0.0;
}

int MP_GridCountType(MP_GridData *data, short type,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int x, y, z, id;
	int count = 0;

	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				id = MP_GRID_INDEX(data, x, y, z);
				if (id >= 0 && id < data->ntot) {
					if (data->type[id] == type) count++;
				}
			}
		}
	}
	return count;
}

int MP_GridUniformRandom(MP_GridData *data, short type, int num,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int n = 0;
	int x, y, z, id;

	while (n < num) {
		x = (int)(data->size[0]*MP_Rand(&(data->rand_seed)));
		y = (int)(data->size[1]*MP_Rand(&(data->rand_seed)));
		z = (int)(data->size[2]*MP_Rand(&(data->rand_seed)));
		id = MP_GRID_INDEX(data, x, y, z);
		if (x >= x0 && x <= x1 && y >= y0 && y <= y1 && z >= z0 && z <= z1 
			&& data->type[id] != type) {
			data->type[id] = type;
			n++;
		}
	}
	return n;
}

int MP_GridGaussRandom(MP_GridData *data, short type, int num, double spdis,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int n = 0;
	int x, y, z, id;

	if (x0 < 0) x0 = 0;
	if (x1 > data->size[0] - 1) x1 = data->size[0] - 1;
	if (y0 < 0) y0 = 0;
	if (y1 > data->size[1] - 1) y1 = data->size[1] - 1;
	if (z0 < 0) z0 = 0;
	if (z1 > data->size[2] - 1) z1 = data->size[2] - 1;
	while (n < num) {
		x = (int)(data->size[0] * (0.5 + spdis*MP_RandGauss(&(data->rand_seed))));
		y = (int)(data->size[1] * (0.5 + spdis*MP_RandGauss(&(data->rand_seed))));
		z = (int)(data->size[2] * (0.5 + spdis*MP_RandGauss(&(data->rand_seed))));
		if (x >= x0 && x <= x1 && y >= y0 && y <= y1 && z >= z0 && z <= z1) {
			id = MP_GRID_INDEX(data, x, y, z);
			if (data->type[id] != type) {
				data->type[id] = type;
				n++;
			}
		}
	}
	return n;
}

int MP_GridWrite(MP_GridData *data, char *filename, int comp)
{
	int i;
	gzFile gfp;
	char mode[32];

	sprintf(mode, "wb%df", comp);
	if ((gfp = gzopen(filename, mode)) == NULL) {
		fprintf(stderr, "Error : can't open %s.(MP_GridWrite)\n", filename);
		return FALSE;
	}
	gzprintf(gfp, "size %d %d %d\n", data->size[0], data->size[1], data->size[2]);
	gzprintf(gfp, "ntype %d\n", data->ntype);
	gzprintf(gfp, "element %.15e %.15e %.15e\n", data->element[0], data->element[1], data->element[2]);
	gzprintf(gfp, "type,update,val\n");
	for (i = 0; i < data->ntot; i++) {
		gzprintf(gfp, "%d %d %.15e\n", data->type[i], data->update[i], data->val[i]);
	}
	gzprintf(gfp, "inter_x,inter_y,inter_z,coef_x,coef_y,coef_z\n");
	for (i = 0; i < data->ntype*data->ntype; i++) {
		gzprintf(gfp, "%d %d %d %.15e %.15e %.15e\n",
			data->inter_x[i], data->inter_y[i], data->inter_z[i],
			data->coef_x[i], data->coef_y[i], data->coef_z[i]);
	}
	gzprintf(gfp, "rhoc\n");
	for (i = 0; i < data->ntype; i++) {
		gzprintf(gfp, "%.15e\n", data->rhoc[i]);
	}
	gzprintf(gfp, "bound %d %d %d %d %d %d\n",
		data->bound[0], data->bound[1], data->bound[2],
		data->bound[3], data->bound[4], data->bound[5]);
	gzprintf(gfp, "step %d\n", data->step);
	gzclose(gfp);
	return TRUE;
}

static int GridRead0(MP_GridData *data, char *filename)
{
	int i;
	gzFile gfp;
	char buf[256], dum[256];
	int nx, ny, nz, ntype;
	int inter;
	double coef;

	if ((gfp = gzopen(filename, "rb")) == NULL) {
		fprintf(stderr, "Error : can't open %s.(MP_GridRead)\n", filename);
		return FALSE;
	}
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d %d %d", dum, &nx, &ny, &nz);
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d", dum, &ntype);
	if (!MP_GridAlloc(data, nx, ny, nz, ntype)) return FALSE;
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %le %le %le", dum,
		&(data->element[0]), &(data->element[1]), &(data->element[2]));
	gzgets(gfp, buf, 256);
	for (i = 0; i < data->ntot; i++) {
		gzgets(gfp, buf, 256);
		sscanf(buf, "%hd %hd %le", &(data->type[i]), &(data->update[i]), &(data->val[i]));
	}
	gzgets(gfp, buf, 256);
	for (i = 0; i < data->ntype*data->ntype; i++) {
		gzgets(gfp, buf, 256);
		sscanf(buf, "%d %le", &inter, &coef);
		data->inter_x[i] = data->inter_y[i] = data->inter_z[i] = inter;
		data->coef_x[i] = data->coef_y[i] = data->coef_z[i] = coef;
	}
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d %d %d %d %d %d", dum,
		&(data->bound[0]), &(data->bound[1]), &(data->bound[2]),
		&(data->bound[3]), &(data->bound[4]), &(data->bound[5]));
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d", dum, &(data->step));
	gzclose(gfp);
	return TRUE;
}

static int GridRead1(MP_GridData *data, char *filename)
{
	int i;
	gzFile gfp;
	char buf[256], dum[256];
	int nx, ny, nz, ntype;

	if ((gfp = gzopen(filename, "rb")) == NULL) {
		fprintf(stderr, "Error : can't open %s.(MP_GridRead)\n", filename);
		return FALSE;
	}
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d %d %d", dum, &nx, &ny, &nz);
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d", dum, &ntype);
	if (!MP_GridAlloc(data, nx, ny, nz, ntype)) return FALSE;
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %le %le %le", dum,
		&(data->element[0]), &(data->element[1]), &(data->element[2]));
	gzgets(gfp, buf, 256);
	for (i = 0; i < data->ntot; i++) {
		gzgets(gfp, buf, 256);
		sscanf(buf, "%hd %hd %le", &(data->type[i]), &(data->update[i]), &(data->val[i]));
	}
	gzgets(gfp, buf, 256);
	for (i = 0; i < data->ntype*data->ntype; i++) {
		gzgets(gfp, buf, 256);
		sscanf(buf, "%d %d %d %le %le %le",
			&(data->inter_x[i]), &(data->inter_y[i]), &(data->inter_z[i]),
			&(data->coef_x[i]), &(data->coef_y[i]), &(data->coef_z[i]));
	}
	gzgets(gfp, buf, 256);
	for (i = 0; i < data->ntype; i++) {
		gzgets(gfp, buf, 256);
		sscanf(buf, "%le", &(data->rhoc[i]));
	}
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d %d %d %d %d %d", dum,
		&(data->bound[0]), &(data->bound[1]), &(data->bound[2]),
		&(data->bound[3]), &(data->bound[4]), &(data->bound[5]));
	gzgets(gfp, buf, 256);
	sscanf(buf, "%s %d", dum, &(data->step));
	gzclose(gfp);
	return TRUE;
}

int MP_GridRead(MP_GridData *data, char *filename, int version)
{
	switch (version) {
	case 0:
		return GridRead0(data, filename);
	case 1:
		return GridRead1(data, filename);
	default:
		fprintf(stderr, "Error : Invalid version, %d(MP_GridRead)\n", version);
		return FALSE;
	}
}

int MP_GridCopy(MP_GridData *src, MP_GridData *dst,
	int x0, int y0, int z0, int x1, int y1, int z1)
{
	int i;
	int nx, ny, nz;
	int x, y, z;
	int src_id, dst_id;

	nx = x1 - x0 + 1;
	ny = y1 - y0 + 1;
	nz = z1 - z0 + 1;
	if (!MP_GridAlloc(dst, nx, ny, nz, src->ntype)) return FALSE;	
	for (i = 0; i < 3; i++) dst->element[i] = src->element[i];
	for (z = z0; z <= z1; z++) {
		for (y = y0; y <= y1; y++) {
			for (x = x0; x <= x1; x++) {
				src_id = MP_GRID_INDEX(src, x, y, z);
				if (src_id >= 0 && src_id < src->ntot) {
					dst_id = MP_GRID_INDEX(dst, x - x0, y - y0, z - z0);
					dst->type[dst_id] = src->type[src_id];
					dst->update[dst_id] = src->update[src_id];
					dst->val[dst_id] = src->val[src_id];
				}
			}
		}
	}
	for (i = 0; i < dst->ntype*dst->ntype; i++) {
		dst->inter_x[i] = src->inter_x[i];
		dst->inter_y[i] = src->inter_y[i];
		dst->inter_z[i] = src->inter_z[i];
		dst->coef_x[i] = src->coef_x[i];
		dst->coef_y[i] = src->coef_y[i];
		dst->coef_z[i] = src->coef_z[i];
	}
	for (i = 0; i < dst->ntype; i++) {
		dst->rhoc[i] = src->rhoc[i];
	}
	for (i = 0; i < 6; i++) dst->bound[i] = src->bound[i];
	dst->step = src->step;
	dst->rand_seed = src->rand_seed;
	return TRUE;
}

int MP_GridClone(MP_GridData *src, MP_GridData *dst)
{
	return MP_GridCopy(src, dst, 0, 0, 0,
		src->size[0]-1, src->size[1]-1, src->size[2]-1);
}
