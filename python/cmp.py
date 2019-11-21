#!/usr/bin/env python

import MPGrid
import MPCLGrid
import time

def AlSiCTran(nx, ny, nz, elm, vlr, local_coef):
    lam_al = 236
    lam_sic = 270
    h_al_sic = 2.227e8
    g = MPGrid.new(nx, ny, nz, 2, local_coef)
    g.element = (elm, elm, elm)
    bc = MPGrid.BoundInsulate
    g.bound = (bc, bc, bc, bc, bc, bc)
    g.set_rhoc(2.7*900, 0) # Al
    g.set_rhoc(3.1*680, 1) # SiC
    g.fill_type(1, (45, 0, 0), (65, ny-1, nz-1))
    g.fill_update(0, (0, 0, 0), (0, ny-1, nz-1))
    g.fill_update(0, (nx-1, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(300, (0, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(vlr+300, (0, 0, 0), (0, ny-1, nz-1))
    if local_coef == False:
        g.set_inter_coef1(MPGrid.InterCond, lam_al, 0, 0)
        g.set_inter_coef1(MPGrid.InterTrans, h_al_sic, 0, 1)
        g.set_inter_coef1(MPGrid.InterTrans, h_al_sic, 1, 0)
        g.set_inter_coef1(MPGrid.InterCond, lam_sic, 1, 1)
    else:
        g.set_local_coef1(lam_al / elm, 0, 0)
        g.set_local_coef1(h_al_sic, 0, 1)        
        g.set_local_coef1(h_al_sic, 1, 0)
        g.set_local_coef1(lam_sic / elm, 1, 1)
    return g

if __name__ == "__main__":
    nloop = 10000
    # Normal
    starttime = time.process_time()
    g = AlSiCTran(100, 100, 1, 1.0e-6, 1.0, False)
    dt = g.estimate_dt()
    dv = g.solve(dt, nloop)
    endtime = time.process_time()
    print(g.step, dv, endtime-starttime)
    # Use Local Coef
    starttime = time.process_time()
    g = AlSiCTran(100, 100, 1, 1.0e-6, 1.0, True)
    dt = g.estimate_dt()
    dv = g.solve(dt, nloop)
    endtime = time.process_time()
    print(g.step, dv, endtime-starttime, "Local Coef")
    # Use OpenCL
    starttime = time.process_time()
    g = AlSiCTran(100, 100, 1, 1.0e-6, 1.0, False)
    k = MPCLGrid.new(g, 0)
    dt = g.estimate_dt()
    dv = k.solve(g, dt, nloop)
    endtime = time.process_time()
    print(g.step, dv, endtime-starttime, "OpenCL")
    # Use OpenCL and Local Coef
    starttime = time.process_time()
    g = AlSiCTran(100, 100, 1, 1.0e-6, 1.0, True)
    k = MPCLGrid.new(g, 0)
    dt = g.estimate_dt()
    dv = k.solve(g, dt, nloop)
    endtime = time.process_time()
    print(g.step, dv, endtime-starttime, "OpenCL and Local Coef")

