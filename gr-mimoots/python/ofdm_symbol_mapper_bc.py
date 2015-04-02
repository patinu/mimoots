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

class ofdm_symbol_mapper_bc(gr.hier_block2):
    """
    docstring for block ofdm_symbol_mapper_bc
    """
    def __init__(self, constellation, packet_len_tag, verbose=False):
        gr.hier_block2.__init__(
            self,
            "ofdm_symbol_mapper_bc",
            gr.io_signature(1, 1, gr.sizeof_char),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_gr_complex)
        ) # Output signature
        
        self.constellation = constellation
        self.packet_len_tag = packet_len_tag

        self.payload_unpack = blocks.repack_bits_bb(
                k=8,
                l=self.constellation.bits_per_symbol(),
                len_tag_key=self.packet_len_tag
        )

        self.payload_mod = digital.chunks_to_symbols_bc(
                symbol_table=self.constellation.points()
        )

        # Define blocks and connect them
        self.connect(self, self.payload_unpack, self.payload_mod, self)
        
        if verbose==True:
            self.connect(self, blocks.file_sink(
                    itemsize=gr.sizeof_char,
                    filename='ofdm_symbol_mapper_input.gr')
            )
            self.connect(self.payload_unpack, blocks.file_sink(
                    itemsize=gr.sizeof_char,
                    filename='ofdm_symbol_mapper_payload_unpack.gr')
            )
            self.connect(self.payload_mod, blocks.file_sink(
                    itemsize=gr.sizeof_gr_complex,
                    filename='ofdm_symbol_mapper_payload_mod.gr')
            )
