import MPGrid
import time

def ETC(g, nl, nr, lam_hs):
    nx = g.size[0]
    ny = g.size[1]
    nz = g.size[2]
    vl = g.ave_val((0, 0, 0), (0, ny - 1, nz - 1))
    vr = g.ave_val((nx - 1, 0, 0), (nx - 1, ny - 1, nz - 1))
    dlr = vl - vr
    dlhs = vl - g.ave_val((nl, 0, 0), (nl, ny - 1, nz - 1))
    drhs = g.ave_val((nx - nr - 1, 0, 0), (nx - nr - 1, ny - 1, nz - 1)) - vr
    etc = lam_hs * (dlhs + drhs) * ((nx - 1) / (nl + nr) - 1) / (dlr - dlhs - drhs)
    return etc

if __name__ == "__main__":
    starttime = time.time()
    dt = 2.0e-12
    fnamef = 'alsic_cpu.mpgrid'
    nx = 510
    ny = 500
    nz = 1
    nl = 5
    nr = 5
    vlr = 1
    elm = 1.0e-6
    findv = 1.0e-12
    lam_al = 236
    lam_sic = 270
    h_al_sic = 2.227e8
    g = MPGrid.new(nx, ny, nz, 2, False)
    g.element = (elm, elm, elm)
    bc = MPGrid.BoundInsulate
    g.bound = (bc, bc, bc, bc, bc, bc)
    g.set_rhoc(2.7*900, 0) # Al
    g.set_rhoc(3.1*680, 1) # SiC    
    g.set_inter_coef1(MPGrid.InterCond, lam_al, 0, 0)
    g.set_inter_coef1(MPGrid.InterTrans, h_al_sic, 0, 1)
    g.set_inter_coef1(MPGrid.InterTrans, h_al_sic, 1, 0)
    g.set_inter_coef1(MPGrid.InterCond, lam_sic, 1, 1)
    g.fill_type(1, (205, 0, 0), (305, ny-1, nz-1))
    g.fill_update(False, (0, 0, 0), (0, ny-1, nz-1))
    g.fill_update(False, (nx-1, 0, 0), (nx-1, ny-1, nz-1))
    g.grad_val(0, vlr+300, 300)
    print('step dv mean_flow etc')
    while 1:
        dv = g.solve(dt, 10000)
        etc = ETC(g, nl, nr, lam_al)
        print(g.step, dv, g.mean_flow(), etc)
        if dv < findv:
            break
    g.write(fnamef, 8)
    endtime = time.time()
    print('----- Execution time =', endtime-starttime, '-----')

