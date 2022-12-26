import sys
from PySide2.QtWidgets import QApplication, QWidget
# 导入我们生成的界面
from ui_main import Ui_Form
 
# 继承QWidget类，以获取其属性和方法
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 设置界面为我们生成的界面
        self.ui = Ui_Form()
        self.ui.setupUi(self)
 
# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWidget()
    window.show()
 
    sys.exit(app.exec_())