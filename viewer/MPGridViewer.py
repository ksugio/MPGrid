import MPGrid
import time

import MPGrid
import MPGLGrid
import sys
import math
import numpy as np
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL
from OpenGL import GL
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

"""
GLWidget Class
"""
class GLWidget(QtOpenGL.QGLWidget):
  def __init__(self, parent=None):
    QtOpenGL.QGLWidget.__init__(self, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
    self.colorMode = [0, 0]
    self.grid = None
    self.draw = MPGLGrid.draw()
    self.scene = MPGLGrid.scene()
    self.model = None
    self.cmp = MPGLGrid.colormap()
    self.axis_disp = True
    self.cmp_disp = True
    self.step_disp = True

  def minimumSizeHint(self):
    return QtCore.QSize(320, 240)

  def sizeHint(self):
    return QtCore.QSize(800, 600)

  def initializeGL(self):
    self.scene.setup()
    self.draw.list()

  def paintGL(self):
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    if self.grid:
      GL.glPushMatrix()
      self.model.transform()
      self.draw.draw(self.grid, self.cmp)
      if self.axis_disp:
        GL.glTranslatef(-2.0, -2.0, -2.0)
        self.draw.draw_axis(self.grid.size)
      GL.glPopMatrix()
      if self.cmp_disp:
        self.drawColormap()
      if self.step_disp:
        s = str(self.grid.step) + ' step'
        self.drawString(10, 20, s)

  def drawColormap(self):
    GL.glPushMatrix()
    GL.glRotated(90.0, 0.0, 0.0, 1.0)
    GL.glRotated(90.0, 1.0, 0.0, 0.0)
    GL.glTranslate((2.0 - self.scene.width) / self.scene.height, -self.cmp.size[1] / 2.0, self.scene.znear - 1.0e-6)
    self.cmp.draw()
    GL.glPopMatrix()

  def drawString(self, x, y, s):
    GL.glPushAttrib(GL.GL_LIGHTING_BIT)
    GL.glDisable(GL.GL_LIGHTING)
    GL.glColor3fv(self.cmp.font_color)
    self.scene.front_text(x, y, s, self.cmp.font_type)
    GL.glPopAttrib()

  def resizeGL(self, width, height):
    self.scene.resize(width, height)

  def mousePressEvent(self, event):
    if self.model:
      self.model.button(event.x(), event.y(), 1)

  def mouseReleaseEvent(self, event):
    if self.model:
      self.model.button(event.x(), event.y(), 0)

  def mouseMoveEvent(self, event):
    if self.model:
      if event.buttons() & QtCore.Qt.LeftButton:
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
          ctrl = 1 
        else:
          ctrl = 0
        if self.model.motion(self.scene, event.x(), event.y(), ctrl):
          self.updateGL()

  def cmpRange(self):
    if self.grid:
      self.draw.cmp_range(self.grid, self.cmp)    

  def screenShot(self):
    buf = GL.glReadPixels(0, 0, self.width(), self.height(), GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
    img0 = np.frombuffer(buf, dtype=np.uint8).reshape(self.height(), self.width(), 3)
    img1 = cv2.cvtColor(img0, cv2.COLOR_RGB2BGR)
    return cv2.flip(img1, 0)
    
  def setColorMode(self, back_mode, cmp_mode):
    self.colorMode = [back_mode, cmp_mode]
    if back_mode == 0:
      self.scene.clear_color = (0.0, 0.0, 0.0, 0.0)
      self.cmp.font_color = (1.0, 1.0, 1.0)
    elif back_mode == 1:
      self.scene.clear_color = (1.0, 1.0, 1.0, 0.0)
      self.cmp.font_color = (0.0, 0.0, 0.0)
    if cmp_mode == 0:
      self.cmp.color()
    elif cmp_mode == 1:
      self.cmp.grayscale()
    self.scene.setup()
    self.updateGL()

"""
FillDialog
""" 
class FillDialog(QtWidgets.QDialog):
  def __init__(self, parent, grid, method, item):
    QtWidgets.QDialog.__init__(self, parent)
    self.grid = grid
    self.method = method
    self.item = item
    self.setWindowTitle(method + " " + item)
    vbox = QtWidgets.QVBoxLayout(self)
    hbox1 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox1)
    label1 = QtWidgets.QLabel()
    label1.setText(item)
    hbox1.addWidget(label1)
    if item == 'Type':
      self.spin = QtWidgets.QSpinBox()
      hbox1.addWidget(self.spin)
      self.spin.setMaximum(grid.ntype - 1)
    elif item == 'Update':
      self.combo1 = QtWidgets.QComboBox()
      hbox1.addWidget(self.combo1)
      self.combo1.addItem('False')
      self.combo1.addItem('True')
    elif item == 'Val':
      self.lined = QtWidgets.QLineEdit()
      self.lined.setText('0')
      self.lined.setValidator(QtGui.QDoubleValidator())
      hbox1.addWidget(self.lined)
    glay = QtWidgets.QGridLayout()
    vbox.addLayout(glay)
    label2 = QtWidgets.QLabel()
    label2.setText("Start (x0, y0, z0)")
    glay.addWidget(label2, 0, 0)
    self.spinx0 = self.SpinBox(grid.size[0] - 1)
    glay.addWidget(self.spinx0, 0, 1)
    self.spiny0 = self.SpinBox(grid.size[1] - 1)
    glay.addWidget(self.spiny0, 0, 2)
    self.spinz0 = self.SpinBox(grid.size[2] - 1)
    glay.addWidget(self.spinz0, 0, 3)
    label3 = QtWidgets.QLabel(self)
    label3.setText("End (x1, y1, z1)")
    glay.addWidget(label3, 1, 0)
    self.spinx1 = self.SpinBox(grid.size[0] - 1)
    glay.addWidget(self.spinx1, 1, 1)
    self.spiny1 = self.SpinBox(grid.size[1] - 1)
    glay.addWidget(self.spiny1, 1, 2)
    self.spinz1 = self.SpinBox(grid.size[2] - 1)
    glay.addWidget(self.spinz1, 1, 3)
    if method == 'Cylinder':
      hbox2 = QtWidgets.QHBoxLayout()
      vbox.addLayout(hbox2)  
      label4 = QtWidgets.QLabel(self)
      label4.setText("Direction")
      hbox2.addWidget(label4)
      self.combo2 = QtWidgets.QComboBox()
      hbox2.addWidget(self.combo2)
      self.combo2.addItem('x')
      self.combo2.addItem('y')
      self.combo2.addItem('z')
    self.button = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.button)
    self.button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.button.accepted.connect(self.Accept)
    self.button.rejected.connect(self.reject)

  def SpinBox(self, max):
    spin = QtWidgets.QSpinBox()
    spin.setMaximum(max)
    spin.setMinimumWidth(50)
    return spin

  def Accept(self):
    x0 = self.spinx0.value()
    y0 = self.spiny0.value()
    z0 = self.spinz0.value()
    x1 = self.spinx1.value()
    y1 = self.spiny1.value()
    z1 = self.spinz1.value()
    if self.method == 'Fill':
      if self.item == 'Type':
        self.grid.fill_type(self.spin.value(), (x0, y0, z0), (x1, y1, z1))
      elif self.item == 'Update':
        if self.combo1.currentIndex() == 0:
          self.grid.fill_update(0, (x0, y0, z0), (x1, y1, z1))
        elif self.combo1.currentIndex() == 1:
          self.grid.fill_update(1, (x0, y0, z0), (x1, y1, z1))
      elif self.item == 'Val':
        val = float(self.lined.text())
        self.grid.fill_val(val, (x0, y0, z0), (x1, y1, z1))
    elif self.method == 'Ellipsoid':
      if self.item == 'Type':
        self.grid.ellipsoid_type(self.spin.value(), (x0, y0, z0), (x1, y1, z1))
      elif self.item == 'Update':
        if self.combo1.currentIndex() == 0:
          self.grid.ellipsoid_update(0, (x0, y0, z0), (x1, y1, z1))
        elif self.combo1.currentIndex() == 1:
          self.grid.ellipsoid_update(1, (x0, y0, z0), (x1, y1, z1))
      elif self.item == 'Val':
        val = float(self.lined.text())
        self.grid.ellipsoid_val(val, (x0, y0, z0), (x1, y1, z1))
    elif self.method == 'Cylinder':
      di = self.combo2.currentIndex()
      if self.item == 'Type':
        self.grid.cylinder_type(self.spin.value(), (x0, y0, z0), (x1, y1, z1), di)
      elif self.item == 'Update':
        if self.combo1.currentIndex() == 0:
          self.grid.cylinder_update(0, (x0, y0, z0), (x1, y1, z1), di)
        elif self.combo1.currentIndex() == 1:
          self.grid.cylinder_update(1, (x0, y0, z0), (x1, y1, z1), di)
      elif self.item == 'Val':
        val = float(self.lined.text())
        self.grid.cylinder_val(val, (x0, y0, z0), (x1, y1, z1), di)
    self.accept()

"""
NewGridDialog
""" 
class NewGridDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.setWindowTitle("New Grid")
    vbox = QtWidgets.QVBoxLayout(self)
    hbox1 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox1)
    label1 = QtWidgets.QLabel()
    label1.setText('nx, ny, nz')
    hbox1.addWidget(label1)
    self.spinnx = self.SpinBox(2000)
    hbox1.addWidget(self.spinnx)
    self.spinny = self.SpinBox(2000)
    hbox1.addWidget(self.spinny)
    self.spinnz = self.SpinBox(2000)
    hbox1.addWidget(self.spinnz)
    hbox2 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox2)
    label2 = QtWidgets.QLabel()
    label2.setText('ntype')
    hbox2.addWidget(label2)
    self.spinntype = self.SpinBox(100)
    hbox2.addWidget(self.spinntype)
    self.check = QtWidgets.QCheckBox("Local Coefficient")
    vbox.addWidget(self.check)
    self.button = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.button)
    self.button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.button.accepted.connect(self.accept)
    self.button.rejected.connect(self.reject)

  def SpinBox(self, max):
    spin = QtWidgets.QSpinBox()
    spin.setMinimum(1)
    spin.setMaximum(max)
    spin.setMaximumWidth(150)
    return spin    

  def newGrid(self):
    nx = self.spinnx.value()
    ny = self.spinny.value()
    nz = self.spinnz.value()
    ntype = self.spinntype.value()
    if (self.check.isChecked()):
      grid = MPGrid.new(nx, ny, nz, ntype, 1)
    else:
      grid = MPGrid.new(nx, ny, nz, ntype, 0)        
    return grid

"""
FromImageDialog
""" 
class ImageScene(QtWidgets.QGraphicsScene):
  pickColor = QtCore.pyqtSignal(int, int, int)

  def __init__(self, *argv, **keywords):
    super(ImageScene, self).__init__(*argv, **keywords)

  def setImage(self, cvimg):
    if len(cvimg.shape) == 2:
      height, width = cvimg.shape
      qimg = QtGui.QImage(cvimg.data, width, height, width, QtGui.QImage.Format_Indexed8)
    elif len(cvimg.shape) == 3:  
      height, width, dim = cvimg.shape
      qimg = QtGui.QImage(cvimg.data, width, height, dim*width, QtGui.QImage.Format_RGB888)
      qimg = qimg.rgbSwapped()
    self.pixmap = QtGui.QPixmap.fromImage(qimg)
    self.clear()
    self.addPixmap(self.pixmap)

  def mousePressEvent(self, event):
    if event.button() == QtCore.Qt.LeftButton:
      x = event.scenePos().x()    
      y = event.scenePos().y()
      c = self.pixmap.toImage().pixel(x, y)
      colors = QtGui.QColor(c).getRgb()
      self.pickColor.emit(colors[0], colors[1], colors[2])

class FromImageDialog(QtWidgets.QDialog):
  def __init__(self, parent):
    QtWidgets.QDialog.__init__(self, parent)
    self.setWindowTitle("From Image")
    self.colors = []
    self.cvimg = None
    hbox = QtWidgets.QHBoxLayout(self)
    vbox = QtWidgets.QVBoxLayout()
    hbox.addLayout(vbox)
    button0 = QtWidgets.QPushButton('Load Image')
    button0.clicked[bool].connect(self.loadImage)
    vbox.addWidget(button0)
    self.list = QtWidgets.QListWidget()
    vbox.addWidget(self.list)
    hbox1 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox1)
    self.spinr = self.SpinBox()
    self.spinr.setPrefix('R : ')
    hbox1.addWidget(self.spinr)
    self.sping = self.SpinBox()
    self.sping.setPrefix('G : ')
    hbox1.addWidget(self.sping)
    self.spinb = self.SpinBox()
    self.spinb.setPrefix('B : ')
    hbox1.addWidget(self.spinb)
    hbox2 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox2)
    button1 = QtWidgets.QPushButton('Add Color')
    button1.clicked[bool].connect(self.addColor)
    hbox2.addWidget(button1)
    button2 = QtWidgets.QPushButton('Delete Color')
    button2.clicked[bool].connect(self.delColor)
    hbox2.addWidget(button2)
    self.buttonb = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.accept)
    self.buttonb.rejected.connect(self.reject)
    view = QtWidgets.QGraphicsView()
    view.setMinimumSize(640, 480)
    self.scene = ImageScene()
    self.scene.pickColor.connect(self.pickColor)
    view.setScene(self.scene)
    hbox.addWidget(view)

  def SpinBox(self):
    spin = QtWidgets.QSpinBox()
    spin.setMinimum(0)
    spin.setMaximum(255)
    spin.setMaximumWidth(100)
    return spin    

  def loadImage(self):
     fname = QtWidgets.QFileDialog.getOpenFileName(self, 'File', filter='Image Files (*.jpg *.png *.tif *.bmp);;All Files (*.*)')[0]
     if fname:
       self.cvimg = cv2.imread(fname)
       self.scene.setImage(self.cvimg)

  def pickColor(self, r, g, b):
    self.spinr.setValue(r)
    self.sping.setValue(g)
    self.spinb.setValue(b)

  def addColor(self):
    rgb = [self.spinr.value(), self.sping.value(), self.spinb.value()]
    if rgb not in self.colors:
      self.colors.append(rgb)
    self.updateList()

  def delColor(self):
    row = self.list.currentRow()
    if row >= 0:
      self.colors.pop(row)
      self.updateList()

  def updateList(self):
    self.list.clear()
    for i in range(len(self.colors)):
      txt = 'Type{} : {}'.format(i+1, self.colors[i])
      self.list.addItem(txt)

  def newGrid(self):
    if self.cvimg is not None:
      img0 = cv2.cvtColor(self.cvimg, cv2.COLOR_BGR2RGB)
      img = cv2.flip(img0, 0)
      nx = img.shape[1]
      ny = img.shape[0]
      ntype = len(self.colors)+1
      grid = MPGrid.new(nx, ny, 1, ntype, 0)
      for x in range(nx):
        for y in range(ny):
          for i in range(len(self.colors)):
            if img[y, x, 0] == self.colors[i][0] and img[y, x, 1] == self.colors[i][1] and img[y, x, 2] == self.colors[i][2]:
              grid.set_type(i+1, (x, y, 0))
      return grid
    else:
      return None

"""
InterCoefDialog
""" 
class InterCoefDialog(QtWidgets.QDialog):
  def __init__(self, parent, grid):
    QtWidgets.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Interface and Coefficient Setting")
    vbox = QtWidgets.QVBoxLayout(self)
    self.table = QtWidgets.QTableWidget(grid.ntype * grid.ntype, 7)
    self.SetTable()
    self.table.cellClicked[int,int].connect(self.cellClicked)
    vbox.addWidget(self.table)
    hbox = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox)
    self.combo1 = QtWidgets.QComboBox()
    self.combo1.setMaximumWidth(80)
    for i in range(grid.ntype):
      for j in range(grid.ntype):
        self.combo1.addItem('Type ' + str(i) + ', ' + str(j))
    hbox.addWidget(self.combo1)
    self.combo2 = QtWidgets.QComboBox()
    self.combo2.setMaximumWidth(80)
    self.combo2.addItem('Cond')
    self.combo2.addItem('Trans')
    hbox.addWidget(self.combo2)
    self.combo3 = QtWidgets.QComboBox()
    self.combo3.setMaximumWidth(80)
    self.combo3.addItem('All')
    self.combo3.addItem('X')
    self.combo3.addItem('Y')
    self.combo3.addItem('Z')
    hbox.addWidget(self.combo3)
    self.lined1 = QtWidgets.QLineEdit()
    self.lined1.setValidator(QtGui.QDoubleValidator())
    hbox.addWidget(self.lined1)
    self.button = QtWidgets.QPushButton('Set')
    self.button.clicked.connect(self.UpdateInterCoef)
    hbox.addWidget(self.button)
    self.buttonb = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def cellClicked(self, row, col):
    self.combo1.setCurrentIndex(row)

  def UpdateInterCoef(self):
    row = self.combo1.currentIndex()
    txt = self.combo2.currentText()
    xyz = self.combo3.currentIndex()
    val = self.lined1.text()
    if xyz == 0:
      self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(txt))
      self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(txt))
      self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(txt))
      self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(val))
      self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(val))
      self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(val))
    elif xyz == 1:
      self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(txt))
      self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(val))
    elif xyz == 2:
      self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(txt))
      self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(val))
    elif xyz == 3:
      self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(txt))
      self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(val))

  def minimumSizeHint(self):
    return QtCore.QSize(320, 240)

  def sizeHint(self):
    return QtCore.QSize(640, 480)

  def SetInterCoef(self, row, inter, coef):
    if inter[0] == 0:
      item = QtWidgets.QTableWidgetItem("Cond")
      self.table.setItem(row, 1, item)
    elif inter[0] == 1:
      item = QtWidgets.QTableWidgetItem("Trans")
      self.table.setItem(row, 1, item)
    if inter[1] == 0:
      item = QtWidgets.QTableWidgetItem("Cond")
      self.table.setItem(row, 2, item)
    elif inter[1] == 1:
      item = QtWidgets.QTableWidgetItem("Trans")
      self.table.setItem(row, 2, item)
    if inter[2] == 0:
      item = QtWidgets.QTableWidgetItem("Cond")
      self.table.setItem(row, 3, item)
    elif inter[2] == 1:
      item = QtWidgets.QTableWidgetItem("Trans")
      self.table.setItem(row, 3, item)
    item = QtWidgets.QTableWidgetItem(str(coef[0]))
    self.table.setItem(row, 4, item)
    item = QtWidgets.QTableWidgetItem(str(coef[1]))
    self.table.setItem(row, 5, item)
    item = QtWidgets.QTableWidgetItem(str(coef[2]))
    self.table.setItem(row, 6, item)
  
  def SetTable(self):
    labels = ['Type i, j', 'Inter x', 'Inter y', 'Inter z', 'Coef x', 'Coef y', 'Coef z']
    self.table.setHorizontalHeaderLabels(labels)
    row = 0
    for i in range(self.grid.ntype):
      for j in range(self.grid.ntype):
        item = QtWidgets.QTableWidgetItem(str(i) + ', ' + str(j))
        self.table.setItem(row, 0, item)
        inter = self.grid.get_inter(i, j)
        coef = self.grid.get_coef(i, j)
        self.SetInterCoef(row, inter, coef)
        row = row + 1

  def Accept(self):
    for row in range(self.table.rowCount()):
      inter = [0, 0, 0]
      if self.table.item(row, 1).text() == 'Trans':
        inter[0] = 1
      if self.table.item(row, 2).text() == 'Trans':
        inter[1] = 1  
      if self.table.item(row, 3).text() == 'Trans':
        inter[2] = 1
      txt_x = self.table.item(row, 4).text()
      txt_y = self.table.item(row, 5).text()
      txt_z = self.table.item(row, 6).text()
      try:
        coef = [float(txt_x), float(txt_y), float(txt_z)]
        i = int(row / self.grid.ntype)
        j = int(row - i * self.grid.ntype)
        self.grid.set_inter_coef3(inter, coef, i, j)
      except:
        print(txt_x, txt_y, txt_z, "is not value.")
      self.accept()

"""
RhocDialog
""" 
class RhocDialog(QtWidgets.QDialog):
  def __init__(self, parent, grid):
    QtWidgets.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Rhoc Setting")
    vbox = QtWidgets.QVBoxLayout(self)
    self.table = QtWidgets.QTableWidget(grid.ntype, 2)
    self.SetTable()
    vbox.addWidget(self.table)
    self.buttonb = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def UpdateRhoc(self):
    row = self.combo1.currentIndex()
    val = self.lined1.text()
    self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(val))

  def SetTable(self):
    labels = ['Type', 'Rhoc']
    self.table.setHorizontalHeaderLabels(labels)
    for row in range(self.grid.ntype):
      item = QtWidgets.QTableWidgetItem(str(row))
      self.table.setItem(row, 0, item)
      rhoc = self.grid.get_rhoc(row)
      item = QtWidgets.QTableWidgetItem(str(rhoc))
      self.table.setItem(row, 1, item)

  def Accept(self):
    for row in range(self.table.rowCount()):
      txt = self.table.item(row, 1).text()
      try:
        rhoc = float(txt)
        self.grid.set_rhoc(rhoc, row)
      except:
        print(txt, 'is not value.')
    self.accept()

"""
ElementDialog
""" 
class ElementDialog(QtWidgets.QDialog):
  def __init__(self, parent, grid):
    QtWidgets.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Element Size")
    vbox = QtWidgets.QVBoxLayout(self)
    label = QtWidgets.QLabel()
    label.setText('ex, ey, ez')
    vbox.addWidget(label)
    hbox = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox)
    self.lined1 = self.LineEdit(str(grid.element[0]))
    hbox.addWidget(self.lined1)
    self.lined2 = self.LineEdit(str(grid.element[1]))
    hbox.addWidget(self.lined2)
    self.lined3 = self.LineEdit(str(grid.element[2]))
    hbox.addWidget(self.lined3)
    self.buttonb = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def LineEdit(self, text):
    lined = QtWidgets.QLineEdit()
    lined.setText(text)
    lined.setValidator(QtGui.QDoubleValidator())
    lined.setMaximumWidth(60)
    return lined

  def Accept(self):
    ex = float(self.lined1.text())
    ey = float(self.lined2.text())
    ez = float(self.lined3.text())
    self.grid.element = (ex, ey, ez)
    self.accept()

"""
BoundDialog
""" 
class BoundDialog(QtWidgets.QDialog):
  def __init__(self, parent, grid):
    QtWidgets.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Boundary Condition")
    vbox = QtWidgets.QVBoxLayout(self)
    glay = QtWidgets.QGridLayout()
    vbox.addLayout(glay)
    label1 = QtWidgets.QLabel()
    label1.setText('Lower (xl, yl, zl)')
    glay.addWidget(label1, 0, 0)
    self.combo1 = self.ComboBox(grid.bound[0])
    glay.addWidget(self.combo1, 0, 1)
    self.combo2 = self.ComboBox(grid.bound[1])
    glay.addWidget(self.combo2, 0, 2)
    self.combo3 = self.ComboBox(grid.bound[2])
    glay.addWidget(self.combo3, 0, 3)
    label2 = QtWidgets.QLabel()
    label2.setText('Upper (xu, yu, zu)')
    glay.addWidget(label2, 1, 0)
    self.combo4 = self.ComboBox(grid.bound[3])
    glay.addWidget(self.combo4, 1, 1)
    self.combo5 = self.ComboBox(grid.bound[4])
    glay.addWidget(self.combo5, 1, 2)
    self.combo6 = self.ComboBox(grid.bound[5])
    glay.addWidget(self.combo6, 1, 3)
    self.buttonb = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def ComboBox(self, bd):
    combo = QtWidgets.QComboBox()
    combo.addItem("Insulate")
    combo.addItem("Periodic")
    combo.setCurrentIndex(bd)
    return combo

  def Accept(self):
    xl = self.combo1.currentIndex()
    yl = self.combo2.currentIndex()
    zl = self.combo3.currentIndex()
    xu = self.combo4.currentIndex()
    yu = self.combo5.currentIndex()
    zu = self.combo6.currentIndex()
    self.grid.bound = (xl, yl, zl, xu, yu, zu)
    self.accept()

"""
DrawRangeDialog
""" 
class DrawRangeDialog(QtWidgets.QDialog):
  def __init__(self, parent, glwidget):
    QtWidgets.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.setWindowTitle("Draw Range")
    vbox = QtWidgets.QVBoxLayout(self)
    glay = QtWidgets.QGridLayout()
    vbox.addLayout(glay)
    label1 = QtWidgets.QLabel()
    label1.setText("Start (x0, y0, z0)")
    glay.addWidget(label1, 0, 0)
    self.spinx0 = self.SpinBox(glwidget.draw.range[0])
    glay.addWidget(self.spinx0, 0, 1)
    self.spiny0 = self.SpinBox(glwidget.draw.range[1])
    glay.addWidget(self.spiny0, 0, 2)
    self.spinz0 = self.SpinBox(glwidget.draw.range[2])
    glay.addWidget(self.spinz0, 0, 3)
    label2 = QtWidgets.QLabel(self)
    label2.setText("End (x1, y1, z1)")
    glay.addWidget(label2, 1, 0)
    self.spinx1 = self.SpinBox(glwidget.draw.range[3])
    glay.addWidget(self.spinx1, 1, 1)
    self.spiny1 = self.SpinBox(glwidget.draw.range[4])
    glay.addWidget(self.spiny1, 1, 2)
    self.spinz1 = self.SpinBox(glwidget.draw.range[5])
    glay.addWidget(self.spinz1, 1, 3)
    self.button = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.button)
    self.button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.button.accepted.connect(self.Accept)
    self.button.rejected.connect(self.reject)

  def SpinBox(self, val):
    spin = QtWidgets.QSpinBox()
    spin.setMaximum(10000)
    spin.setValue(val)    
    spin.setMinimumWidth(60)
    return spin

  def Accept(self):
    x0 = self.spinx0.value()
    y0 = self.spiny0.value()
    z0 = self.spinz0.value()
    x1 = self.spinx1.value()
    y1 = self.spiny1.value()
    z1 = self.spinz1.value()
    self.glwidget.draw.range = (x0, y0, z0, x1, y1, z1)
    self.glwidget.updateGL()
    self.accept()

"""
ColorDialog
""" 
class ColorDialog(QtWidgets.QDialog):
  def __init__(self, parent, glwidget):
    QtWidgets.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.setWindowTitle("Color")
    vbox = QtWidgets.QVBoxLayout(self)
    hbox1 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox1)
    label1 = QtWidgets.QLabel()
    label1.setText("Background")
    hbox1.addWidget(label1)
    self.combo1 = QtWidgets.QComboBox()
    self.combo1.addItem("Black")
    self.combo1.addItem("White")
    self.combo1.setCurrentIndex(glwidget.colorMode[0])
    hbox1.addWidget(self.combo1)
    hbox2 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox2)
    label2 = QtWidgets.QLabel()
    label2.setText("Colormap")
    hbox2.addWidget(label2)
    self.combo2 = QtWidgets.QComboBox()
    self.combo2.addItem("Color")
    self.combo2.addItem("Grayscale")
    self.combo2.setCurrentIndex(glwidget.colorMode[1])
    hbox2.addWidget(self.combo2)
    self.buttonb = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def Accept(self):
    self.glwidget.setColorMode(self.combo1.currentIndex(), self.combo2.currentIndex())
    self.accept()

"""
SolveDialog
""" 
class SolveDialog(QtWidgets.QDialog):
  def __init__(self, parent, glwidget):
    QtWidgets.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.grid = None
    self.setWindowTitle("Solve")
    vbox = QtWidgets.QVBoxLayout(self)
    self.texted = QtWidgets.QTextEdit()
    self.texted.setReadOnly(True)
    vbox.addWidget(self.texted)
    glay = QtWidgets.QGridLayout()
    vbox.addLayout(glay)
    label1 = QtWidgets.QLabel()
    label1.setText("Dt")
    glay.addWidget(label1, 0, 0)
    self.lined1 = QtWidgets.QLineEdit()
    self.lined1.setValidator(QtGui.QDoubleValidator())
    self.lined1.setText(str(glwidget.grid.estimate_dt()))
    glay.addWidget(self.lined1, 0, 1)
    label2 = QtWidgets.QLabel()
    label2.setText("Interval")
    glay.addWidget(label2, 1, 0)
    self.spin1 = QtWidgets.QSpinBox()
    self.spin1.setMinimum(1)
    self.spin1.setMaximum(1000)
    glay.addWidget(self.spin1, 1, 1)
    label3 = QtWidgets.QLabel()
    label3.setText("Finish Dv")
    glay.addWidget(label3, 2, 0)
    self.lined2 = QtWidgets.QLineEdit()
    self.lined2.setValidator(QtGui.QDoubleValidator())
    self.lined2.setText("1.0e-12")
    glay.addWidget(self.lined2, 2, 1)
    hbox1 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox1)
    self.button1 = QtWidgets.QPushButton("Start/Stop")
    self.button1.setCheckable(True)
    self.button1.clicked.connect(self.solveStartStop)
    hbox1.addWidget(self.button1)    
    self.buttonb = QtWidgets.QDialogButtonBox()
    hbox1.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.Reject)
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.doSolve)

  def doSolve(self):    
    dv = self.grid.solve(self.dt, self.step)
    li = str(self.grid.step) + ', ' + str(dv)
    self.texted.append(li)
    if dv < self.findv:
      self.button1.setChecked(False)
      self.stopSolve()
    
  def startSolve(self):
    self.grid = MPGrid.clone(self.glwidget.grid)
    self.lined1.setDisabled(True)
    self.spin1.setDisabled(True)
    self.lined2.setDisabled(True)
    self.buttonb.setDisabled(True)
    self.timer.start()
    
  def stopSolve(self):
    self.timer.stop()
    self.lined1.setDisabled(False)
    self.spin1.setDisabled(False)
    self.lined2.setDisabled(False)
    self.buttonb.setDisabled(False)  

  def solveStartStop(self):
    if self.button1.isChecked():
      self.dt = float(self.lined1.text())
      self.step = self.spin1.value()
      self.findv = float(self.lined2.text())
      self.startSolve()
    else:
      self.stopSolve()
      
  def Accept(self):
    if self.grid:
      self.glwidget.grid = self.grid
    self.accept()
    
  def Reject(self):
    self.reject()

"""
DrawDialog
""" 
class DrawDialog(QtWidgets.QDialog):
  def __init__(self, parent, glwidget):
    QtWidgets.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.setWindowTitle("Draw Setting")
    vbox = QtWidgets.QVBoxLayout(self)
    hbox = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox)
    label = QtWidgets.QLabel()
    label.setText("Draw Method")
    hbox.addWidget(label)    
    self.combo = QtWidgets.QComboBox()
    self.combo.addItem("Quads")
    self.combo.addItem("Cubes")
    self.combo.setCurrentIndex(glwidget.draw.method) 
    hbox.addWidget(self.combo)
    self.table = QtWidgets.QTableWidget(glwidget.grid.ntype, 2)
    self.SetTable()
    vbox.addWidget(self.table)
    self.check1 = QtWidgets.QCheckBox("Display Axis")    
    vbox.addWidget(self.check1)
    self.check1.setChecked(glwidget.axis_disp)
    self.check2 = QtWidgets.QCheckBox("Display Colormap")    
    vbox.addWidget(self.check2)
    self.check2.setChecked(glwidget.cmp_disp)
    self.check3 = QtWidgets.QCheckBox("Display Step")    
    vbox.addWidget(self.check3)
    self.check3.setChecked(glwidget.step_disp)   
    self.buttonb = QtWidgets.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def SetTable(self):
    self.table.setHorizontalHeaderLabels(['Type', 'Display'])
    for row in range(self.glwidget.grid.ntype):
      item = QtWidgets.QTableWidgetItem(str(row))
      self.table.setItem(row, 0, item)
      item = QtWidgets.QTableWidgetItem()
      item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
      if self.glwidget.draw.get_disp(row) == 1:
        item.setCheckState(QtCore.Qt.Checked)
      else:
        item.setCheckState(QtCore.Qt.Unchecked)
      self.table.setItem(row, 1, item)

  def Accept(self):
    self.glwidget.draw.method = self.combo.currentIndex()
    for row in range(self.table.rowCount()):
      item = self.table.item(row, 1)
      if item.checkState() == QtCore.Qt.Checked:
        self.glwidget.draw.set_disp(row, 1)
      else:
        self.glwidget.draw.set_disp(row, 0)
    self.glwidget.axis_disp = self.check1.isChecked()
    self.glwidget.cmp_disp = self.check2.isChecked()
    self.glwidget.step_disp = self.check3.isChecked()
    self.glwidget.cmpRange()
    self.glwidget.updateGL()
    self.accept()

"""
ProfileDialog
""" 
class ProfileCanvas(FigureCanvas):
  def __init__(self, parent=None, width=5, height=4, dpi=100):
    self.fig = Figure(figsize=(width, height), dpi=dpi)
    self.axes = self.fig.add_subplot(111)
    FigureCanvas.__init__(self, self.fig)
    self.setParent(parent)
    FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

  def drawGraph(self, grid, di, s1, s2):
    vals = np.zeros(grid.size[di], np.float64)
    if di == 0:
      for x in range(grid.size[di]):
        vals[x] = grid.get_val((x, s1, s2))
    elif di == 1:
      for y in range(grid.size[di]):
        vals[y] = grid.get_val((s1, y, s2))
    elif di == 2:
      for z in range(grid.size[di]):
        vals[z] = grid.get_val((s1, s2, z))
    self.axes.cla()
    self.axes.plot(range(grid.size[di]), vals, 'k-')
    self.draw()
    
  def saveGraph(self, fname):
    self.fig.savefig(fname)

class ProfileDialog(QtWidgets.QDialog):
  def __init__(self, parent, grid, di):
    QtWidgets.QDialog.__init__(self, parent)
    self.grid = grid
    self.di = di
    title = ['Profile X', 'Profile Y', 'Profile Z']    
    self.setWindowTitle(title[di])
    vbox = QtWidgets.QVBoxLayout(self)
    self.canvas = ProfileCanvas()
    vbox.addWidget(self.canvas)
    hbox1 = QtWidgets.QHBoxLayout()
    vbox.addLayout(hbox1)
    spin1_text = ['Y : ', 'X : ', 'X : ']
    spin1_max = [grid.size[1] - 1, grid.size[0] - 1, grid.size[0] - 1]    
    spin2_text = ['Z : ', 'Z : ', 'Y : ']
    spin2_max = [grid.size[2] - 1, grid.size[2] - 1, grid.size[1] - 1]
    self.spin1 = self.SpinBox(spin1_max[di])
    self.spin1.setPrefix(spin1_text[di])
    self.spin1.valueChanged[int].connect(self.SpinChanged)
    hbox1.addWidget(self.spin1)
    self.spin2 = self.SpinBox(spin2_max[di])
    self.spin2.setPrefix(spin2_text[di])
    self.spin2.valueChanged[int].connect(self.SpinChanged)
    hbox1.addWidget(self.spin2)
    hbox2 = QtWidgets.QHBoxLayout()
    hbox2.addStretch(1)
    vbox.addLayout(hbox2)
    button1 = QtWidgets.QPushButton("Save Fig")
    button1.clicked.connect(self.saveFig)
    hbox2.addWidget(button1)
    button2 = QtWidgets.QPushButton("Close")
    button2.clicked.connect(self.reject)
    hbox2.addWidget(button2)
    self.canvas.drawGraph(grid, di, self.spin1.value(), self.spin2.value())

  def SpinBox(self, max):
    spin = QtWidgets.QSpinBox()
    spin.setMaximum(max)
    spin.setMinimumWidth(50)
    return spin
    
  def SpinChanged(self):
    self.canvas.drawGraph(self.grid, self.di, self.spin1.value(), self.spin2.value())

  def saveFig(self):
    fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Fig')[0]
    if fname:
      self.canvas.saveGraph(str(fname)) 


"""
Overall Coef
""" 
class OverallCoefDialog(QtWidgets.QDialog):
  def __init__(self, parent, cx, cy, cz):
    QtWidgets.QDialog.__init__(self, parent)
    self.setWindowTitle("Overall Coef")
    vbox = QtWidgets.QVBoxLayout(self)
    linedx = self.LineEdit('X', cx)
    vbox.addWidget(linedx)
    linedy = self.LineEdit('Y', cy)
    vbox.addWidget(linedy)
    linedz = self.LineEdit('Z', cz)
    vbox.addWidget(linedz)
    button = QtWidgets.QPushButton("Close")
    button.clicked.connect(self.close)
    vbox.addWidget(button)

  def LineEdit(self, label, val):
    lined = QtWidgets.QLineEdit()
    lined.setText('{} : {}'.format(label, val))
    lined.setReadOnly(True)
    return lined

"""
MainWindow
"""    
class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    QtWidgets.QWidget.__init__(self, parent)
    self.setWindowTitle(self.tr("MPGridViewer"))
    self.glwidget = GLWidget()
    self.setCentralWidget(self.glwidget)
    self.MainMenuBar()
    self.MainToolBar()
    self.compress = 8

  def MainMenuBar(self):
    menubar = QtWidgets.QMenuBar(self)
    self.setMenuBar(menubar)
    file_menu = QtWidgets.QMenu('File', self)
    file_menu.addAction('New', self.fileNew)
    file_menu.addAction('New from Image', self.fileFromImage)   
    file_menu.addAction('Open', self.fileOpen)
    file_menu.addAction('Save', self.fileSave)
    file_menu.addAction('Save Image', self.fileSaveImage)
    file_menu.addAction('Quit', QtCore.QCoreApplication.instance().quit)   
    menubar.addMenu(file_menu)
    view_menu = QtWidgets.QMenu('View', self)
    view_menu.addAction('Draw Setting', self.drawDialog)
    view_menu.addAction('Draw Range', self.drawrangeDialog)   
    view_menu.addAction('Color', self.colorDialog)
    menubar.addMenu(view_menu)
    grid_menu = QtWidgets.QMenu('Grid', self)
    grid_menu.addAction('Element Size', self.elementDialog)
    grid_menu.addAction('Boundary Condition', self.boundDialog)
    grid_menu.addAction('Inter-Coef Setting', self.intercoefDialog)
    grid_menu.addAction('Rhoc Setting', self.rhocDialog)
    fill_menu = QtWidgets.QMenu('Fill', self)
    fill_menu.addAction('Type', self.fillDialog)
    fill_menu.addAction('Update', self.fillDialog)
    fill_menu.addAction('Val', self.fillDialog)
    grid_menu.addMenu(fill_menu)
    ellip_menu = QtWidgets.QMenu('Ellipsoid', self)
    ellip_menu.addAction('Type', self.ellipDialog)
    ellip_menu.addAction('Update', self.ellipDialog)
    ellip_menu.addAction('Val', self.ellipDialog)
    grid_menu.addMenu(ellip_menu)    
    cyl_menu = QtWidgets.QMenu('Cylinder', self)
    cyl_menu.addAction('Type', self.cylDialog)
    cyl_menu.addAction('Update', self.cylDialog)
    cyl_menu.addAction('Val', self.cylDialog)
    grid_menu.addMenu(cyl_menu)
    grid_menu.addAction('Ref Local Coef', self.refLocalCoef)
    grid_menu.addAction('Solve', self.solveDialog)
    grid_menu.addAction('Overall Coef', self.overallCoef)
    menubar.addMenu(grid_menu)
    ana_menu = QtWidgets.QMenu('Analysis', self)
    pro_menu = QtWidgets.QMenu('Profile', self)
    pro_menu.addAction('X', self.profileDialog)
    pro_menu.addAction('Y', self.profileDialog)
    pro_menu.addAction('Z', self.profileDialog)
    ana_menu.addMenu(pro_menu)
    menubar.addMenu(ana_menu)

  def fileNew(self):
    dlg = NewGridDialog(self)
    if dlg.exec_():
      self.glwidget.grid = dlg.newGrid()
      region = self.glwidget.draw.region(self.glwidget.grid)
      self.glwidget.model = MPGLGrid.model((0,0,1,0,1,0), region)
      self.glwidget.cmp.range = (0.0, 0.0)
      self.glwidget.updateGL()

  def fileFromImage(self):
    dlg = FromImageDialog(self)
    if dlg.exec_():
      self.glwidget.grid = dlg.newGrid()
      region = self.glwidget.draw.region(self.glwidget.grid)
      self.glwidget.model = MPGLGrid.model((0,0,1,0,1,0), region)
      self.glwidget.cmp.range = (0.0, 0.0)
      self.glwidget.updateGL()

  def fileOpen(self):
    fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0]
    if fname:
      self.glwidget.grid = MPGrid.read(str(fname))
      region = self.glwidget.draw.region(self.glwidget.grid)
      self.glwidget.model = MPGLGrid.model((0,0,1,0,1,0), region)
      self.glwidget.cmpRange()
      self.glwidget.updateGL()

  def fileSave(self):
    if self.glwidget.grid:
      fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file')[0]
      if fname:
        self.glwidget.grid.write(str(fname), self.compress)

  def fileSaveImage(self):
    if self.glwidget.grid:
      fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save image')[0]
      if fname:      
        img = self.glwidget.screenShot()
        cv2.imwrite(str(fname), img)

  def fillDialog(self):
    if self.glwidget.grid:
      dlg = FillDialog(self, self.glwidget.grid, 'Fill', self.sender().text())
      ok = dlg.exec_()
      if ok:
        self.glwidget.cmpRange()
        self.glwidget.updateGL()

  def ellipDialog(self):
    if self.glwidget.grid:
      dlg = FillDialog(self, self.glwidget.grid, 'Ellipsoid', self.sender().text())
      ok = dlg.exec_()
      if ok:
        self.glwidget.cmpRange()
        self.glwidget.updateGL()      

  def cylDialog(self):
    if self.glwidget.grid:
      dlg = FillDialog(self, self.glwidget.grid, 'Cylinder', self.sender().text())
      ok = dlg.exec_()
      if ok:
        self.glwidget.cmpRange()
        self.glwidget.updateGL()

  def intercoefDialog(self):
    if self.glwidget.grid:
      dlg = InterCoefDialog(self, self.glwidget.grid)
      dlg.exec_()

  def rhocDialog(self):
    if self.glwidget.grid:
      dlg = RhocDialog(self, self.glwidget.grid)
      dlg.exec_()

  def elementDialog(self):
    if self.glwidget.grid:
      dlg = ElementDialog(self, self.glwidget.grid)
      dlg.exec_()

  def boundDialog(self):
    if self.glwidget.grid:
      dlg = BoundDialog(self, self.glwidget.grid)
      dlg.exec_()

  def drawrangeDialog(self):
    dlg = DrawRangeDialog(self, self.glwidget)
    dlg.exec_()

  def drawDialog(self):
    if self.glwidget.grid:
      dlg = DrawDialog(self, self.glwidget)
      dlg.exec_()

  def colorDialog(self):
    dlg = ColorDialog(self, self.glwidget)
    dlg.exec_()

  def refLocalCoef(self):
    if self.glwidget.grid:
      ret = QtWidgets.QMessageBox.question(self, 'Ref Local Coef', "Reflect Local Coefficient?",\
                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
      if (ret == QtWidgets.QMessageBox.Yes):
        self.glwidget.grid.ref_local_coef_all()
        self.glwidget.cmpRange()
        self.glwidget.updateGL()

  def solveDialog(self):
    if self.glwidget.grid:
      dlg = SolveDialog(self, self.glwidget)
      ok = dlg.exec_()
      if ok:
        self.glwidget.cmpRange()
        self.glwidget.updateGL()

  def overallCoef(self):
    if self.glwidget.grid:
      elm = self.glwidget.grid.element
      cx = self.glwidget.grid.overall_coef(0, 1.0/elm[0])
      cy = self.glwidget.grid.overall_coef(1, 1.0/elm[1])
      cz = self.glwidget.grid.overall_coef(2, 1.0/elm[2])
      dlg = OverallCoefDialog(self, cx, cy, cz)
      dlg.exec_()

  def profileDialog(self):
    if self.glwidget.grid:
      txt = self.sender().text()
      if txt == 'X':
        dlg = ProfileDialog(self, self.glwidget.grid, 0)
      elif txt == 'Y':
        dlg = ProfileDialog(self, self.glwidget.grid, 1)
      elif txt == 'Z':
        dlg = ProfileDialog(self, self.glwidget.grid, 2)
      dlg.exec_()

  def MainToolBar(self):
    toolbar = QtWidgets.QToolBar(self)
    toolbar.addAction('Reset', self.resetModel)
    toolbar.addAction('Fit', self.fitModel)    
    toolbar.addSeparator()    
    group1 = QtWidgets.QButtonGroup(self)
    button1 = ToolButton('Rot', self.setMouseMode)
    button1.toggle()
    group1.addButton(button1)
    toolbar.addWidget(button1)
    button2 = ToolButton('Trans', self.setMouseMode)
    group1.addButton(button2)
    toolbar.addWidget(button2)
    button3 = ToolButton('Zoom', self.setMouseMode)
    group1.addButton(button3)
    toolbar.addWidget(button3)
    toolbar.addSeparator()
    group2 = QtWidgets.QButtonGroup(self)
    button4 = ToolButton('Type', self.setDrawKind)
    button4.toggle()
    group2.addButton(button4)
    toolbar.addWidget(button4)
    button5 = ToolButton('Update', self.setDrawKind)
    group2.addButton(button5)
    toolbar.addWidget(button5)
    button6 = ToolButton('Val', self.setDrawKind)
    group2.addButton(button6)
    toolbar.addWidget(button6)
    button7 = ToolButton('Cx', self.setDrawKind)
    group2.addButton(button7)
    toolbar.addWidget(button7)
    button8 = ToolButton('Cy', self.setDrawKind)
    group2.addButton(button8)
    toolbar.addWidget(button8)
    button9 = ToolButton('Cz', self.setDrawKind)
    group2.addButton(button9)
    toolbar.addWidget(button9)
    self.addToolBar(toolbar)

  def setMouseMode(self, pressed):
    if self.glwidget.model:
      txt = self.sender().text()
      if txt == "Rot":
        self.glwidget.model.button_mode = 0
      elif txt == "Trans":
        self.glwidget.model.button_mode = 1 
      elif txt == "Zoom":
        self.glwidget.model.button_mode = 2

  def setDrawKind(self, pressed):
    txt = self.sender().text()
    if txt == "Type":
      self.glwidget.draw.kind = 0
    elif txt == "Update":
      self.glwidget.draw.kind = 1 
    elif txt == "Val":
      self.glwidget.draw.kind = 2
      self.glwidget.cmpRange()
    elif txt == "Cx":
      self.glwidget.draw.kind = 3
      self.glwidget.cmpRange()
    elif txt == "Cy":
      self.glwidget.draw.kind = 4
      self.glwidget.cmpRange()
    elif txt == "Cz":
      self.glwidget.draw.kind = 5
      self.glwidget.cmpRange()
    self.glwidget.updateGL()

  def resetModel(self):
    if self.glwidget.model:
      self.glwidget.model.reset()
      self.glwidget.updateGL()

  def fitModel(self):
    if self.glwidget.model:
      self.glwidget.model.fit()
      self.glwidget.updateGL()

class ToolButton(QtWidgets.QToolButton):
  def __init__(self, text, func):
    super(ToolButton, self).__init__()
    self.setText(text)
    self.clicked[bool].connect(func)
    self.setCheckable(True)

if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())