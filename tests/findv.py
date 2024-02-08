import MPGrid
import time
import math as m

if __name__ == "__main__":
    starttime = time.time()
    dt = 2.0e-12
    elm = 1.0e-6
    lam = 236
    rhoc = 2.7*900
    findv = 1.0e-14
    nx = 110
    ny = 100
    nz = 1
    nl = 5
    nr = 5
    vlr = 1
    g = MPGrid.new(nx, ny, nz, 2, False)
    g.element = (elm, elm, elm)
    bc = MPGrid.BoundInsulate
    g.bound = (bc, bc, bc, bc, bc, bc)
    g.set_rhoc(rhoc, 0)
    g.set_inter_coef1(MPGrid.InterCond, lam, 0, 0)
    g.fill_update(False, (0, 0, 0), (0, ny-1, nz-1))
    g.fill_update(False, (nx-1, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(300, (0, 0, 0), (nx-1, ny-1, nz-1))
    g.fill_val(vlr+300, (0, 0, 0), (0, ny-1, nz-1))
    print('dv mean_flow diff')
    pdv = 1.0e-3
    while 1:
        dv = g.solve(dt, 1)
        if (pdv/dv >= 10):
            v12 = g.ave_val((1, 0, 0), (1, ny-1, nz-1)) - g.ave_val((2, 0, 0), (2, ny-1, nz-1))
            etc = lam*v12*(nx-nl-nr-1)/(vlr-nl*v12-nr*v12)
            print("%2.1e %3.2e %3.2e" % (dv, g.mean_flow(), etc-lam))
            pdv = dv
        if dv < findv:
            break
    endtime = time.time()
    print('----- Execution time =', endtime-starttime, '-----')
