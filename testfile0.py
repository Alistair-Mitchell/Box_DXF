import sys, math
from PyQt5 import QtCore, QtGui, QtWidgets

n = 8
r = 150
s = 0
global poly
poly = 0

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))        # set fillColor
        self.polygon = self.createPoly()                         # polygon with n points, radius, angle of the first point

    def createPoly(self):
        if poly = 0
            polygon = QtGui.QPolygonF()
            poly = 1
        w = 360/n                                                       # angle per step
        for i in range(n):                                              # add the points of polygon
            t = w*i + s
            x = r*math.cos(math.radians(t))
            y = r*math.sin(math.radians(t))
            polygon.append(QtCore.QPointF(self.width()/2 +x, self.height()/2 + y))

        return polygon

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)

app = QtWidgets.QApplication(sys.argv)

widget = MyWidget()
widget.show()

sys.exit(app.exec_())
