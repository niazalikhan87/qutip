#This file is part of QuTIP.
#
#    QuTIP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    QuTIP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with QuTIP.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011, Paul D. Nation & Robert J. Johansson
#
###########################################################################
import sys,time
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
    except:
        raise RuntimeError('PyQt4 or PySide GUI module is not installed.')


class ProgressBar(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.thread = Worker()
        self.percent = 0
        self.pbar = QProgressBar(self)
        self.pbar.setStyleSheet("QProgressBar {width: 25px;border: 3px solid black; border-radius: 5px; background: white;text-align: center;padding: 0px;}" 
                               +"QProgressBar::chunk:horizontal {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6699FF, stop: 0.5 #66AAFF, stop: 0.6 #66CCFF, stop:1 #FFFFFF);}")
        self.pbar.setGeometry(25, 40, 300,40)
        self.label = QLabel(self)
        self.label.setStyleSheet("QLabel {font-size: 12px;}")
        self.label.setText("Trajectories completed:                                       a")
        self.label.move(25, 20)
        self.setWindowTitle('Monte-Carlo Trajectories')
        self.setGeometry(300, 300, 350, 120)
        #self.setWindowOpacity(0.9) #make transparent
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        self.setFixedSize(self.size());
        self.connect(self.thread, SIGNAL("completed"), self.updateUi)  
        self.connect(self.thread, SIGNAL("done"), self.end)
        self.thread.start()
    def updateUi(self):
        self.percent+=1
        self.pbar.setValue(self.percent)
        self.label.setText('Trajectories completed: '+str(self.percent)+ '/100')
    def end(self):
        time.sleep(0.5)
        return self.close()
            
class Worker(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
    def run(self):
       # Note: This is never called directly. It is called by Qt once the
       # thread environment has been set up.
       for n in range(1,101):
           self.emit(SIGNAL("completed"))
           time.sleep(.05)
       return self.emit(SIGNAL("done"))
       
           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pbar = ProgressBar()
    pbar.show()
    pbar.raise_()
    app.exec_()
