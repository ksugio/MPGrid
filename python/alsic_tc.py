#!/usr/bin/env python

import MPGrid
import time

if __name__ == "__main__":
    starttime = time.clock()
    dt = 1.0e-12
    fnamef = 'alsic_f.mpgrid'
    nx = 110
    ny = 10
    nz = 1
    nl = 5
    nr = 5
    vlr = 1
    elm = 1.0e-6
    findv = 1.0e-13
    lam_al = 236
    lam_sic = 270
    h_al_sic = 2.227e8
    g = MPGrid.new(nx, ny, nz, 2, MPGrid.False)
    g.element = (elm, elm, elm)
    g.bound = (0, 0, 0, 0, 0, 0)
    g.set_rhoc(2.7*900, 0) # Al
    g.set_rhoc(3.1*680, 1) # SiC    
    g.set_inter_coef1(0, lam_al, 0, 0)
    g.set_inter_coef1(1, h_al_sic, 0, 1)
    g.set_inter_coef1(1, h_al_sic, 1, 0)
    g.set_inter_coef1(0, lam_sic, 1, 1)
    g.fill_type(1, (45, 0, 0), (65, ny-1, nz-1))
    g.fill_update(0, (0, 0, 0), (0, ny-1, nz-1))
    g.fill_update(0, (nx-1, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(300, (0, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(vlr+300, (0, 0, 0), (0, ny-1, nz-1))
    while 1:
        dv = g.solve(dt, 10000)
        v12 = g.ave_val((1, 0, 0), (1, ny-1, nz-1)) - g.ave_val((2, 0, 0), (2, ny-1, nz-1))
        sigma = lam_al*v12*(nx-nl-nr-1)/(vlr-nl*v12-nr*v12)
        print g.step, dv, sigma
        if dv < findv:
            break
    g.write(fnamef, 8)
    endtime = time.clock()
    print '----- Execution time =', endtime-starttime, '-----'

