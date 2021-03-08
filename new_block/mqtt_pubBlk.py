from supsisim.RCPblk import RCPblk
from scipy import size

def mqtt_pubBlk(pout,topic):
    """

    Call:   mqtt_pubBlk(pout, topic)

    Parameters
    ----------
       pout: connected output port(s)
      topic : topic to publish
       

    Returns
    -------
        blk  : RCPblk

    """
   

    blk = RCPblk('mqtt_pub',pin,[],[0,0],1,[],[0],topic)
    return blk

