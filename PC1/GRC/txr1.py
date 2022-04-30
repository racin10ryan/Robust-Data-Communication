#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tx_R1
# Author: ryan
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from build_packet_new import build_packet_new  # grc-generated hier_block
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import pdu
from xmlrpc.server import SimpleXMLRPCServer
import threading
import osmosdr
import time



from gnuradio import qtgui

class txr1(gr.top_block, Qt.QWidget):

    def __init__(self, freq=915e6, samp_rate=2e6, transmit_divider=1/10):
        gr.top_block.__init__(self, "Tx_R1", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tx_R1")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "txr1")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

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
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.qtgui_time_sink_x_0_2_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'File Source Time', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_2_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_2_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_2_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_2_0.enable_tags(True)
        self.qtgui_time_sink_x_0_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_2_0.enable_grid(False)
        self.qtgui_time_sink_x_0_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_2_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_2_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_2_0_win)
        self.qtgui_time_sink_x_0_2 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'Transmit Time', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_2.set_update_time(0.10)
        self.qtgui_time_sink_x_0_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_2.enable_tags(True)
        self.qtgui_time_sink_x_0_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_2.enable_autoscale(False)
        self.qtgui_time_sink_x_0_2.enable_grid(False)
        self.qtgui_time_sink_x_0_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_2_win)
        self.pdu_tags_to_pdu_x_0 = pdu.tags_to_pdu_c(pmt.intern('SOB'), pmt.intern('EOB'), 1024, samp_rate, [], False, 0, 0.0)
        self.pdu_tags_to_pdu_x_0.set_eob_parameters(1, 0)
        self.pdu_tags_to_pdu_x_0.enable_time_debug(False)
        self.osmosdr_sink_0_1 = osmosdr.sink(
            args="numchan=" + str(1) + " " + 'hackrf=0000000000000000f77c60dc235e53c3'
        )
        self.osmosdr_sink_0_1.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_sink_0_1.set_sample_rate(samp_rate)
        self.osmosdr_sink_0_1.set_center_freq(freq, 0)
        self.osmosdr_sink_0_1.set_freq_corr(0, 0)
        self.osmosdr_sink_0_1.set_gain(14, 0)
        self.osmosdr_sink_0_1.set_if_gain(47, 0)
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
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("Test"), 1000)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_interleaved_char_to_complex_0 = blocks.interleaved_char_to_complex(False,1.0)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, '/home/ryan/Documents/Tests/input.txt', False, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_copy_0 = blocks.copy(gr.sizeof_char*1)
        self.blocks_copy_0.set_enabled(True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.pdu_tags_to_pdu_x_0, 'pdus'), (self.blocks_message_strobe_0, 'set_msg'))
        self.connect((self.blocks_copy_0, 0), (self.build_packet_new_0_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_copy_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_interleaved_char_to_complex_0, 0))
        self.connect((self.blocks_interleaved_char_to_complex_0, 0), (self.qtgui_time_sink_x_0_2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.osmosdr_sink_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.qtgui_time_sink_x_0_2, 0))
        self.connect((self.build_packet_new_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.build_packet_new_0_0, 0), (self.pdu_tags_to_pdu_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "txr1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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
        self.pdu_tags_to_pdu_x_0.set_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_2.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_2_0.set_samp_rate(self.samp_rate)

    def get_transmit_divider(self):
        return self.transmit_divider

    def set_transmit_divider(self, transmit_divider):
        self.transmit_divider = transmit_divider
        self.blocks_multiply_const_vxx_0_0.set_k(self.transmit_divider)

    def get_payload_chosen_constellation(self):
        return self.payload_chosen_constellation

    def set_payload_chosen_constellation(self, payload_chosen_constellation):
        self.payload_chosen_constellation = payload_chosen_constellation
        self.build_packet_new_0_0.set_payload_constell(self.payload_chosen_constellation)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default=eng_notation.num_to_str(float(915e6)),
        help="Set Frequency [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(2e6)),
        help="Set Sample Rate [default=%(default)r]")
    parser.add_argument(
        "--transmit-divider", dest="transmit_divider", type=eng_float, default=eng_notation.num_to_str(float(1/10)),
        help="Set Transmit Divider [default=%(default)r]")
    return parser


def main(top_block_cls=txr1, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(freq=options.freq, samp_rate=options.samp_rate, transmit_divider=options.transmit_divider)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()