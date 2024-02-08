import MPGrid
import time

def ETC(g, nloop, dt, findv):
    starttime = time.time()
    nr = 5
    nl = 5
    vlr = 1
    nx = g.size[0]
    ny = g.size[1]
    nz = g.size[2]
    lam_mat = g.get_coef(0, 0)[0]
    print('nx = %d ny = %d nz = %d lam_mat = %f' % (nx, ny, nz, lam_mat))
    print('step dv mean_flow etc')
    while 1:
        dv = g.solve(dt, nloop)
        v12 = g.ave_val((1, 0, 0), (1, ny-1, nz-1)) - g.ave_val((2, 0, 0), (2, ny-1, nz-1))
        etc = lam_mat*v12*(nx-nl-nr-1)/(vlr-nl*v12-nr*v12)
        print(g.step, dv, g.mean_flow(), etc)
        if dv < findv:
            break
    endtime = time.time()
    print('----- Execution time =', endtime-starttime, '-----')
    return etc

if __name__ == "__main__":
    fname = ['bwimg.mpgrid',]
    fnamef = ['bwimg_f.mpgrid',]
    nloop = 10000
    dt = 1.0e-12
    findv = 1.0e-12
    etc = []
    for i in range(len(fname)):
        g = MPGrid.read(fname[i])
        etc.append(ETC(g, nloop, dt, findv))
        g.write(fnamef[i], 8)
    print(fname, etc)

