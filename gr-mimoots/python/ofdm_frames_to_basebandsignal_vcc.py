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
import mimoots

class ofdm_frames_to_basebandsignal_vcc(gr.hier_block2):
    """
    docstring for block ofdm_frames_to_basebandsignal_vcc
    """
    def __init__(self, fft_len, cp_len, packet_len_tag, 
                 scale=1, verbose=True):
        gr.hier_block2.__init__(self,
                "ofdm_frames_to_basebandsignal_vcc",
                gr.io_signature(1, 1, fft_len*gr.sizeof_gr_complex),
                gr.io_signature(1, 1, gr.sizeof_gr_complex)
        )
        
        self.fft_len = fft_len
        self.cp_len = cp_len
        self.scale = scale
        self.packet_len_tag = packet_len_tag
            
        self.scaler = mimoots.ofdm_scale_symbol_vcvc(
                symbol_len=self.fft_len,
                scale=self.scale
        )

        self.cyclic_prefixer = digital.ofdm_cyclic_prefixer(
                input_size=self.fft_len,
                output_size=self.fft_len+cp_len,
                rolloff_len=0,
                len_tag_key=self.packet_len_tag
        )

            # Define blocks and connect them
        self.connect(self, self.scaler, self.cyclic_prefixer, self)
        
        if verbose==True:
            self.connect(self, blocks.file_sink(
                    itemsize=self.fft_len*gr.sizeof_gr_complex,
                    filename='ofdm_frames_to_basebandsignal_input.gr')
            )
            self.connect(self.scaler, blocks.file_sink(
                    itemsize=self.fft_len*gr.sizeof_gr_complex,
                    filename='ofdm_frames_to_basebandsignal_scaler.gr')
            )
            self.connect(self.cyclic_prefixer, blocks.file_sink(
                    itemsize=gr.sizeof_gr_complex,
                    filename='ofdm_frames_to_basebandsignal_cyclic_prefixer.gr')
            )
