from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from polygon import *


class Show(object):
    def __init__(self) -> None:
        self.polygon_color = [51,161,201]
        self.per = [p / 255 for p in self.polygon_color]
        self.l, self.r, self.b, self.t = -50, 50, -50, 50 # 绘制的左右上下边界
        self.mouse_x, self.mouse_y = 0, 0 # 记录拖拽时上一次鼠标位置
        self.xf, self.yf = 0, 0  # 绘制时xy偏移量
        self.isFirst = True             # 用于第一次加载标志
    
    def gl_init(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION) # 正投影
        # glLoadIdentity()
        # gluOrtho2D(self.l, self.r, self.b, self.t) # 定义xy轴范围
        
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
            self.recover_position()
            
    
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
    
    def draw(self):
        '''绘制'''
        glClear(GL_COLOR_BUFFER_BIT)
        # glTranslatef(self.xf, self.yf, 0.0) # 偏移
        self.draw_aes()
        self.draw_polygon()
        glFlush()  # 执行绘图
    
    def key(self, key: str, x: int, y: int) -> None:
        '''普通按键'''
        print(key, x, y)
        if key == b' ':
            print('1')
            self.recover_position()
    
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
        
    def mouse(self, button, state, x, y):
        '''
        针对滚轮上下滑动缩放处理
        同时记录鼠标点击的位置, 便于拖拽计算
        '''
        if state == 1:
            return
        
        view = glGetIntegerv(GL_VIEWPORT)
        # print(view)
        self.mouse_x, self.mouse_y = x,  view[3] - y
        # print(f'mouse click: {self.mouse_x}, {self.mouse_y}')
        
        # todo 这里放大缩小的系数应该是要能调整的
        if button == 4: # 滚轮下滑 缩小
            self.l -= 10
            self.r += 10
            self.b -= 10
            self.t += 10
        elif button == 3: # 滚轮上滑 放大
            if self.r - self.l > 30:
                self.l += 10
                self.r -= 10
            if self.t - self.b > 30:
                self.b += 10
                self.t -= 10
        else:
            return
        
        glLoadIdentity()
        gluOrtho2D(self.l, self.r, self.b, self.t)
        glutPostRedisplay()
        
    def mousemotion(self, x, y):
        '''针对鼠标拖拽处理'''
        view = glGetIntegerv(GL_VIEWPORT)
        # print(view)
        to_x, to_y = x,  view[3] - y
        coord_width = self.r - self.l
        coord_height= self.t - self.b
        # print(f'mouse move: {x}, {view[3] - y}')
        
        x_move = (to_x - self.mouse_x) / view[2] * coord_width
        y_move = (to_y - self.mouse_y) / view[3] * coord_height
        self.l -= x_move
        self.r -= x_move
        self.b -= y_move
        self.t -= y_move
        # print(f'l_x: {self.l_x} l_y: {self.l_y}')
        glLoadIdentity()
        gluOrtho2D(self.l, self.r, self.b, self.t)
        glutPostRedisplay()
        
        self.mouse_x, self.mouse_y = to_x,  to_y
        
    def load_polygon(self):
        self.polygon_set = PolygonSet()
        self.polygon_set.load_file('polygon.txt')
        
if __name__ == '__main__':
    glutInit()                           # 1. 初始化glut库
    displayMode = GLUT_RGB | GLUT_SINGLE
    glutInitDisplayMode(displayMode)
    
    glutInitWindowSize(600, 500)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('Polygons')
    
    show = Show()
    show.load_polygon()
    show.gl_init()                           # 初始化画布
    glutDisplayFunc(show.draw)               # 注册回调函数draw()
    glutMouseFunc(show.mouse)                # 鼠标
    glutMotionFunc(show.mousemotion)         # 注册响应鼠标拖拽的函数mousemotion()
    glutKeyboardFunc(show.key)               # 按键
    glutSpecialFunc(show.keyspec)            # 特殊按键 (上下左右)
    
    
    glutMainLoop()                           # 进入glut主循环  