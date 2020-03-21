from rtai_lxrt import *
from rtai_mbx import *
from rtai_msg import *



MAX_NAME_SIZE=256
class RTPARAM(Structure) :
        _fields_ = [	("modelName",c_char*MAX_NAME_SIZE),
			("blockName",c_char*MAX_NAME_SIZE),
			("paramName",c_char*MAX_NAME_SIZE),
			("nRows",c_uint),
			("nCols",c_uint),
			("dataType",c_uint),
			("dataClass",c_uint),
			("dataValue",c_double*MAX_NAME_SIZE)]

class datuak(Structure) :
        _fields_ = [	("index",c_int),
			("mat_ind",c_int),
			("value",c_double)]

datuak_p=(datuak*2)()

xd=c_int(2)
xd1=c_int(0)
#rt_rpcx(task1,byref(xd),byref(xd1),sizeof(xd),sizeof(xd1))

datuak_p[0].index=0
datuak_p[0].mat_ind=0
datuak_p[0].value=5.3
datuak_p[1].value=1.7
datuak_p[1].mat_ind=1
datuak_p[1].index=0

#rt_rpcx(task1,datuak_p,byref(xd1),sizeof(datuak_p),sizeof(xd1))

#mName=(c_char*MAX_NAME_SIZE)()
#mName=cast(mName,POINTER(c_char))
mName=b''
#bName=(c_char*MAX_NAME_SIZE)()
#bName=cast(bName,POINTER(c_char))
bName=b''
#pName=(c_char*MAX_NAME_SIZE)()
#pName=cast(pName,POINTER(c_char))
pName=b''
dValue=(c_double*MAX_NAME_SIZE)()
#dValue=cast(dValue,POINTER(c_double))
rtParam=RTPARAM(mName,bName,pName,c_uint(0),c_uint(0),c_uint(0),c_uint(0),dValue)
#data = DATA(0, 0)
#data=c_double(0)

rt_allow_nonroot_hrt()
task = rt_task_init_schmod(nam2num("LAT1"), 20, 0, 0, 0, 0xF)
task1 = rt_get_adr(nam2num("KTASK"))


rt_make_soft_real_time()

#p=c_uint(112)
c=c_ulong(99)
g=c_ulong(103)
po=c_uint()

val=c_double(4)
xi=c_uint(0)
#rt_rpc(task1,c,byref(po))
#rt_rpcx(task1,byref(xi),byref(rtParam),sizeof(xi),sizeof(rtParam))
#rt_sendx(task1,byref(xl),sizeof(xl))



# Azkena

# Function list parameters
list={'None':{'None':0}}
def list_parameters():
	g=c_ulong(103)
	po=c_uint(0)
	#poi=c_int(0)
	rt_rpc(task1,g,byref(po))
	#rt_rpcx(task1,byref(xi),byref(poi),sizeof(xi),sizeof(poi))
	t1=rt_rpcx(task1,byref(xi),byref(po),sizeof(xi),sizeof(po))
	#tmp={rtParam.paramName[:]: rtParam.dataValue[0:]}
	Param_names=[]
	list=[]
	for ii in range(0,po.value):	#&0x0FFFF-1):
            t1=rt_rpcx(task1,byref(xi),byref(rtParam),sizeof(xi),sizeof(rtParam))
			
            tmp={rtParam.paramName: rtParam.dataValue[0:1]}
            list.append({rtParam.blockName:tmp})#[rtParam.paramName]= rtParam.dataValue[0:1]
            print(rtParam.blockName+"  "+rtParam.paramName+"  "+str(rtParam.dataValue[0:1]))
	
	return list

# Change of parameter 

def change_p(datuak):
	# [index,value]
	p=c_ulong(112)
	xi=c_int(datuak[0]) #index)
	poi=c_int(0)
	rt_rpc(task1,p,byref(poi))
	rt_rpcx(task1,byref(xi),byref(poi),sizeof(xi),sizeof(poi))
	pvalue=c_double(datuak[1]) #value)
	rt_rpcx(task1,byref(pvalue),byref(poi),sizeof(pvalue),sizeof(poi))
	rt_rpcx(task1,byref(xi),byref(poi),sizeof(xi),sizeof(poi))

def find_param(params, name):
     p_name=[ii for ii in params if (ii.keys()[0].find('Gain_in')+1)!=0]
     ind=[ii for ii in range(0,len(params)) if (params[ii].keys()[0].find('Gain_in')+1)!=0]
     return p_name,ind


#Strategy for various parameters
#rt_rpcx(task1,datuak_p,byref(xd1),sizeof(datuak_p),sizeof(xd1))

