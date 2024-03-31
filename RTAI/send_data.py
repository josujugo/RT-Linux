#!/usr/bin/python

from rtai_lxrt import *
from rtai_mbx  import *
from rtai_msg  import *

from scipy import sin
from array import *


#Estructura de datios para mandar en mailbox

class DATA(Structure) :
	_fields_ = [("time", c_double),
		    ("signal", c_double)]



#Crear mailbox

mbx = rt_mbx_init(nam2num("MBX1"), 20*sizeof(dato))

if mbx == NULL :
	libc.libc.printf("CANNOT CREATE MAILBOX\n")
	sys.exit(1)

# Crear tarea RTAI

task = rt_task_init_schmod(nam2num("DATCAL"), 0, 0, 0, 0, 0xF)

if task == 0 :
	libc.printf("CANNOT INIT MASTER LATENCY TASK\n")
	sys.exit(1)

libc.printf("\n## RTAI tst with python ##\n")


#  Poner en marcha reloj RT, si no lo esta

hard_timer_running = rt_is_hard_timer_running()

if hard_timer_running == 0 :
	if TIMER_MODE != 0 :
		rt_set_periodic_mode()
	elif TIMER_MODE == 0 :
		rt_set_oneshot_mode()
	period = start_rt_timer(nano2count(PERIOD))
else :
	period = nano2count(100000000)

# Hacer tiempo eral duro

rt_make_hard_real_time()

# Tiempo de espera para arrancar la tarea pèriodica

delay = rt_get_time() + 2*period

#Hacer tarea periodica

rt_task_make_periodic(task, delay, period)



while True :
	# Aqui se espera al evento periodico
	if rt_task_wait_period() == 0 :
		dato.time=(rt_get_time()-expected)*0.000000001
		dato.signal=sin(0.5*(dato.time))
		# se manda datos al mailbox
		rt_mbx_send_if(mbx, byref(dato), sizeof(dato))

# soft realtime
rt_make_soft_real_time()

# Parar reloj y destruir objetos RTAI
if hard_timer_running == 0 :
	stop_rt_timer()	


rt_task_delete(task)
rt_mbx_delete(mbx)
