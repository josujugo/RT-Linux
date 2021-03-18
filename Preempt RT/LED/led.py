from supsisim.RCPblk import RCPblk
from scipy import size

def ledBlk(pout,topic):
    """

    Call:   ledBlk(pin, pin_number)

    Parameters
    ----------
       pin: connected input port(s)
       pinN: pin number
       

    Returns
    -------
        blk  : RCPblk

    """
   

    blk = RCPblk('led',pin,[],[0,0],1,[],[0],pinN)
    return blk

