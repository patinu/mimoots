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
from gnuradio import analog
from gnuradio import digital
import mimoots
from mimoots import utils

class ofdm_basebandsignal_to_frames_cvc(gr.hier_block2):
    """
    docstring for block ofdm_basebandsignal_to_frames_cvc
    """
    def __init__(self, fft_len, cp_len, nofdm_symbols):
        gr.hier_block2.__init__(
                self,
                "ofdm_basebandsignal_to_frames_cvc",
                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                gr.io_signature(1, 1, fft_len*gr.sizeof_gr_complex)
        )
        
        self.fft_len = fft_len
        self.cp_len = cp_len
        self.nofdm_symbols = nofdm_symbols

        sync_detect = digital.ofdm_sync_sc_cfb(
                fft_len = fft_len,
                cp_len = cp_len
        )
        
        delay = blocks.delay(gr.sizeof_gr_complex, self.fft_len+self.cp_len)
        
        oscillator = analog.frequency_modulator_fc(-2.0 / self.fft_len)
        
        mixer = blocks.multiply_cc()
    
        frames = mimoots.ofdm_extract_frame_cvc(
                fft_len = self.fft_len,
                cp_len = self.cp_len,
                nsymbols_per_ofdmframe = self.nofdm_symbols+2 # +2 Sync-Words
        )

        self.connect(self, sync_detect)
        self.connect((sync_detect,0), oscillator, (mixer,0))
        self.connect((self,0), delay, (mixer,1))
        self.connect((sync_detect,1), (frames,1))
        self.connect(mixer, (frames,0))
        
        self.connect(frames, self)
        
        
