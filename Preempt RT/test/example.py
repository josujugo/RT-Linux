import os
import ctypes

PORT = 0x378
NSEC_PER_SEC = 1000000000

librt=ctypes.CDLL('librt.so', mode=ctypes.RTLD_GLOBAL)
# using clock_nanosleep of librt */

class timeval(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]
    
""" 
extern int clock_nanosleep(clockid_t __clock_id, int __flags,
      __const struct timespec *__req,
      struct timespec *__rem);

   the struct timespec consists of nanoseconds
 * and seconds. if the nanoseconds are getting
 * bigger than 1000000000 (= 1 second) the
 * variable containing seconds has to be
 * incremented and the nanoseconds decremented
 * by 1000000000.
"""
 
def tsnorm(ts):
   while (ts.tv_nsec >= NSEC_PER_SEC):
      ts.tv_nsec = ts.tv_nsec-NSEC_PER_SEC;
      ts.tv_sec = ts.tv_sec++1;

prio=20
interval=500000000;

print("using realtime, priority: %d\n",prio);
param = os.sched_param(os.sched_get_priority_max(os.SCHED_FIFO))
#param.sched_priority = prio;

t=timeval()

# enable realtime fifo scheduling
tmp = os.sched_setscheduler(0, os.SCHED_FIFO, param)
if tmp == -1:
         print("sched_setscheduler failed");
         os._exit(-1);

# get current time */
CLOCK_REALTIME = 0
librt.clock_gettime(CLOCK_REALTIME,ctypes.byref(t))

# start after one second */
t.tv_sec = t.tv_sec + 1
ii=0
TIMER_ABSTIME = 1

while (1):
      # wait untill next shot */
      librt.clock_nanosleep(CLOCK_REALTIME, TIMER_ABSTIME, ctypes.byref(t), None);
      # do the stuff */
      ii=ii+1
      print(t.tv_sec, ii, '')
      # calculate next shot */
      t.tv_nsec = t.tv_nsec+interval;
      tsnorm(t);
