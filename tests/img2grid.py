import cv2
import MPGrid

def Img2Grid(img, elm, lam, hcoef, rhoc):
    nr = 5
    nl = 5
    vlr = 1
    nx = img.shape[1]+nr+nl
    ny = img.shape[0]
    nz = 1
    ntype = len(lam)
    g = MPGrid.new(nx, ny, nz, ntype, True)
    g.element = (elm, elm, elm)
    bc = MPGrid.BoundInsulate
    g.bound = (bc, bc, bc, bc, bc, bc)
    for i in range(ntype):
        for j in range(ntype):
            if i == j:
                g.set_inter_coef1(MPGrid.InterCond, lam[i], i, j)
            else:
                g.set_inter_coef1(MPGrid.InterTrans, hcoef[i][j], i, j)
        g.set_rhoc(rhoc[i], i)
    g.fill_update(False, (0, 0, 0), (0, ny-1, nz-1))
    g.fill_update(False, (nx-1, 0, 0), (nx-1, ny-1, nz-1))
    g.grad_val(0, vlr+300, 300)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] < 128:
                g.set_type(0, (nr+j, img.shape[0]-1-i, 0))
            else:
                g.set_type(1, (nr+j, img.shape[0]-1-i, 0))
    g.ref_local_coef()
    return g

if __name__ == "__main__":
    fname = 'bwimg.png'
    gname = 'bwimg.mpgrid'
    elm = 1.6e-6
    lam = [236, 580]
    hcoef = [[0, 1.101e8], [1.101e8, 0]]
    rhoc = [2.7*900, 2.2*691]
    img = cv2.imread(fname, 0)
    g = Img2Grid(img, elm, lam, hcoef, rhoc)
    g.write(gname, 8)
