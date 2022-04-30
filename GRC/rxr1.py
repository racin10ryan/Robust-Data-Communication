#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Rx_R1
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
from deconstruct_packets_new import deconstruct_packets_new  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from xmlrpc.server import SimpleXMLRPCServer
import threading
import osmosdr
import time



from gnuradio import qtgui

class rxr1(gr.top_block, Qt.QWidget):

    def __init__(self, freq=915e6, rxBB=0, rxIF=40, samp_rate=2e6):
        gr.top_block.__init__(self, "Rx_R1", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Rx_R1")
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

        self.settings = Qt.QSettings("GNU Radio", "rxr1")

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
        self.rxBB = rxBB
        self.rxIF = rxIF
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.payload_chosen_constellation = payload_chosen_constellation = digital.constellation_bpsk().base()

        ##################################################
        # Blocks
        ##################################################
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8001), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.qtgui_time_sink_x_0_2 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'Receiver Time', #name
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
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            'Receiver Freqency ', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.osmosdr_source_0_1 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'hackrf=0000000000000000f77c60dc235e53c3'
        )
        self.osmosdr_source_0_1.set_time_now(osmosdr.time_spec_t(time.time()), osmosdr.ALL_MBOARDS)
        self.osmosdr_source_0_1.set_sample_rate(samp_rate)
        self.osmosdr_source_0_1.set_center_freq(freq, 0)
        self.osmosdr_source_0_1.set_freq_corr(0, 0)
        self.osmosdr_source_0_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0_1.set_gain_mode(True, 0)
        self.osmosdr_source_0_1.set_gain(14, 0)
        self.osmosdr_source_0_1.set_if_gain(rxIF, 0)
        self.osmosdr_source_0_1.set_bb_gain(rxBB, 0)
        self.osmosdr_source_0_1.set_antenna('', 0)
        self.osmosdr_source_0_1.set_bandwidth(samp_rate, 0)
        self.deconstruct_packets_new_0 = deconstruct_packets_new(
            header_mod=digital.constellation_bpsk(),
            multiply=1/128,
            payload_mod=payload_chosen_constellation,
            samp_rate=samp_rate,
            thresh=0.915,
        )
        self.blocks_interleaved_char_to_complex_0 = blocks.interleaved_char_to_complex(False,1.0)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/ryan/Documents/Tests/output.wav', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_copy_0 = blocks.copy(gr.sizeof_gr_complex*1)
        self.blocks_copy_0.set_enabled(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_copy_0, 0), (self.deconstruct_packets_new_0, 0))
        self.connect((self.blocks_copy_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_interleaved_char_to_complex_0, 0), (self.qtgui_time_sink_x_0_2, 0))
        self.connect((self.deconstruct_packets_new_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.deconstruct_packets_new_0, 0), (self.blocks_interleaved_char_to_complex_0, 0))
        self.connect((self.osmosdr_source_0_1, 0), (self.blocks_copy_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rxr1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0_1.set_center_freq(self.freq, 0)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)

    def get_rxBB(self):
        return self.rxBB

    def set_rxBB(self, rxBB):
        self.rxBB = rxBB
        self.osmosdr_source_0_1.set_bb_gain(self.rxBB, 0)

    def get_rxIF(self):
        return self.rxIF

    def set_rxIF(self, rxIF):
        self.rxIF = rxIF
        self.osmosdr_source_0_1.set_if_gain(self.rxIF, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.deconstruct_packets_new_0.set_samp_rate(self.samp_rate)
        self.osmosdr_source_0_1.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0_1.set_bandwidth(self.samp_rate, 0)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_time_sink_x_0_2.set_samp_rate(self.samp_rate)

    def get_payload_chosen_constellation(self):
        return self.payload_chosen_constellation

    def set_payload_chosen_constellation(self, payload_chosen_constellation):
        self.payload_chosen_constellation = payload_chosen_constellation
        self.deconstruct_packets_new_0.set_payload_mod(self.payload_chosen_constellation)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--freq", dest="freq", type=eng_float, default=eng_notation.num_to_str(float(915e6)),
        help="Set Frequency [default=%(default)r]")
    parser.add_argument(
        "--rxBB", dest="rxBB", type=intx, default=0,
        help="Set Receiver Baseband Gain [default=%(default)r]")
    parser.add_argument(
        "--rxIF", dest="rxIF", type=intx, default=40,
        help="Set Receiver IF Gain [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(2e6)),
        help="Set Sample Rate [default=%(default)r]")
    return parser


def main(top_block_cls=rxr1, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(freq=options.freq, rxBB=options.rxBB, rxIF=options.rxIF, samp_rate=options.samp_rate)

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
