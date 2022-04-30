"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.system = pmt.intern("system")
        self.portName = 'Done'
        self.message_port_register_in(self.system)
        self.message_port_register_out(pmt.intern(self.portName))
        self.selector = True
        
    def set_msg_handler(self, msg):
    	PMT_msg=pmt.pmt_t(msg)
    	self.system_handler(msg)
        
        
    def handle_msg(self, msg):
    	PMT_msg=pmt.intern("Done")
    	self.message_port_pub(pmt.intern(self.portName), PMT_msg)
    		

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] 
        #if input_items[0] == None:
        	#Print("Donedf")
        return len(output_items[0])
