#!/usr/bin/python

from rtai_lxrt import *
from rtai_mbx import *
from rtai_msg import *
from rtai_sem import *
import scipy as sc
#from terminalplot import plot
import pyqtgraph as pg


class DATA(Structure) :
	_fields_ = [("t", c_double), 
	            ("signal1", c_double),
	            ("signal2", c_double)]
	            #("signal3", c_double)]

datos = DATA(0, 0)


rt_allow_nonroot_hrt()

task = rt_task_init_schmod(nam2num("REVTASK"), 20, 0, 0, 0, 0xF)

mbx = rt_get_adr(nam2num("RTS0"))
rt_make_soft_real_time()

tmp=sc.zeros((1,3))
ii=1
pg.setConfigOption('background', 'w')
pw = pg.plot()

N=10000
while True :
	rt_mbx_receive(mbx, byref(datos), sizeof(datos))
	tmp=sc.r_[tmp,[[datos.t, datos.signal1,datos.signal2]]]	
	if ii%10==0:
		#print ii, tmp[ii-100:ii,0]
		pw.plot(tmp[ii-N:ii:10,0].tolist(),tmp[ii-N:ii:10,1].tolist(), pen=(0,3),clear=True)#,tmp[ii-100:ii,2],tmp[ii-100:ii,3])
		pw.plot(tmp[ii-N:ii:10,0].tolist(),tmp[ii-N:ii:10,2].tolist(), pen=(1,3))
		#pw.plot(tmp[ii-N:ii:10,0].tolist(),tmp[ii-N:ii:10,3].tolist(), pen=(2,3))
		pg.QtGui.QApplication.processEvents()
	#print "* time:", datos.t, "signal1:",datos.signal1,"signal2:",datos.signal2,"signal3:",datos.signal3," *\n"
	ii=ii+1
rt_task_delete(task)
print "* EXITING DISPLAY *"

