from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL
from PySide2.QtGui import QKeyEvent

from polygon import *

class MyGLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.load_polygon()
        self.polygon_color = [51,161,201]
        self.per = [p / 255 for p in self.polygon_color]
        self.l, self.r, self.b, self.t = -50, 50, -50, 50 # 绘制的左右上下边界
        self.mouse_x, self.mouse_y = 0, 0 # 记录拖拽时上一次鼠标位置
        self.xf, self.yf = 0, 0  # 绘制时xy偏移量
        self.isFirst = True             # 用于第一次加载标志

        # 这个三个是虚函数, 需要重写
        # paintGL
        # initializeGL
        # resizeGL

    # 启动时会先调用 initializeGL, 再调用 resizeGL , 最后调用两次 paintGL
    # 出现窗口覆盖等情况时, 会自动调用 paintGL
    # 调用过程参考 https://segmentfault.com/a/1190000002403921
    # 绘图之前的设置
    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION) # 正投影


    def draw_aes(self):
        '''绘制坐标系'''
        glColor3f(61/255, 89/255, 171/255)
        glLineWidth(0.1)
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0x0101)
        glBegin(GL_LINES)
        
        # 两个点一条线
        glVertex3f(-2147483648, 0, 0.0)
        glVertex3f(2147483647, 0, 0.0)
        glVertex3f(0,-2147483648, 0.0)
        glVertex3f(0, 2147483647, 0.0)
    
        glEnd();

    def draw_polygon(self):
        '''绘制多边形'''
        glDisable(GL_LINE_STIPPLE)
        glFrontFace(GL_CW);   # 设置CW方向为“正面”，CW即ClockWise，顺时针
        # 设置正面逆时针为线条模式  GL_LINE / GL_FILL
        glPolygonMode(GL_FRONT, GL_LINE); 
        # 设置反面顺时针为填充模式
        glPolygonMode(GL_BACK, GL_LINE); 
        glLineWidth(1)

        for polygon in self.polygon_set:
            glColor3f(self.per[0], self.per[1], self.per[2])
            glBegin(GL_POLYGON)
            for pt in polygon.hull():
                glVertex2f(pt.x(), pt.y())
            glEnd()
            
            for hole in polygon.holes():
                glColor3f(0, 0, 0)  # 设定颜色RGB
                glBegin(GL_POLYGON)
                for pt in hole:
                    glVertex2f(pt.x(), pt.y())
                glEnd()
        
        if self.isFirst:
            print('draw')
            self.isFirst = False
            # self.recover_position()

	# 绘图函数
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        # glTranslatef(self.xf, self.yf, 0.0) # 偏移
        self.draw_aes()
        self.draw_polygon()
        glFlush()  # 执行绘图

    def resizeGL(self, w, h):
        glLoadIdentity()
        gluOrtho2D(self.l, self.r, self.b, self.t) # 定义xy轴范围

    def keyPressEvent(self, event: QKeyEvent):
        print(event)

    def keyspec(self, button, x, y):
        '''特殊按键'''
        # print(button, x, y)
        if button == GLUT_KEY_LEFT:
            self.l -= 10
            self.r -= 10
        elif button == GLUT_KEY_RIGHT:
            self.l += 10
            self.r += 10
        elif button == GLUT_KEY_UP:
            self.b += 10
            self.t += 10
        elif button == GLUT_KEY_DOWN:
            self.b -= 10
            self.t -= 10
        glLoadIdentity()
        gluOrtho2D(self.l, self.r, self.b, self.t)
        glutPostRedisplay()

    def recover_position(self):
        self.l, self.b, self.r, self.t = self.polygon_set.bbox()
        self.l -= 10
        self.b -= 10
        self.r += 10
        self.t += 10
        glLoadIdentity()
        # print(self.l, self.b, self.r, self.t)
        gluOrtho2D(self.l, self.r, self.b, self.t)
        glutPostRedisplay()

    def load_polygon(self):
        self.polygon_set = PolygonSet()
        self.polygon_set.load_file('polygon.txt')