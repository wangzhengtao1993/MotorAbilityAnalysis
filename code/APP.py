from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from EMGUi import HomePage, NewFile
# from EMGProcess import readData as rd



app = QApplication([])
homepage = HomePage()
homepage.ui.show()
app.exec_()





