#!/usr/bin/env python

# The Python version of Qwt-5.0.0/examples/data_plot

# for debugging, requires: python configure.py  --trace ...
if False:
    import sip
    sip.settracemask(0x3f)

import random
import sys
import socket
import os
import time
import struct

from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *


server_address = '/tmp/bsock'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)


while True:
	try:
		connection, client_address = sock.accept()
		break
		print "bat"
	except:
		pass
		time.sleep(0.5)
		
		print "bi"

class DataPlot(Qwt.QwtPlot):

    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.Qt.white)
        self.alignScales()

        # Initialize data
        self.x = arange(0.0, 100.1, 0.1)
        self.y = zeros(len(self.x), Float)

        self.setTitle("A Moving QwtPlot Demonstration")
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        self.curveR = Qwt.QwtPlotCurve("Data Moving Right")
        self.curveR.attach(self)


        self.curveR.setPen(Qt.QPen(Qt.Qt.red))

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
        self.y = concatenate((self.y[:1], self.y[:-1]), 1)
        self.x = concatenate((self.x[:1], self.x[:-1]), 1)
	data = connection.recv(16)
	data=struct.unpack('dd',data)
        self.y[0] = data[1]
        self.x[0] = data[0]
		

        self.curveR.setData(self.x, self.y)

        self.replot()

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

# Local Variables: ***
# mode: python ***
# End: ***


