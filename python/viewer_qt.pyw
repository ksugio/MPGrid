#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Thu Jan 28 12:04:57 2016

@author: Kenjiro Sugio
"""

import MPGrid
import MPGLGrid
import sys
import math
import numpy as np
from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL
from PIL import Image
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

"""
GLWidget Class
"""
class GLWidget(QtOpenGL.QGLWidget):
  def __init__(self, parent=None):
    QtOpenGL.QGLWidget.__init__(self, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)
    self.lastPos = QtCore.QPoint()
    self.mouseMode = 0
    self.colorMode = [0, 0]
    self.grid = None
    self.draw = MPGLGrid.draw()
    self.scene = MPGLGrid.scene()
    self.model = MPGLGrid.model()
    self.cmp = MPGLGrid.colormap()
    self.axis_disp = True
    self.cmp_disp = True
    self.step_disp = True
    self.__width = 800
    self.__height = 600

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
        GL.glPushMatrix()
        GL.glTranslate((2.0 - self.__width) / self.__height, -self.cmp.size[1]/2.0, self.scene.znear - 1.0e-6)
        self.cmp.draw()
        GL.glPopMatrix()
      if self.step_disp:
        self.drawStep()
    
  def resizeGL(self, width, height):
    self.__width = width
    self.__height = height
    self.scene.resize(width, height)

  def mousePressEvent(self, event):
    self.lastPos = QtCore.QPoint(event.pos())

  def mouseReleaseEvent(self, event):
    self.model.inverse()

  def mouseMoveEvent(self, event):
    dx = event.x() - self.lastPos.x()
    dy = event.y() - self.lastPos.y()
    mod = QtGui.QApplication.keyboardModifiers()
    if event.buttons() & QtCore.Qt.LeftButton:
        if self.mouseMode == 0:
            if mod == QtCore.Qt.ControlModifier:
                cx = self.__width / 2
                cy = self.__height / 2
                if event.x() <= cx and event.y() <= cy:
                    az = math.pi * (-dx + dy) / self.__height
                elif event.x() > cx and event.y() <= cy:
                    az = math.pi * (-dx - dy) / self.__height
                elif event.x() <= cx and event.y() > cy:
                    az = math.pi * (dx + dy) / self.__height
                elif event.x() > cx and event.y() > cy:
                    az = math.pi * (dx - dy) / self.__height
                self.model.rot_z(-az)
            else:
                ay = math.pi * dx / self.__height
                self.model.rot_y(-ay)
                ax = math.pi *dy / self.__height
                self.model.rot_x(-ax)
        elif self.mouseMode == 1:
            if mod == QtCore.Qt.ControlModifier:
                mz = 2.0 * dy / self.__height
                self.model.trans_z(-mz)
            else:
                mx = 2.0 * dx / self.__height
                self.model.trans_x(mx)
                my = 2.0 * dy / self.__height
                self.model.trans_y(-my)
        elif self.mouseMode == 2:
            s = 1.0 - float(dy) / self.__height
            self.model.zoom(s)
        self.updateGL()
        self.lastPos = QtCore.QPoint(event.pos())
        
  def gridFit(self):
    self.draw.fit(self.grid, self.__width, self.__height, self.model)

  def cmpRange(self):
    self.draw.cmp_range(self.grid, self.cmp)    

  def screenShot(self):
    screenshot = GL.glReadPixels(0, 0, self.width(), self.height(), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
    img = Image.frombuffer("RGBA", (self.width(), self.height()), screenshot, "raw", "RGBA", 0, 0)
    return img
    
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
    
  def drawStep(self):
    s = str(self.grid.step) + ' step'
    GL.glPushAttrib(GL.GL_LIGHTING_BIT)
    GL.glDisable(GL.GL_LIGHTING)
    GL.glRasterPos3d((2.0 * 10 - self.__width) / self.__height,\
      2.0*(self.__height - 20) / self.__height - 1.0, self.scene.znear - 1.0e-6)
    GL.glColor3fv(self.cmp.font_color)    
    MPGLGrid.text_bitmap(s, self.cmp.font_type)
    GL.glPopAttrib()

"""
FillDialog
""" 
class FillDialog(QtGui.QDialog):
  def __init__(self, parent, grid, method, item):
    QtGui.QDialog.__init__(self, parent)
    self.grid = grid
    self.method = method
    self.item = item
    self.setWindowTitle(method + " " + item)
    vbox = QtGui.QVBoxLayout(self)
    hbox1 = QtGui.QHBoxLayout()
    vbox.addLayout(hbox1)
    label1 = QtGui.QLabel()
    label1.setText(item)
    hbox1.addWidget(label1)
    if item == 'Type':
      self.spin = QtGui.QSpinBox()
      hbox1.addWidget(self.spin)
      self.spin.setMaximum(grid.ntype-1)
    elif item == 'Update':
      self.combo1 = QtGui.QComboBox()
      hbox1.addWidget(self.combo1)
      self.combo1.addItem('False')
      self.combo1.addItem('True')
    elif item == 'Val':
      self.lined = QtGui.QLineEdit()
      hbox1.addWidget(self.lined)
    glay = QtGui.QGridLayout()
    vbox.addLayout(glay)
    label2 = QtGui.QLabel()
    label2.setText("Start (x0, y0, z0)")
    glay.addWidget(label2, 0, 0)
    self.spinx0 = self.SpinBox(grid.size[0]-1)
    glay.addWidget(self.spinx0, 0, 1)
    self.spiny0 = self.SpinBox(grid.size[1]-1)
    glay.addWidget(self.spiny0, 0, 2)
    self.spinz0 = self.SpinBox(grid.size[2]-1)
    glay.addWidget(self.spinz0, 0, 3)
    label3 = QtGui.QLabel(self)
    label3.setText("End (x1, y1, z1)")
    glay.addWidget(label3, 1, 0)
    self.spinx1 = self.SpinBox(grid.size[0]-1)
    glay.addWidget(self.spinx1, 1, 1)
    self.spiny1 = self.SpinBox(grid.size[1]-1)
    glay.addWidget(self.spiny1, 1, 2)
    self.spinz1 = self.SpinBox(grid.size[2]-1)
    glay.addWidget(self.spinz1, 1, 3)
    if method == 'Cylinder':
      hbox2 = QtGui.QHBoxLayout()
      vbox.addLayout(hbox2)  
      label4 = QtGui.QLabel(self)
      label4.setText("Direction")
      hbox2.addWidget(label4)
      self.combo2 = QtGui.QComboBox()
      hbox2.addWidget(self.combo2)
      self.combo2.addItem('x')
      self.combo2.addItem('y')
      self.combo2.addItem('z')
    self.button = QtGui.QDialogButtonBox()
    vbox.addWidget(self.button)
    self.button.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.button.accepted.connect(self.Accept)
    self.button.rejected.connect(self.reject)

  def SpinBox(self, max):
    spin = QtGui.QSpinBox()
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
        val = self.lined.text().toDouble()
        if val[1]:
          self.grid.fill_val(val[0], (x0, y0, z0), (x1, y1, z1))
    elif self.method == 'Ellipsoid':
      if self.item == 'Type':
        self.grid.ellipsoid_type(self.spin.value(), (x0, y0, z0), (x1, y1, z1))
      elif self.item == 'Update':
        if self.combo1.currentIndex() == 0:
          self.grid.ellipsoid_update(0, (x0, y0, z0), (x1, y1, z1))
        elif self.combo1.currentIndex() == 1:
          self.grid.ellipsoid_update(1, (x0, y0, z0), (x1, y1, z1))
      elif self.item == 'Val':
        val = self.lined.text().toDouble()
        if val[1]:
          self.grid.ellipsoid_val(val[0], (x0, y0, z0), (x1, y1, z1))
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
        val = self.lined.text().toDouble()
        if val[1]:
          self.grid.cylinder_val(val[0], (x0, y0, z0), (x1, y1, z1), di)
    self.accept()

"""
NewGridDialog
""" 
class NewGridDialog(QtGui.QDialog):
  def __init__(self, parent):
    QtGui.QDialog.__init__(self, parent)
    self.setWindowTitle("New Grid")
    vbox = QtGui.QVBoxLayout(self)
    hbox1 = QtGui.QHBoxLayout()
    vbox.addLayout(hbox1)
    label1 = QtGui.QLabel()
    label1.setText('nx, ny, nz')
    hbox1.addWidget(label1)
    self.spinnx = self.SpinBox(2000)
    hbox1.addWidget(self.spinnx)
    self.spinny = self.SpinBox(2000)
    hbox1.addWidget(self.spinny)
    self.spinnz = self.SpinBox(2000)
    hbox1.addWidget(self.spinnz)
    hbox2 = QtGui.QHBoxLayout()
    vbox.addLayout(hbox2)
    label2 = QtGui.QLabel()
    label2.setText('ntype')
    hbox2.addWidget(label2)
    self.spinntype = self.SpinBox(100)
    hbox2.addWidget(self.spinntype)
    self.button = QtGui.QDialogButtonBox()
    vbox.addWidget(self.button)
    self.button.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.button.accepted.connect(self.accept)
    self.button.rejected.connect(self.reject)

  def SpinBox(self, max):
    spin = QtGui.QSpinBox()
    spin.setMinimum(1)
    spin.setMaximum(max)
    spin.setMinimumWidth(50)
    return spin    

  @staticmethod
  def newGrid(self):
    dlg = NewGridDialog(self)
    ok = dlg.exec_()
    if ok:
      nx = dlg.spinnx.value()
      ny = dlg.spinny.value()
      nz = dlg.spinnz.value()
      ntype = dlg.spinntype.value()
      grid = MPGrid.new(nx, ny, nz, ntype)
      return grid
    else:
      return None

"""
InterCoefDialog
""" 
class InterCoefDialog(QtGui.QDialog):
  def __init__(self, parent, grid):
    QtGui.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Interface and Coefficient Setting")
    vbox = QtGui.QVBoxLayout(self)
    self.table = QtGui.QTableWidget(grid.ntype*grid.ntype, 7)
    self.SetTable()
    self.table.cellClicked[int,int].connect(self.cellClicked)
    vbox.addWidget(self.table)
    hbox = QtGui.QHBoxLayout()
    vbox.addLayout(hbox)
    self.combo1 = QtGui.QComboBox()
    self.combo1.setMaximumWidth(80)
    for i in range(grid.ntype):
      for j in range(grid.ntype):
        self.combo1.addItem('Type '+str(i)+', '+str(j))
    hbox.addWidget(self.combo1)
    self.combo2 = QtGui.QComboBox()
    self.combo2.setMaximumWidth(80)
    self.combo2.addItem('Cond')
    self.combo2.addItem('Trans')
    hbox.addWidget(self.combo2)
    self.lined1 = QtGui.QLineEdit()
    hbox.addWidget(self.lined1)
    self.button = QtGui.QPushButton('Set')
    self.button.clicked.connect(self.SetInterCoef1)
    hbox.addWidget(self.button)
    self.buttonb = QtGui.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def cellClicked(self, row, col):
    self.combo1.setCurrentIndex(row)

  def SetInterCoef1(self):
    row = self.combo1.currentIndex()
    item = QtGui.QTableWidgetItem(self.combo2.currentText())
    self.table.setItem(row, 1, item)
    item = QtGui.QTableWidgetItem(self.combo2.currentText())
    self.table.setItem(row, 2, item)
    item = QtGui.QTableWidgetItem(self.combo2.currentText())
    self.table.setItem(row, 3, item)
    item = QtGui.QTableWidgetItem(self.lined1.text())
    self.table.setItem(row, 4, item)
    item = QtGui.QTableWidgetItem(self.lined1.text())
    self.table.setItem(row, 5, item)
    item = QtGui.QTableWidgetItem(self.lined1.text())
    self.table.setItem(row, 6, item)

  def minimumSizeHint(self):
    return QtCore.QSize(320, 240)

  def sizeHint(self):
    return QtCore.QSize(640, 480)

  def SetInterCoef(self, row, inter, coef):
    if inter[0] == 0:
      item = QtGui.QTableWidgetItem("Cond")
      self.table.setItem(row, 1, item)
    elif inter[0] == 1:
      item = QtGui.QTableWidgetItem("Trans")
      self.table.setItem(row, 1, item)
    if inter[1] == 0:
      item = QtGui.QTableWidgetItem("Cond")
      self.table.setItem(row, 2, item)
    elif inter[1] == 1:
      item = QtGui.QTableWidgetItem("Trans")
      self.table.setItem(row, 2, item)
    if inter[2] == 0:
      item = QtGui.QTableWidgetItem("Cond")
      self.table.setItem(row, 3, item)
    elif inter[2] == 1:
      item = QtGui.QTableWidgetItem("Trans")
      self.table.setItem(row, 3, item)
    item = QtGui.QTableWidgetItem(str(coef[0]))
    self.table.setItem(row, 4, item)
    item = QtGui.QTableWidgetItem(str(coef[1]))
    self.table.setItem(row, 5, item)
    item = QtGui.QTableWidgetItem(str(coef[2]))
    self.table.setItem(row, 6, item)
  
  def SetTable(self):
    labels = QtCore.QStringList()
    labels.append("Type i, j")
    labels.append("Inter x")
    labels.append("Inter y")
    labels.append("Inter z")
    labels.append("Coef x")
    labels.append("Coef y")
    labels.append("Coef z")
    self.table.setHorizontalHeaderLabels(labels)
    row = 0
    for i in range(self.grid.ntype):
      for j in range(self.grid.ntype):
        item = QtGui.QTableWidgetItem(str(i)+', '+str(j))
        self.table.setItem(row, 0, item)
        inter = self.grid.get_inter(i, j)
        coef = self.grid.get_coef(i, j)
        self.SetInterCoef(row, inter, coef)
        row = row + 1

  def Accept(self):
    for row in range(self.table.rowCount()):
      inter = [0, 0, 0]
      if self.table.item(row, 1).text().compare("Trans") == 0:
        inter[0] = 1
      if self.table.item(row, 2).text().compare("Trans") == 0:
        inter[1] = 1  
      if self.table.item(row, 3).text().compare("Trans") == 0:
        inter[2] = 1
      coef_x = self.table.item(row, 4).text().toDouble()
      coef_y = self.table.item(row, 5).text().toDouble()
      coef_z = self.table.item(row, 6).text().toDouble()
      if coef_x[1] and coef_y[1] and coef_z[1]:
          coef = [coef_x[0], coef_y[0], coef_z[0]]
          i = row / self.grid.ntype
          j = row - i*self.grid.ntype
          self.grid.set_inter_coef3(inter, coef, i, j)
      self.accept()

"""
RhocDialog
""" 
class RhocDialog(QtGui.QDialog):
  def __init__(self, parent, grid):
    QtGui.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Rhoc Setting")
    vbox = QtGui.QVBoxLayout(self)
    self.table = QtGui.QTableWidget(grid.ntype, 2)
    self.SetTable()
    vbox.addWidget(self.table)
    self.buttonb = QtGui.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def SetTable(self):
    labels = QtCore.QStringList()
    labels.append("Type")
    labels.append("Rhoc")
    self.table.setHorizontalHeaderLabels(labels)
    for row in range(self.grid.ntype):
      item = QtGui.QTableWidgetItem(str(row))
      self.table.setItem(row, 0, item)
      rhoc = self.grid.get_rhoc(row)
      item = QtGui.QTableWidgetItem(str(rhoc))
      self.table.setItem(row, 1, item)

  def Accept(self):
    for row in range(self.table.rowCount()):
      rhoc = self.table.item(row, 1).text().toDouble()
      if rhoc[1]:
        self.grid.set_rhoc(rhoc[0], row)
    self.accept()

"""
ElementDialog
""" 
class ElementDialog(QtGui.QDialog):
  def __init__(self, parent, grid):
    QtGui.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Element Size")
    vbox = QtGui.QVBoxLayout(self)
    label = QtGui.QLabel()
    label.setText('ex, ey, ez')
    vbox.addWidget(label)
    hbox = QtGui.QHBoxLayout()
    vbox.addLayout(hbox)
    self.lined1 = self.LineEdit(str(grid.element[0]))
    hbox.addWidget(self.lined1)
    self.lined2 = self.LineEdit(str(grid.element[1]))
    hbox.addWidget(self.lined2)
    self.lined3 = self.LineEdit(str(grid.element[2]))
    hbox.addWidget(self.lined3)
    self.buttonb = QtGui.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def LineEdit(self, text):
    lined = QtGui.QLineEdit()
    lined.setText(text)
    lined.setMaximumWidth(60)
    return lined

  def Accept(self):
    ex = self.lined1.text().toDouble()
    ey = self.lined2.text().toDouble()
    ez = self.lined3.text().toDouble()
    if ex[1] and ey[1] and ez[1]:
      self.grid.element = (ex[0], ey[0], ez[0])
    self.accept()

"""
BoundDialog
""" 
class BoundDialog(QtGui.QDialog):
  def __init__(self, parent, grid):
    QtGui.QDialog.__init__(self, parent)
    self.grid = grid
    self.setWindowTitle("Boundary Condition")
    vbox = QtGui.QVBoxLayout(self)
    glay = QtGui.QGridLayout()
    vbox.addLayout(glay)
    label1 = QtGui.QLabel()
    label1.setText('Lower (xl, yl, zl)')
    glay.addWidget(label1, 0, 0)
    self.combo1 = self.ComboBox(grid.bound[0])
    glay.addWidget(self.combo1, 0, 1)
    self.combo2 = self.ComboBox(grid.bound[1])
    glay.addWidget(self.combo2, 0, 2)
    self.combo3 = self.ComboBox(grid.bound[2])
    glay.addWidget(self.combo3, 0, 3)
    label2 = QtGui.QLabel()
    label2.setText('Upper (xu, yu, zu)')
    glay.addWidget(label2, 1, 0)
    self.combo4 = self.ComboBox(grid.bound[3])
    glay.addWidget(self.combo4, 1, 1)
    self.combo5 = self.ComboBox(grid.bound[4])
    glay.addWidget(self.combo5, 1, 2)
    self.combo6 = self.ComboBox(grid.bound[5])
    glay.addWidget(self.combo6, 1, 3)
    self.buttonb = QtGui.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def ComboBox(self, bd):
    combo = QtGui.QComboBox()
    combo.addItem("Adiabatic")
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
class DrawRangeDialog(QtGui.QDialog):
  def __init__(self, parent, glwidget):
    QtGui.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.setWindowTitle("Draw Range")
    vbox = QtGui.QVBoxLayout(self)
    glay = QtGui.QGridLayout()
    vbox.addLayout(glay)
    label1 = QtGui.QLabel()
    label1.setText("Start (x0, y0, z0)")
    glay.addWidget(label1, 0, 0)
    self.spinx0 = self.SpinBox(glwidget.draw.range[0])
    glay.addWidget(self.spinx0, 0, 1)
    self.spiny0 = self.SpinBox(glwidget.draw.range[1])
    glay.addWidget(self.spiny0, 0, 2)
    self.spinz0 = self.SpinBox(glwidget.draw.range[2])
    glay.addWidget(self.spinz0, 0, 3)
    label2 = QtGui.QLabel(self)
    label2.setText("End (x1, y1, z1)")
    glay.addWidget(label2, 1, 0)
    self.spinx1 = self.SpinBox(glwidget.draw.range[3])
    glay.addWidget(self.spinx1, 1, 1)
    self.spiny1 = self.SpinBox(glwidget.draw.range[4])
    glay.addWidget(self.spiny1, 1, 2)
    self.spinz1 = self.SpinBox(glwidget.draw.range[5])
    glay.addWidget(self.spinz1, 1, 3)
    self.button = QtGui.QDialogButtonBox()
    vbox.addWidget(self.button)
    self.button.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.button.accepted.connect(self.Accept)
    self.button.rejected.connect(self.reject)

  def SpinBox(self, val):
    spin = QtGui.QSpinBox()
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
class ColorDialog(QtGui.QDialog):
  def __init__(self, parent, glwidget):
    QtGui.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.setWindowTitle("Color")
    vbox = QtGui.QVBoxLayout(self)
    hbox1 = QtGui.QHBoxLayout()
    vbox.addLayout(hbox1)
    label1 = QtGui.QLabel()
    label1.setText("Background")
    hbox1.addWidget(label1)
    self.combo1 = QtGui.QComboBox()
    self.combo1.addItem("Black")
    self.combo1.addItem("White")
    self.combo1.setCurrentIndex(glwidget.colorMode[0])
    hbox1.addWidget(self.combo1)
    hbox2 = QtGui.QHBoxLayout()
    vbox.addLayout(hbox2)
    label2 = QtGui.QLabel()
    label2.setText("Colormap")
    hbox2.addWidget(label2)
    self.combo2 = QtGui.QComboBox()
    self.combo2.addItem("Color")
    self.combo2.addItem("Grayscale")
    self.combo2.setCurrentIndex(glwidget.colorMode[1])
    hbox2.addWidget(self.combo2)
    self.buttonb = QtGui.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def Accept(self):
    self.glwidget.setColorMode(self.combo1.currentIndex(), self.combo2.currentIndex())
    self.accept()

"""
SolveDialog
""" 
class SolveDialog(QtGui.QDialog):
  def __init__(self, parent, glwidget):
    QtGui.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.grid = None
    self.setWindowTitle("Solve")
    vbox = QtGui.QVBoxLayout(self)
    self.texted = QtGui.QTextEdit()
    self.texted.setReadOnly(True)
    vbox.addWidget(self.texted)
    glay = QtGui.QGridLayout()
    vbox.addLayout(glay)
    label1 = QtGui.QLabel()
    label1.setText("Dt")
    glay.addWidget(label1, 0, 0)
    self.lined1 = QtGui.QLineEdit()
    self.lined1.setText(str(glwidget.grid.estimate_dt()))
    glay.addWidget(self.lined1, 0, 1)
    label2 = QtGui.QLabel()
    label2.setText("Interval")
    glay.addWidget(label2, 1, 0)
    self.spin1 = QtGui.QSpinBox()
    self.spin1.setMinimum(1)
    self.spin1.setMaximum(1000)
    glay.addWidget(self.spin1, 1, 1)
    label3 = QtGui.QLabel()
    label3.setText("Finish Dv")
    glay.addWidget(label3, 2, 0)
    self.lined2 = QtGui.QLineEdit()
    self.lined2.setText("1.0e-12")
    glay.addWidget(self.lined2, 2, 1)
    hbox1 = QtGui.QHBoxLayout()
    vbox.addLayout(hbox1)
    self.button1 = QtGui.QPushButton("Start/Stop")
    self.button1.setCheckable(True)
    self.button1.clicked.connect(self.solveStartStop)
    hbox1.addWidget(self.button1)    
    self.buttonb = QtGui.QDialogButtonBox()
    hbox1.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.Reject)
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.doSolve)

  def doSolve(self):    
    dv = self.grid.solve(self.dt[0], self.step)
    li = str(self.grid.step) + ', ' + str(dv)
    self.texted.append(li)
    if dv < self.findv[0]:
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
      self.dt = self.lined1.text().toDouble()
      self.step = self.spin1.value()
      self.findv = self.lined2.text().toDouble()
      if self.dt[1] and self.findv[1]:
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
class DrawDialog(QtGui.QDialog):
  def __init__(self, parent, glwidget):
    QtGui.QDialog.__init__(self, parent)
    self.glwidget = glwidget
    self.setWindowTitle("Draw Setting")
    vbox = QtGui.QVBoxLayout(self)
    hbox = QtGui.QHBoxLayout()
    vbox.addLayout(hbox)
    label = QtGui.QLabel()
    label.setText("Draw Method")
    hbox.addWidget(label)    
    self.combo = QtGui.QComboBox()
    self.combo.addItem("Quads")
    self.combo.addItem("Cubes")
    self.combo.setCurrentIndex(glwidget.draw.method) 
    hbox.addWidget(self.combo)
    self.table = QtGui.QTableWidget(glwidget.grid.ntype, 2)
    self.SetTable()
    vbox.addWidget(self.table)
    self.check1 = QtGui.QCheckBox("Display Axis");    
    vbox.addWidget(self.check1);
    self.check1.setChecked(glwidget.axis_disp)
    self.check2 = QtGui.QCheckBox("Display Colormap");    
    vbox.addWidget(self.check2);
    self.check2.setChecked(glwidget.cmp_disp)
    self.check3 = QtGui.QCheckBox("Display Step");    
    vbox.addWidget(self.check3);
    self.check3.setChecked(glwidget.step_disp)   
    self.buttonb = QtGui.QDialogButtonBox()
    vbox.addWidget(self.buttonb)
    self.buttonb.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
    self.buttonb.accepted.connect(self.Accept)
    self.buttonb.rejected.connect(self.reject)

  def SetTable(self):
    labels = QtCore.QStringList()
    labels.append("Type")
    labels.append("Display")
    self.table.setHorizontalHeaderLabels(labels)
    for row in range(self.glwidget.grid.ntype):
      item = QtGui.QTableWidgetItem(str(row))
      self.table.setItem(row, 0, item)
      item = QtGui.QTableWidgetItem()
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
    self.axes.hold(False)
    FigureCanvas.__init__(self, self.fig)
    self.setParent(parent)
    FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
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

class ProfileDialog(QtGui.QDialog):
  def __init__(self, parent, grid, di):
    QtGui.QDialog.__init__(self, parent)
    self.grid = grid
    self.di = di
    title = ['Profile X', 'Profile Y', 'Profile Z']    
    self.setWindowTitle(title[di])
    vbox = QtGui.QVBoxLayout(self)
    self.canvas = ProfileCanvas()
    vbox.addWidget(self.canvas)
    hbox1 = QtGui.QHBoxLayout()
    vbox.addLayout(hbox1)
    spin1_text = ['Y : ', 'X : ', 'X : ']
    spin1_max = [grid.size[1]-1, grid.size[0]-1, grid.size[0]-1]    
    spin2_text = ['Z : ', 'Z : ', 'Y : ']
    spin2_max = [grid.size[2]-1, grid.size[2]-1, grid.size[1]-1]
    self.spin1 = self.SpinBox(spin1_max[di])
    self.spin1.setPrefix(spin1_text[di])
    self.spin1.valueChanged[int].connect(self.SpinChanged)
    hbox1.addWidget(self.spin1)
    self.spin2 = self.SpinBox(spin2_max[di])
    self.spin2.setPrefix(spin2_text[di])
    self.spin2.valueChanged[int].connect(self.SpinChanged)
    hbox1.addWidget(self.spin2)
    hbox2 = QtGui.QHBoxLayout()
    hbox2.addStretch(1)
    vbox.addLayout(hbox2)
    button1 = QtGui.QPushButton("Save Fig")
    button1.clicked.connect(self.saveFig)
    hbox2.addWidget(button1)
    button2 = QtGui.QPushButton("Close")
    button2.clicked.connect(self.reject)
    hbox2.addWidget(button2)
    self.canvas.drawGraph(grid, di, self.spin1.value(), self.spin2.value())

  def SpinBox(self, max):
    spin = QtGui.QSpinBox()
    spin.setMaximum(max)
    spin.setMinimumWidth(50)
    return spin
    
  def SpinChanged(self):
    self.canvas.drawGraph(self.grid, self.di, self.spin1.value(), self.spin2.value())

  def saveFig(self):
    fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Fig')
    if fname:
      self.canvas.saveGraph(str(fname))    

"""
MainWindow
"""    
class MainWindow(QtGui.QMainWindow):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    self.setWindowTitle(self.tr("MPGridViewer"))
    self.glwidget = GLWidget()
    self.setCentralWidget(self.glwidget)
    self.MainMenuBar()
    self.MainToolBar()
    self.compress = 8

  def MainMenuBar(self):
    menubar = QtGui.QMenuBar(self)
    self.setMenuBar(menubar)
    file_menu = QtGui.QMenu('File', self)
    file_menu.addAction('New', self.fileNew)   
    file_menu.addAction('Open', self.fileOpen)
    file_menu.addAction('Save', self.fileSave)
    file_menu.addAction('Save Image', self.fileSaveImage)
    file_menu.addAction('Quit', QtCore.QCoreApplication.instance().quit)   
    menubar.addMenu(file_menu)
    view_menu = QtGui.QMenu('View', self)
    view_menu.addAction('Draw Setting', self.drawDialog)
    view_menu.addAction('Draw Range', self.drawrangeDialog)   
    view_menu.addAction('Color', self.colorDialog)
    menubar.addMenu(view_menu)
    grid_menu = QtGui.QMenu('Grid', self)
    grid_menu.addAction('Element Size', self.elementDialog)
    grid_menu.addAction('Boundary Condition', self.boundDialog)
    grid_menu.addAction('Inter-Coef Setting', self.intercoefDialog)
    grid_menu.addAction('Rhoc Setting', self.rhocDialog)
    fill_menu = QtGui.QMenu('Fill', self)
    fill_menu.addAction('Type', self.fillDialog)
    fill_menu.addAction('Update', self.fillDialog)
    fill_menu.addAction('Val', self.fillDialog)
    grid_menu.addMenu(fill_menu)
    ellip_menu = QtGui.QMenu('Ellipsoid', self)
    ellip_menu.addAction('Type', self.ellipDialog)
    ellip_menu.addAction('Update', self.ellipDialog)
    ellip_menu.addAction('Val', self.ellipDialog)
    grid_menu.addMenu(ellip_menu)    
    cyl_menu = QtGui.QMenu('Cylinder', self)
    cyl_menu.addAction('Type', self.cylDialog)
    cyl_menu.addAction('Update', self.cylDialog)
    cyl_menu.addAction('Val', self.cylDialog)
    grid_menu.addMenu(cyl_menu)
    grid_menu.addAction('Solve', self.solveDialog)
    menubar.addMenu(grid_menu)
    ana_menu = QtGui.QMenu('Analysis', self)
    pro_menu = QtGui.QMenu('Profile', self)
    pro_menu.addAction('X', self.profileDialog)
    pro_menu.addAction('Y', self.profileDialog)
    pro_menu.addAction('Z', self.profileDialog)
    ana_menu.addMenu(pro_menu)
    menubar.addMenu(ana_menu)

  def fileNew(self):
    self.glwidget.grid = NewGridDialog.newGrid(self)
    if self.glwidget.grid:
      self.glwidget.model.init()
      self.glwidget.gridFit()
      self.glwidget.cmp.range = (0.0, 0.0)
      self.glwidget.updateGL()

  def fileOpen(self):
    fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
    if fname:
      self.glwidget.grid = MPGrid.read(str(fname))
      self.glwidget.model.init()
      self.glwidget.gridFit()
      self.glwidget.cmpRange()
      self.glwidget.updateGL()

  def fileSave(self):
    if self.glwidget.grid:
      fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file')
      if fname:
        self.glwidget.grid.write(str(fname), self.compress)
        
  def fileSaveImage(self):
    if self.glwidget.grid:
      fname = QtGui.QFileDialog.getSaveFileName(self, 'Save image')
      if fname:      
        img = self.glwidget.screenShot()
        img.save(str(fname))

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
    
  def solveDialog(self):
    if self.glwidget.grid:
      dlg = SolveDialog(self, self.glwidget)
      ok = dlg.exec_()
      if ok:
        self.glwidget.cmpRange()
        self.glwidget.updateGL()

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
    toolbar = QtGui.QToolBar(self)
    toolbar.addAction('Init', self.initModel)
    toolbar.addAction('Fit', self.gridFit)    
    toolbar.addSeparator()    
    group1 = QtGui.QButtonGroup(self)
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
    group2 = QtGui.QButtonGroup(self)
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
    self.addToolBar(toolbar)

  def setMouseMode(self, pressed):
    txt = self.sender().text()
    if txt == "Rot":
        self.glwidget.mouseMode = 0
    elif txt == "Trans":
        self.glwidget.mouseMode = 1 
    elif txt == "Zoom":
        self.glwidget.mouseMode = 2

  def setDrawKind(self, pressed):
    txt = self.sender().text()
    if txt == "Type":
        self.glwidget.draw.kind = 0
    elif txt == "Update":
        self.glwidget.draw.kind = 1 
    elif txt == "Val":
        self.glwidget.draw.kind = 2
    self.glwidget.updateGL()

  def initModel(self):
    self.glwidget.model.init()
    self.glwidget.updateGL()

  def gridFit(self):
    self.glwidget.gridFit()
    self.glwidget.updateGL()

class ToolButton(QtGui.QToolButton):
  def __init__(self, text, func):
    super(ToolButton, self).__init__()
    self.setText(text)
    self.clicked[bool].connect(func)
    self.setCheckable(True)

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())


