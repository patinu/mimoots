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
from gnuradio import digital
from gnuradio import fft
from mimoots import utils

class ofdm_frame_to_symbols_vcc(gr.hier_block2):
    """
    docstring for block ofdm_frame_to_symbols_vcc
    """
    def __init__(self, fft_len, cp_len, 
                 occupied_carriers, pilot_carriers, pilot_symbols,
                 constellation, nofdm_symbols, packet_len_tag):
        gr.hier_block2.__init__(self,
                "ofdm_frame_to_symbols_vcc",
                gr.io_signature(1, 1, fft_len*gr.sizeof_gr_complex),
                gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        
        self.fft_len = fft_len
        self.cp_len = cp_len
        self.occupied_carriers = occupied_carriers
        self.pilot_carriers = pilot_carriers
        self.pilot_symbols = pilot_symbols
        self.constellation = constellation
        self.nofdm_symbols = nofdm_symbols;
        self.packet_len_tag = packet_len_tag
        
        self.frame_len_tag_key = "frame_length"

        self.fft_payload = fft.fft_vcc(
                fft_size = self.fft_len,
                forward = True, 
                window = (), 
                shift = True
        )
        
        self.chanest = digital.ofdm_chanest_vcvc(
                sync_symbol1 = utils.ofdm_make_sync_word1(
                        self.fft_len, 
                        self.occupied_carriers, 
                        self.pilot_carriers
                ),
                sync_symbol2 = utils.ofdm_make_sync_word2(
                        self.fft_len,
                        self.occupied_carriers,
                        self.pilot_carriers
                ),
                n_data_symbols = self.nofdm_symbols
        )
            
        self.payload_equalizer = digital.ofdm_equalizer_simpledfe(
                fft_len = self.fft_len,
                constellation = self.constellation.base(),
                occupied_carriers = self.occupied_carriers,
                pilot_carriers = self.pilot_carriers,
                pilot_symbols = self.pilot_symbols,
                symbols_skipped = 0
        )
        
        self.payload_eq = digital.ofdm_frame_equalizer_vcvc(
                equalizer = self.payload_equalizer.base(),
                cp_len = cp_len,
                len_tag_key = self.frame_len_tag_key,
                propagate_channel_state = True,
                fixed_frame_len = self.nofdm_symbols
        )
    
        # doesn't accept names of parameters
        self.payload_serializer = digital.ofdm_serializer_vcc(
                self.fft_len, # fft_len = 
                self.occupied_carriers, # occupied_carriers = 
                self.frame_len_tag_key, # len_tag_key =
                self.packet_len_tag, # packet_len_tag = 
                0 # symbolsskipped = 
        )
        
        self.connect(self, self.fft_payload, self.chanest, self.payload_eq,
                     self.payload_serializer, self)
