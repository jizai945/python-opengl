import sys
import PySide2
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import Qt
from ui_main import Ui_Form
import os

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
 
# 继承QWidget类，以获取其属性和方法
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('polygon show')
        self.ui.btn_file.clicked.connect(self.on_file_btn_clicked)
        
    def on_file_btn_clicked(self):
        '''文件对话框'''
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Text Files (*.txt)', options=options)
        if file_name:
            # 如果选择了文件，打印文件名
            print(file_name)
            self.ui.le_file.setText(file_name)
            self.ui.openGLWidget.load_polygon(file_name)
            self.ui.openGLWidget.update()
 
# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWidget()
    window.setFixedSize(900,900)
    window.show()
 
    sys.exit(app.exec_())