#!/usr/bin/env python

# The Python version of Qwt-5.0.0/examples/data_plot

# for debugging, requires: python configure.py  --trace ...
if False:
    import sip
    sip.settracemask(0x3f)

import random
import sys
from rtai_lxrt import *
from rtai_mbx import *
from rtai_msg import *
from rtai_sem import *


from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *

class DATA0(Structure) :
        _fields_ = [("signal", c_double)]

class DATA1(Structure) :
        _fields_ = [("t", c_double),
                    ("signal", c_double)]
class DATA3(Structure) :
        _fields_ = [("t", c_double),
                    ("signal1", c_double),
                    ("signal2", c_double),
                    ("signal3", c_double)]

datos = DATA3(0,0,0, 0)


datos1 = DATA1(0)


rt_allow_nonroot_hrt()

task = rt_task_init_schmod(nam2num("REVTASK"), 20, 0, 0, 0, 0xF)

mbx1 = rt_get_adr(nam2num("MBX1"))
mbx = rt_get_adr(nam2num("RTS0"))
print(mbx)
print(mbx1)
rt_make_soft_real_time()




class DataPlot(Qwt.QwtPlot):
    i=0
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.Qt.white)
        self.alignScales()

        # Initialize data
        self.x = arange(0.0, 100.1, 0.5)
        self.y1 = zeros(len(self.x), float)
        self.y2 = zeros(len(self.x), float)
        self.y3 = zeros(len(self.x), float)

        self.setTitle("RTAI Maibox conection")
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        self.curve1 = Qwt.QwtPlotCurve("Data 1")
        self.curve1.attach(self)
        self.curve1.setPen(Qt.QPen(Qt.Qt.red))

        self.curve2 = Qwt.QwtPlotCurve("Data 2")
        self.curve2.attach(self)
        self.curve2.setPen(Qt.QPen(Qt.Qt.blue))

        self.curve3 = Qwt.QwtPlotCurve("Data 3")
        self.curve3.attach(self)
        self.curve3.setPen(Qt.QPen(Qt.Qt.green))



        mY = Qwt.QwtPlotMarker()
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.attach(self)

        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")
    
        self.startTimer(50)
        self.phase = 0.0

    # __init__()

    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(
                    Qwt.QwtAbstractScaleDraw.Backbone, False)

    # alignScales()
    
    def timerEvent(self, e):
        if self.phase > pi - 0.0001:
            self.phase = 0.0

        # y moves from left to right:
        # shift y array right and assign new value y[0]
        self.x = concatenate((self.x[:1], self.x[:-1]), 0)
        self.y1 = concatenate((self.y1[:1], self.y1[:-1]), 0)
        self.y2 = concatenate((self.y2[:1], self.y2[:-1]), 0)
        self.y3 = concatenate((self.y3[:1], self.y3[:-1]), 0)
        self.y1[0] =  datos.signal1
        self.y2[0] =  datos.signal2*3
        self.y3[0] =  datos.signal3

        self.x[0] =  datos.t*0.1
        #self.x[0] =  self.i
	rt_mbx_receive(mbx1, byref(datos1), sizeof(datos1))
	rt_mbx_receive(mbx, byref(datos), sizeof(datos))
        self.i=self.i+1
	self.curve1.setData(self.x, self.y1)
	self.curve2.setData(self.x, self.y2)
	self.curve3.setData(self.x, self.y3)
	#print(datos.signal3)

        self.replot()
        self.phase += pi*0.02

    # timerEvent()

# class DataPlot

def make():
    demo = DataPlot()
    demo.resize(500, 300)
    demo.show()
    return demo

# make()

def main(args): 
    app = Qt.QApplication(args)
    demo = make()
    sys.exit(app.exec_())

# main()

# Admire
if __name__ == '__main__':
    main(sys.argv)
    rt_task_delete(task)
    print "* EXITING DISPLAY *"

# Local Variables: ***
# mode: python ***
# End: ***


