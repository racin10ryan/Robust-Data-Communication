#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tx
# Author: ryan
# GNU Radio version: 3.10.1.1

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from build_packet_new import build_packet_new  # grc-generated hier_block
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from xmlrpc.server import SimpleXMLRPCServer
import threading
import osmosdr
import time




class tx(gr.top_block):

    def __init__(self, freq=922e6, samp_rate=2e6, transmit_divider=1/47):
        gr.top_block.__init__(self, "Tx", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.freq = freq
        self.samp_rate = samp_rate
        self.transmit_divider = transmit_divider

        ##################################################
        # Variables
        ##################################################
        self.payload_chosen_constellation = payload_chosen_constellation = digital.constellation_bpsk().base()

        ##################################################
        # Blocks
        ##################################################
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8002), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.osmosdr_sink_0_1 = osmosdr.sink(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_sink_0_1.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_sink_0_1.set_sample_rate(samp_rate)
        self.osmosdr_sink_0_1.set_center_freq(freq, 0)
        self.osmosdr_sink_0_1.set_freq_corr(0, 0)
        self.osmosdr_sink_0_1.set_gain(0, 0)
        self.osmosdr_sink_0_1.set_if_gain(0, 0)
        self.osmosdr_sink_0_1.set_bb_gain(0, 0)
        self.osmosdr_sink_0_1.set_antenna('', 0)
        self.osmosdr_sink_0_1.set_bandwidth(samp_rate, 0)
        self.build_packet_new_0_0 = build_packet_new(
            divide=1,
            header_constell=digital.constellation_bpsk(),
            payload_constell=payload_chosen_constellation,
            samp_rate=samp_rate,
        )
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(transmit_divider)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, '/media/ryan/New Volume/Senior Design/Working On/PC1/packet.ddi', False, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_copy_0 = blocks.copy(gr.sizeof_char*1)
        self.blocks_copy_0.set_enabled(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_copy_0, 0), (self.build_packet_new_0_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_copy_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.osmosdr_sink_0_1, 0))
        self.connect((self.build_packet_new_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))

    def changeConstellations(self, constellString):
        temp = None
        if constellString == "BPSK":
            temp = digital.constellation_bpsk().base()
        elif constellString == "QPSK":
            temp = digital.constellation_qpsk().base()
        elif constellString == "16QAM":
            temp = digital.constellation_16qam().base()
        self.set_payload_chosen_constellation(temp)

    def enableFlow(self, d_enable):
        self.blocks_copy_0.set_enabled(d_enable)

    def configureFile(self):
        self.disconnect((self.blocks_file_source_0_0, 0), (self.blocks_copy_0, 0))
        self.disconnect((self.blocks_file_source_0_0, 0), (self.blocks_interleaved_char_to_complex_0, 0))
        self.blocks_file_source_0_0.close()
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, str(os.getcwd())+'/packet.ddi', False, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)

        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_copy_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_interleaved_char_to_complex_0, 0))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0_1.set_center_freq(self.freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.build_packet_new_0_0.set_samp_rate(self.samp_rate)
        self.osmosdr_sink_0_1.set_sample_rate(self.samp_rate)
        self.osmosdr_sink_0_1.set_bandwidth(self.samp_rate, 0)

    def get_transmit_divider(self):
        return self.transmit_divider

    def set_transmit_divider(self, transmit_divider):
        self.transmit_divider = transmit_divider
        self.blocks_multiply_const_vxx_0_0.set_k(self.transmit_divider)

    def get_payload_chosen_constellation(self):
        return self.payload_chosen_constellation

    def set_payload_chosen_constellation(self, payload_chosen_constellation):
        self.disconnect((self.blocks_copy_0, 0), (self.build_packet_new_0_0, 0))
        self.disconnect((self.build_packet_new_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.build_packet_new_0_0 = build_packet_new(
            divide=1,
            header_constell=digital.constellation_bpsk(),
            payload_constell=payload_chosen_constellation,
            samp_rate=self.samp_rate,
        )
        self.connect((self.blocks_copy_0, 0), (self.build_packet_new_0_0, 0))
        self.connect((self.build_packet_new_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0)))



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default=eng_notation.num_to_str(float(922e6)),
        help="Set Frequency [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(2e6)),
        help="Set Sample Rate [default=%(default)r]")
    parser.add_argument(
        "--transmit-divider", dest="transmit_divider", type=eng_float, default=eng_notation.num_to_str(float(1/47)),
        help="Set Transmit Divider [default=%(default)r]")
    return parser


def main(top_block_cls=tx, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(freq=options.freq, samp_rate=options.samp_rate, transmit_divider=options.transmit_divider)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
