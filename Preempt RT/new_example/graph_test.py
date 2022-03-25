#!/usr/bin/env python

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import threading
import zmq

context = zmq.Context( )
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")
topicfilter=b'graph'
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
topicfilter=b'data'
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsLayoutWidget(show=True, title="Beam evolution plot")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


p1 = win.addPlot(title="Beam evolution plot")
ptr = 2


global string, old_string

def get_string(socket):
    while True:
        global string
        string1 = socket.recv()
        if string1[0:3]==b'gra':
            string = string1

string=""
old_string = string
ii = 0
x = threading.Thread(target=get_string, args=(socket,))
x.start()
def update():
    global ptr, p1, string, old_string, ii
    p1.enableAutoRange('xy', True)
    if ptr == 0:
          pass## stop auto-scaling after the first data set is plotted
    ptr += 1
    if string[0:3]==b'gra':
            if string != old_string:
                old_string = string
                ii=ii+1
                data=eval(string[6:])
                if ii == 21:
                    print('21')
                    p1.clear()
                    ii=0
                p1.plot(data[0], data[1], pen=(1,3))
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
