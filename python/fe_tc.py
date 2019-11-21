#!/usr/bin/env python

import MPGrid
import time

if __name__ == "__main__":
    starttime = time.process_time()
    dt = 1.0e-12
    fnamef = 'fe_f.mpgrid'
    nx = 110
    ny = 10
    nz = 1
    nl = 5
    nr = 5
    vlr = 1
    elm = 1.0e-6
    findv = 1.0e-13
    lam_fe = 67
    g = MPGrid.new(nx, ny, nz, 1, False)
    g.element = (elm, elm, elm)
    g.bound = (0, 0, 0, 0, 0, 0)
    g.set_rhoc(7.87*460, 0) # Fe
    g.set_inter_coef1(0, lam_fe, 0, 0)
    g.fill_update(0, (0, 0, 0), (0, ny-1, nz-1))
    g.fill_update(0, (nx-1, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(300, (0, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(vlr+300, (0, 0, 0), (0, ny-1, nz-1))
    while 1:
        dv = g.solve(dt, 10000)
        v12 = g.ave_val((1, 0, 0), (1, ny-1, nz-1)) - g.ave_val((2, 0, 0), (2, ny-1, nz-1))
        sigma = lam_fe*v12*(nx-nl-nr-1)/(vlr-nl*v12-nr*v12)
        print(g.step, dv, sigma)
        if dv < findv:
            break
    g.write(fnamef, 8)
    endtime = time.process_time()
    print('----- Execution time =', endtime-starttime, '-----')

