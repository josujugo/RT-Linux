#!/usr/bin/python

import sys
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore

from rtai_lxrt import *
from rtai_mbx import *
from rtai_msg import *
from rtai_sem import *
import scipy as sc

class DATA(Structure) :
	_fields_ = [("t", c_double), 
	            ("signal1", c_double),
	            ("signal2", c_double),
	            ("signal3", c_double)]

datos = DATA(0, 0)

rt_allow_nonroot_hrt()

task = rt_task_init_schmod(nam2num("REVTASK"), 20, 0, 0, 0, 0xF)

mbx = rt_get_adr(nam2num("RTS0"))
rt_make_soft_real_time()

tmp=sc.zeros((1,4))

# globals
PLOT_LEN = 2048
DOUBLE_SIZE = 8
PACKET_LEN = NIN * PACKET_NUM * DOUBLE_SIZE
PLOT_LINE_COLORS = ['y', 'g', 'r', 'b', 'c', 'm', 'k', 'w']
PLOT_WINDOM_SIZE = (1000, 600)
TIMER_PERIOD = 20


# some plot related stuff
app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Scope")
win.resize(PLOT_WINDOM_SIZE[0], PLOT_WINDOM_SIZE[1])
pg.setConfigOptions(antialias=True, useWeave=True)
plots = []
curves = []
p = win.addPlot(title="u"+str(i))
plots.append(p)
# add plots for all inputs to blk
for i in range(NIN):
    p.showGrid(x=True, y=True)
    c = PLOT_LINE_COLORS[i % len(PLOT_LINE_COLORS)]
    curves.append(p.plot(pen=c))
    win.nextRow()

tdata = np.zeros(shape=(NIN, PLOT_LEN))
# time bounds, s.t. we start at 0 Delta
t = 1 - PLOT_LEN

def update():
    """Will receive data from model and plot it."""
    import struct
    global t, curves, tdata, PACKET_NUM, NIN, timer
	rt_mbx_receive(mbx, byref(datos), sizeof(datos))
	data=sc.r_[tmp,[[datos.t, datos.signal1,datos.signal2, datos.signal3]]]	
    #data = sock.recv(PACKET_LEN, socket.MSG_WAITALL)
    if not data:
        # other end closed connection
        timer.stop()        
        return
        
    t += PACKET_NUM
	if ii%1000==0:
		#print ii, tmp[ii-100:ii,0]
		plot(tmp[ii-1000:ii:3,0].tolist(),tmp[ii-1000:ii:3,2].tolist())#,tmp[ii-100:ii,2],tmp[ii-100:ii,3])
    for j in range(3):
        tdata[j][:] = data[:,0]
        curves[j].setData(tdata[j])
        curves[j].setPos(t, 0)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(TIMER_PERIOD)

if __name__ == "__main__":
    import sys
    if (1 != sys.flags.interactive) or not hasattr(QtCore, "PYQT_VERSION"):
        QtGui.QApplication.instance().exec_()
