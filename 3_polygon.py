from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Show(object):
    def __init__(self) -> None:
        self.polygon_color = [51,161,201]
        self.per = [p / 255 for p in self.polygon_color]
        self.l, self.r, self.b, self.t = -50, 50, -50, 50
        self.mouse_x, self.mouse_y = 0, 0 # 记录拖拽时上一次鼠标位置
        self.real_x, self.real_y = 0, 0 # 记录实时位置

    def gl_init(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION) # 正投影
        glLoadIdentity()
        gluOrtho2D(self.l, self.r, self.b, self.t) # 定义xy轴范围

    def draw_aes(self):
        glColor3f(61/255, 89/255, 171/255)
        glLineWidth(1)
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0x0101)
        glBegin(GL_LINES)
        
        # 两个点一条线
        glVertex3f(-2147483648, 0, 0.0)
        glVertex3f(2147483647, 0, 0.0)
        glVertex3f(0,-2147483648, 0.0)
        glVertex3f(0, 2147483647, 0.0)
    
        glEnd();

    def draw_polygon_demo(self):
        glDisable(GL_LINE_STIPPLE)
        glFrontFace(GL_CW);   # 设置CW方向为“正面”，CW即ClockWise，顺时针
        # 设置正面逆时针为线条模式  GL_LINE / GL_FILL
        glPolygonMode(GL_FRONT, GL_LINE); 
        # 设置反面顺时针为填充模式
        glPolygonMode(GL_BACK, GL_LINE); 
        glLineWidth(1)

        # 顺时针
        glColor3f(self.per[0], self.per[1], self.per[2])
        glBegin(GL_POLYGON)
        glVertex2f(0, 0)
        glVertex2f(0 , 10)
        glVertex2f(10, 10)
        glVertex2f(10, 0)
        glEnd()
        # 逆时针
        glColor3f(0, 0, 0)  # 设定颜色RGB
        glBegin(GL_POLYGON)
        glVertex2f(5, 5)
        glVertex2f(3, 5)
        glVertex2f(3, 3)
        glVertex2f(5, 3)
        glEnd()
        
        # 顺时针
        glColor3f(self.per[0], self.per[1], self.per[2])
        glBegin(GL_POLYGON)
        glVertex2f(20, 20)
        glVertex2f(25, 15)
        glVertex2f(15, 15)
        glEnd()
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw_aes()
        self.draw_polygon_demo()
        glFlush()  # 执行绘图
    
    def key(self, key: str, x: int, y: int) -> None:
        print(key, x, y)
        # if key == 'w':
        #     print('w')
    
    # def keyspec(self, button, x, y):
    #     print(button, x, y)
    #     # if (button == GLUT_LEFT_BUTTON):
    #     #     print('1')
    #     #     glScalef(0.5, 0.5, 0.0)
    #     #     self.l_x -= 10
    #     #     # draw()
    #     # elif(button == GLUT_RIGHT_BUTTON):
    #     #     print('2')
    #     #     glScalef(1.5, 1.5, 0.0)
    #     #     # draw()
    #     glutPostRedisplay() #重新调用绘制函数

    def mouse(self, button, state, x, y):
        # print(button, state, x, y)
        if state == 1:
            return

        view = glGetIntegerv(GL_VIEWPORT)
        # print(view)
        self.mouse_x, self.mouse_y = x,  view[3] - y
        print(f'mouse click: {self.mouse_x}, {self.mouse_y}')
        
        if button == 4:
            # 滚轮下滑 缩小
            # print('sub')
            # glScalef(0.5,0.5,0)
            
            self.l -= 10
            self.r += 10
            self.b -= 10
            self.t += 10
        elif button == 3:
             # 滚轮上滑 放大
            # print('add')
            # glScalef(1.5,1.5,0)
            if self.r - self.l > 30:
                self.l += 10
                self.r -= 10
            if self.t - self.b > 30:
                self.b += 10
                self.t -= 10
            
        self.gl_init()
        glutPostRedisplay() #重新调用绘制函数

    def mousemotion(self, x, y):
        # print(x, y)
        view = glGetIntegerv(GL_VIEWPORT)
        # print(view)
        to_x, to_y = x,  view[3] - y
        coord_width = self.r - self.l
        coord_height= self.t - self.b
        print(f'mouse move: {x}, {view[3] - y}')
        
        x_move = (to_x - self.mouse_x) / view[2] * coord_width
        y_move = (to_y - self.mouse_y) / view[3] * coord_height
        self.l -= x_move
        self.r -= x_move
        self.b -= y_move
        self.t -= y_move
        # print(f'l_x: {self.l_x} l_y: {self.l_y}')
        self.gl_init()
        
        self.mouse_x, self.mouse_y = to_x,  to_y

    def timer(self, value):
        print(f'{self.real_x} {self.real_y}')
        glutTimerFunc(1000, show.timer, 1)

    def test(self, x, y):
        view = glGetIntegerv(GL_VIEWPORT)
        self.real_x = self.l + x/view[2] * (self.r - self.l)
        self.real_y = self.b + (view[3] - y) /view[3] * (self.t - self.b)

if __name__ == '__main__':
    glutInit()                           # 1. 初始化glut库
    displayMode = GLUT_RGB | GLUT_SINGLE
    glutInitDisplayMode(displayMode)
    
    glutInitWindowSize(600, 500)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('Demo')
    
    show =  Show()
    show.gl_init()                           # 初始化画布
    glutDisplayFunc(show.draw)               # 注册回调函数draw()
    # glutKeyboardFunc(show.key)               # 按键
    # glutSpecialFunc(show.keyspec)            # 特殊按键 
    glutMouseFunc(show.mouse)                # 鼠标
    glutMotionFunc(show.mousemotion)         # 注册响应鼠标拖拽的函数mousemotion()
    glutTimerFunc(1000, show.timer, 1)
    
    glutPassiveMotionFunc(show.test)
    
    glutMainLoop()                           # 进入glut主循环    