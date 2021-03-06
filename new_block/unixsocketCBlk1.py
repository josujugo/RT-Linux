from supsisim.RCPblk import RCPblk
from scipy import size

def unixsocketCBlk1(pin, pout,sockname):
    """

    Call:   unixsocketCBlk1(pin,pout, sockname)

    Parameters
    ----------
       pin: connected input port(s)
       pout: connected output port(s)
       sockname : Socket

    Returns
    -------
        blk  : RCPblk

    """
    
    blk = RCPblk('unixsockC1',pin,pout,[0,0],1,[],[0],'/tmp/'+sockname)
    return blk

