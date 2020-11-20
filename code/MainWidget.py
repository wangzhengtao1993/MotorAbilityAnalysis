from PySide2.QtWidgets import QApplication, QMessageBox, QDialog, QWidget
from PySide2.QtUiTools import QUiLoader
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
# from EMGProcess import readData as rd
from pymysql import *
from new_user import NewUser
from new_test import NewTest


class HomePage(QWidget):

    def __init__(self):
        # 自定义绘图窗口
        QUiLoader().registerCustomWidget(pg.PlotWidget)
        self.conn = connect(host='localhost', port=3306, user='root',
                            password='123456', database='motor_ability_analysis',
                            charset='utf8')
        # 获得cursor对象
        self.cursor = self.conn.cursor()
        print("database motor_ability_analysis connected")
        # 加载主页ui
        self.ui = QUiLoader().load('ui_design/main.ui')
        # self.ui = QUiLoader().load('ui_design/main2.ui')
        # 初始化绘图窗口
        self.init_plot()
        self.ui.reset_plot_btn.clicked.connect(self.init_plot)
        # 显示默认窗口设置
        # self.ui.window_step.setText(str(self.win_setting[0]) + 'ms')
        # self.ui.window_width.setText(str(self.win_setting[1]) + 'ms')

        # 槽函数
        self.ui.new_user_btn.clicked.connect(self.new_user)
        self.ui.open_user_btn.clicked.connect(self.open_user)
        # self.ui.plot_btn.clicked.connect(self.multpolt)
        self.ui.new_test_btn.clicked.connect(self.new_test)
        # self.ui.window_setting_btn.clicked.connect(self.showWindowSetting)

    def init_plot(self):
        if True:
            muscle = ['', '三角肌前束', '三角肌中束', '肱二头肌', '肱三头肌',
                      '腕屈肌', '腕伸肌']
        else:
            muscle = ['', '股直肌', '股二头肌', '半腱肌 ', '股内侧肌',
                      '胫骨前肌', '外侧腓肠肌']

        for i in range(1, 7):
            EMG_plot = getattr(self.ui, 'EMG_plot_0' + str(i))  # 不是很懂，但是能用
            EMG_plot.setBackground('w')
            EMG_plot.setLabel("bottom", 't/s')
            EMG_plot.setLabel("left", 'u/' + chr(956) + 'V')
            y_max = int(self.ui.y_max.currentText())
            EMG_plot.setYRange(min=0, max=y_max, padding=0)
            EMG_plot.setXRange(min=0, max=100, padding=0)
            EMG_plot.setTitle(muscle[i])
            # EMG_plot.clear()

    def get_plot_info(self):
        user_id = self.ui.le_uesr_id.text()
        motion_name = self.ui.cb_motion_name.currentIndex()
        motion_mode = self.ui.cb_motion_mode.currentIndex()
        plot_info = [user_id, motion_name, motion_mode]
        return plot_info

    # 时间窗设置
    def setWin(self):
        s = int(self.ui.window_step_2.currentText())
        w = int(self.ui.window_width_2.currentText())
        win_set = [s, w]
        return win_set

    # 新建病历
    def new_user(self):
        new_user = NewUser()
        new_user.ui.show()
        new_user.ui.exec_()
        sql = "select max(user_id) from t_user"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print("result", result)
        user_id = result[0]
        print(user_id)
        self.show_user_info(user_id)

    def open_user(self):
        print("open")
        user_id = self.ui.le_uesr_id.text()
        self.show_user_info(user_id)

    def show_user_info(self, user_id):
        user_id = int(user_id)
        sql = "select * from t_user where user_id = %s" % user_id
        print("sql:", sql)
        self.cursor.execute(sql)
        user_info = self.cursor.fetchone()
        print(user_info)
        self.ui.l_user_id.setText(str(user_info[0]))
        self.ui.l_name.setText(str(user_info[1]))
        self.ui.l_gender.setText(str(user_info[2]))
        self.ui.l_year_of_birth.setText(str(user_info[3]))
        self.ui.l_handedness.setText(str(user_info[4]))
        self.ui.l_height.setText(str(user_info[5]))
        self.ui.l_weight.setText(str(user_info[6]))
        self.ui.l_waistline.setText(str(user_info[7]))
        self.ui.l_upperarm.setText(str(user_info[8]))
        self.ui.l_forearm.setText(str(user_info[9]))
        self.ui.l_thigh.setText(str(user_info[10]))
        self.ui.l_shank.setText(str(user_info[11]))
        print("user info is shown on Widget")

    def new_test(self):
        user_id = self.ui.l_user_id.text()
        name = self.ui.l_name.text()
        print("import new test data of ID:%s Name:%s" % (user_id, name))
        new_test = NewTest(user_id)
        new_test.ui.show()
        new_test.ui.exec_()

    # 绘图
    def multpolt(self):
        win_set = self.setWin()

        TESTINFO = [FREQUENCY, TESTTIME]
        self.ui.motion.setText(MOTION)
        self.ui.test_time.setText(TESTINFO[1])
        self.ui.frequency.setText(str(TESTINFO[0]) + 'Hz')
        EMG.rect(EMG.raw)
        if self.ui.plot_type.currentText() == '原始信号':
            print('原始信号')
            data = EMG.raw
            plot_type = 1
        elif self.ui.plot_type.currentText() == '整流信号':
            print('整流信号')
            data = EMG.re_raw
            plot_type = 2
        elif self.ui.plot_type.currentText() == '均方根':
            print('均方根')
            data = EMG.re_raw
            data = EMG.RMS(data, win_set)
            plot_type = 3
        else:
            print('平均值')
            data = EMG.re_raw
            data = EMG.AEMG(data, win_set)
            plot_type = 4

        for i in range(1, 9):
            t = data[:, 0]
            plotdata = data[:, i]
            EMG_plot = getattr(self.ui, 'EMG_plot_0' + str(i))
            EMG_plot.clear()
            EMG_plot.plot(t, plotdata, pen=pg.mkPen('b'))
            plotdata = data[:, i + 8]
            EMG_plot.plot(t, plotdata, pen=pg.mkPen('r'))


if __name__ == '__main__':
    app = QApplication([])
    homepage = HomePage()
    homepage.ui.show()
    app.exec_()
