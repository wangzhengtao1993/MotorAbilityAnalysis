from PySide2.QtWidgets import QApplication, QMessageBox, QDialog
from PySide2.QtUiTools import QUiLoader
from pyqtgraph.Qt import QtCore

import pyqtgraph as pg
from EMGProcess import readData as rd
from new_user import NewUser


# 主页
class HomePage():

    def __init__(self):
        # 自定义绘图窗口
        QUiLoader().registerCustomWidget(pg.PlotWidget)
        # 加载主页ui
        self.ui = QUiLoader().load('ui_design/main.ui')
        # 初始化绘图窗口
        self.init_plot()
        self.ui.reset_plot_btn.clicked.connect(self.init_plot)
        # 显示默认窗口设置

        # self.ui.window_step.setText(str(self.win_setting[0]) + 'ms')
        # self.ui.window_width.setText(str(self.win_setting[1]) + 'ms')
        # 槽函数
        self.ui.newfile_btn.clicked.connect(self.newfile)
        self.ui.plot_btn.clicked.connect(self.multpolt)
        # self.ui.window_setting_btn.clicked.connect(self.showWindowSetting)

    def init_plot(self):
        muscle = ['', '三角肌前束', '三角肌中束', '肱二头肌', '肱三头肌', \
                  '腕屈肌', '腕伸肌', '指浅屈肌', '指伸肌']
        for i in range(1, 9):
            EMG_plot = getattr(self.ui, 'EMG_plot_0' + str(i))  # 不是很懂，但是能用

            EMG_plot.setBackground('w')
            EMG_plot.setLabel("bottom", 't/s')
            EMG_plot.setLabel("left", 'u/' + chr(956) + 'V')
            y_max = int(self.ui.y_max.currentText())
            EMG_plot.setYRange(min=0, max=y_max, padding=0)
            EMG_plot.setXRange(min=0, max=100, padding=0)
            EMG_plot.setTitle(muscle[i])

            # EMG_plot.clear()

    # 时间窗设置
    def setWin(self):
        s = int(self.ui.window_step_2.currentText())
        w = int(self.ui.window_width_2.currentText())
        win_set = [s, w]
        return win_set

    # 新建病历
    def newfile(self):
        newfile = NewFile()
        newfile.ui.show()
        newfile.ui.exec_()
        file = newfile.getProfile()
        newid = newfile.getID()
        print(file)
        print(file[newid])

        # 显示病历信息
        self.ui.id.setText(str(newid))
        self.ui.name.setText(file[newid][0])
        self.ui.gender.setText(file[newid][1])
        self.ui.age.setText(file[newid][2])
        self.ui.hight.setText(file[newid][3])
        self.ui.weight.setText(file[newid][4])

    # 绘图
    def multpolt(self):
        EMG = rd()
        FREQUENCY = EMG.FREQUENCY
        TESTTIME = EMG.TESTTIME
        MOTION = EMG.MOTION
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
