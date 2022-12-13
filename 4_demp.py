#coding=utf-8
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
def init():
    glClearColor(1.0, 1.0, 6.0, 1.0) # 背景颜色
    glMatrixMode(GL_PROJECTION) # 投影
    gluOrtho2D(0.0, 600.0, 0.0, 600.0) # 参数分别代表（左下角x坐标，右上角x坐标，左下角y坐标，右上角y坐标）
#图形围绕定点（width,highth)做变换
width=70
highth=70
#画所要处理的图像
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 0.0, 1.0) #三角形颜色
    GLfloat
    PointA = (50+width, 50+highth)
    PointB = (100+width, 100+highth)
    PointC = (150+width, 50+highth)
    glLineWidth(5.0)
    glBegin(GL_LINE_LOOP) # 闭合折线 开始绘制线段
    glVertex2fv(PointA)
    glVertex2fv(PointB)
    glVertex2fv(PointC)
    glEnd() #结束绘制线段
    glFlush() #清空缓冲区
 
#用键盘将图像平移
def mykeyboard(key, x, y):
    global width, highth
    if (key == GLUT_KEY_RIGHT):
        width += 1.0
    if (key == GLUT_KEY_LEFT):
        width -= 1.0
    if (key == GLUT_KEY_UP):
        highth += 1.0
    if (key == GLUT_KEY_DOWN):
        highth -= 1.0
    glutPostRedisplay()
 
#用鼠标图形缩放
def mymouse(button,state,x,y):
    if (state == GLUT_DOWN):
        if (button == GLUT_LEFT_BUTTON):
            glScalef(0.5, 0.5, 0.0)
            display()
        elif(button == GLUT_RIGHT_BUTTON):
            glScalef(1.5, 1.5, 0.0)
            display()
        glutPostRedisplay() #重新调用绘制函数
    return
if __name__=="__main__":
    glutInit() #窗口初始化
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(600,600)
    glutCreateWindow("slide and scale")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(mykeyboard)#特殊按键
    glutMouseFunc(mymouse)
    glutMainLoop() #运行主函数