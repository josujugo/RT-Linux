from supsisim.RCPblk import RCPblk
from scipy import size

def ledBlk(pin,pinN):
    """

    Call:   ledBlk(pin, pinN)

    Parameters
    ----------
       pin: connected input port(s)
       pinN: pin number
       

    Returns
    -------
        blk  : RCPblk

    """
   
    blk = RCPblk('ledp',pin,[],[0,0],0,[],[pinN])
    return blk

