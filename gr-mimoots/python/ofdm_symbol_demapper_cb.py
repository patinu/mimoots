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

class ofdm_symbol_demapper_cb(gr.hier_block2):
    """
    docstring for block ofdm_symbol_demapper_cb
    """
    def __init__(self, constellation, packet_len_tag):
        gr.hier_block2.__init__(
            self,
            "ofdm_symbol_demapper_cb",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),
            gr.io_signature(1, 1, gr.sizeof_char)
        )
        
        self.constellation = constellation;
        self.packet_len_tag = packet_len_tag;
        
        payload_demod = digital.constellation_decoder_cb(
                constellation = self.constellation.base()
        )
    
        payload_repack = blocks.repack_bits_bb(
                k = self.constellation.bits_per_symbol(),
                l = 8,
                len_tag_key = self.packet_len_tag,
                align_output = True
        )

        # Define blocks and connect them
        self.connect(self, payload_demod, payload_repack, self)
