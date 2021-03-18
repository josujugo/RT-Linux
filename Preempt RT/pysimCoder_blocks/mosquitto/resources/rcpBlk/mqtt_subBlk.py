from supsisim.RCPblk import RCPblk
from scipy import size, zeros

def mqtt_subBlk(pout,topic,defvals):
    """

    Call:   mqtt_subBlk(pout, topic, defvals)

    Parameters
    ----------
       pout: connected output port(s)
       topic : topic to subscribe
       defvals : Default outputs
       

    Returns
    -------
        blk  : RCPblk

    """
    
    outputs = len(pout)
    vals = zeros(outputs,float)
    if len(defvals) > outputs:
        N=outputs
    else:
        N = len(defvals)

    for n in range(N):
        vals[n]=defvals[n]
        
    
    blk = RCPblk('mqtt_sub',[], pout,[0,0],0,vals,[0,0],topic)
    return blk

