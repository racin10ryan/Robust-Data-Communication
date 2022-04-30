#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: rd1zmq
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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading
import osmosdr
import time



from gnuradio import qtgui

class rd1zmq(gr.top_block, Qt.QWidget):

    def __init__(self, freq=915e6, rxBB=0, rxIF=40, samp_rate=2e6):
        gr.top_block.__init__(self, "rd1zmq", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("rd1zmq")
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

        self.settings = Qt.QSettings("GNU Radio", "rd1zmq")

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
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:1234', 100, False, -1, "")
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8004), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
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


        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0_1, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.osmosdr_source_0_1, 0), (self.zeromq_pub_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rd1zmq")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_0_1.set_center_freq(self.freq, 0)

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
        self.osmosdr_source_0_1.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0_1.set_bandwidth(self.samp_rate, 0)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)



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


def main(top_block_cls=rd1zmq, options=None):
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
