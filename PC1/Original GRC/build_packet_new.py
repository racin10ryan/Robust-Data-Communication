# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Build Packet New
# Author: ryan
# GNU Radio version: 3.10.1.1

from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal







class build_packet_new(gr.hier_block2):
    def __init__(self, divide=1, header_constell=digital.constellation_bpsk(), payload_constell=digital.constellation_bpsk(), samp_rate=20000000):
        gr.hier_block2.__init__(
            self, "Build Packet New",
                gr.io_signature(1, 1, gr.sizeof_char*1),
                gr.io_signature.makev(3, 3, [gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1, gr.sizeof_gr_complex*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.divide = divide
        self.header_constell = header_constell
        self.payload_constell = payload_constell
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.occupied_carriers = occupied_carriers = (list(range(-26, -21)) + list(range(-20, -7)) + list(range(-6, 0)) + list(range(1, 7)) + list(range(8, 21)) + list(range(22, 27)),)
        self.length_tag_key = length_tag_key = "packet_len"
        self.H = H = fec.ldpc_H_matrix(gr.prefix() + "/share/gnuradio/fec/ldpc/" + "n_0100_k_0042_gap_02.alist", 2)
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.rolloff = rolloff = 0
        self.pilot_symbols = pilot_symbols = ((1, 1, 1, -1,),)
        self.pilot_carriers = pilot_carriers = ((-21, -7, 7, 21,),)
        self.packet_len = packet_len = 52
        self.ldpc_enc_H = ldpc_enc_H = fec.ldpc_par_mtrx_encoder_make_H(H)
        self.header_format = header_format = digital.header_format_ofdm(occupied_carriers, 1, length_tag_key,)
        self.fft_len = fft_len = 64

        ##################################################
        # Blocks
        ##################################################
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.fec_extended_tagged_encoder_0_0 = fec.extended_tagged_encoder(encoder_obj_list=ldpc_enc_H, puncpat='11', lentagname=length_tag_key, mtu=1512)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(header_format, length_tag_key)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(
            fft_len,
            fft_len + int(fft_len/4),
            rolloff,
            length_tag_key)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2), length_tag_key, True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, length_tag_key, False)
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bc(payload_constell.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(header_constell.points(), 1)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, length_tag_key, 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, length_tag_key)
        self.blocks_repack_bits_bb_0_0_0 = blocks.repack_bits_bb(8, payload_constell.bits_per_symbol(), length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, header_constell.bits_per_symbol(), length_tag_key, False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(divide)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self, 2))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.fec_extended_tagged_encoder_0_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.fec_extended_tagged_encoder_0_0, 0), (self.blocks_repack_bits_bb_0_0_0, 0))
        self.connect((self.fec_extended_tagged_encoder_0_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self, 0), (self.blocks_throttle_0, 0))


    def get_divide(self):
        return self.divide

    def set_divide(self, divide):
        self.divide = divide
        self.blocks_multiply_const_vxx_1.set_k(self.divide)

    def get_header_constell(self):
        return self.header_constell

    def set_header_constell(self, header_constell):
        self.header_constell = header_constell

    def get_payload_constell(self):
        return self.payload_constell

    def set_payload_constell(self, payload_constell):
        self.payload_constell = payload_constell

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, 1, self.length_tag_key,))

    def get_H(self):
        return self.H

    def set_H(self, H):
        self.H = H

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_ldpc_enc_H(self):
        return self.ldpc_enc_H

    def set_ldpc_enc_H(self, ldpc_enc_H):
        self.ldpc_enc_H = ldpc_enc_H

    def get_header_format(self):
        return self.header_format

    def set_header_format(self, header_format):
        self.header_format = header_format

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len

