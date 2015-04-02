#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
from gnuradio import fft
from mimoots import utils

class ofdm_symbols_to_frame_cvc(gr.hier_block2):
    """
    docstring for block ofdm_symbols_to_frame_cvc
    """
    def __init__(self, fft_len, cp_len, 
                 occupied_carriers, pilot_carriers, pilot_symbols,
                 packet_len_tag, verbose=False):
        gr.hier_block2.__init__(
                self,
                "ofdm_symbols_to_frame_cvc",
                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                gr.io_signature(1, 1, fft_len*gr.sizeof_gr_complex)
        )
        
        self.fft_len = fft_len
        self.cp_len = cp_len
        self.occupied_carriers = occupied_carriers
        self.pilot_carriers = pilot_carriers
        self.pilot_symbols = pilot_symbols
        self.packet_len_tag = packet_len_tag
        
        self.allocator = digital.ofdm_carrier_allocator_cvc(
                fft_len=self.fft_len,
                occupied_carriers=self.occupied_carriers,
                pilot_carriers=self.pilot_carriers,
                pilot_symbols=self.pilot_symbols,
                sync_words=[
                    utils.ofdm_make_sync_word1(self.fft_len,
                                               self.occupied_carriers,
                                               self.pilot_carriers),
                    utils.ofdm_make_sync_word2(self.fft_len,
                                               self.occupied_carriers,
                                               self.pilot_carriers),
                ],
                len_tag_key=self.packet_len_tag
        )

        self.ffter = fft.fft_vcc(
                fft_size=self.fft_len,
                forward=False,
                window=(),
                shift=True
        )

        self.connect(self, self.allocator, self.ffter, self)
        
        if verbose==True:
            self.connect(self, blocks.file_sink(
                    itemsize=gr.sizeof_gr_complex,
                    filename='ofdm_symbols_to_frame_input.gr')
            )
            self.connect(self.allocator, blocks.file_sink(
                    itemsize=self.fft_len*gr.sizeof_gr_complex,
                    filename='ofdm_symbols_to_frame_allocator.gr')
            )
            self.connect(self.ffter, blocks.file_sink(
                    itemsize=self.fft_len*gr.sizeof_gr_complex,
                    filename='ofdm_symbols_to_frame_ffter.gr')
            )
