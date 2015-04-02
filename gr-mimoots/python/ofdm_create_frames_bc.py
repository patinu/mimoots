#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Paul Machemehl
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
""" blubb """
from gnuradio import gr
from gnuradio import digital
from gnuradio import blocks
from gnuradio import fft
from gnuradio.gr import packet_utils
from mimoots import utils
import mimoots
import numpy
import random

class ofdm_create_frames_bc(gr.hier_block2):
    """
    blabla
    """
    def __init__(self,
                 data=[[],],
                 fft_len=64,
                 cp_len=16,
                 nofdm_symbols=10,
                 nofdm_frames=1,
                 ofdm_symbol_scale=1,
                 constellation=digital.constellation_bpsk(),
                 occupied_carriers=(range(-26, -21) + range(-20, -7) +
                                    range(-6, 0) + range(1, 7) +
                                    range(8, 21) + range(22, 27),),
                 pilot_carriers=((-21, -7, 7, 21),),
                 pilot_symbols=tuple([(1, -1, 1, -1),]),
                 scale=1.0,
                 seq_seed=42,
                 debug=False
    ):
        gr.hier_block2.__init__(self,
            "ofdm_create_frames_bc",
            gr.io_signature(0, 0, 0),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_gr_complex)) # Output signature

        # =====================================================================
        # Generate class-members
        # =====================================================================
        self._def_occupied_carriers = occupied_carriers
        self._def_pilot_carriers = pilot_carriers
        self._def_pilot_symbols = pilot_symbols
        self._seq_seed = seq_seed

        self.data = data
        self.fft_len = fft_len
        self.cp_len = cp_len
        self.ofdm_symbol_scale = ofdm_symbol_scale
        self.constellation = constellation

        self.packet_len_tag = "packet_length"
        self.frame_length_tag_key = "frame_length"
        self.nofdm_symbols = nofdm_symbols
        self.nofdm_frames = nofdm_frames
        self.scale = scale

        self.debug = debug

        # =====================================================================
        # Create data to convert into OFDM-Frames
        # =====================================================================

        random.seed(self._seq_seed)

        self.data_len = utils.ofdm_get_data_len(
                nofdm_symbols=self.nofdm_symbols,
                noccupied_carriers=len(self._def_occupied_carriers[0]),
                constellation=constellation
        )

        if debug == True:
            print 'Frames: {}'.format(self.nofdm_frames)
            print 'Länge: {}'.format(self.data_len)

        (data_tosend, tags) = packet_utils.packets_to_vectors(
                self.data,
                self.packet_len_tag
        )

        # ===================================================================
        # Create all blocks
        # ===================================================================

        self.data_source = blocks.vector_source_b(
                data=data_tosend,
                vlen=1,
                tags=tags,
                repeat=False
        )

        self.payload_unpack = blocks.repack_bits_bb(
                k=8,
                l=self.constellation.bits_per_symbol(),
                len_tag_key=self.packet_len_tag
        )

        self.payload_mod = digital.chunks_to_symbols_bc(
                symbol_table=self.constellation.points()
        )

        self.allocator = digital.ofdm_carrier_allocator_cvc(
                fft_len=self.fft_len,
                occupied_carriers=self._def_occupied_carriers,
                pilot_carriers=self._def_pilot_carriers,
                pilot_symbols=self._def_pilot_symbols,
                sync_words=[
                    utils.ofdm_make_sync_word1(self.fft_len,
                                          self._def_occupied_carriers,
                                          self._def_pilot_carriers),
                    utils.ofdm_make_sync_word2(self.fft_len,
                                          self._def_occupied_carriers,
                                          self._def_pilot_carriers),
                ],
                len_tag_key=self.packet_len_tag
        )

        self.ffter = fft.fft_vcc(
                fft_size=self.fft_len,
                forward=False,
                window=(),
                shift=True
        )

        self.scale = mimoots.ofdm_scale_symbol_vcvc(
                symbol_len=self.fft_len,
                scale=self.scale
        )

        self.cyclic_prefixer = digital.ofdm_cyclic_prefixer(
                input_size=self.fft_len,
                output_size=self.fft_len+cp_len,
                rolloff_len=0,
                len_tag_key=self.packet_len_tag
        )

        # ===================================================================
        # Connect all blocks
        # ===================================================================

        self.connect(
                self.data_source, self.payload_unpack, self.payload_mod,
                self.allocator, self.ffter, self.scale, self.cyclic_prefixer,
                self
        )
        
        #self.connect(
        #        self.data_source, self.payload_mod, self.payload_unpack,
        #        self.allocator, self.ffter, self.scale, self.cyclic_prefixer,
        #        self
        #)

        # ===================================================================
        # Debug-Output
        # ===================================================================
        if self.debug == True:
            self.connect(self.data_source,
                         blocks.file_sink(gr.sizeof_char,
                                          'create-data_source.dat'))

            self.connect(self.payload_unpack,
                         blocks.file_sink(gr.sizeof_char,
                                          'create-payload_unpack.dat'))

            self.connect(self.payload_mod,
                         blocks.file_sink(gr.sizeof_gr_complex,
                                          'create-payload_mod.dat'))

            self.connect(self.allocator,
                         blocks.file_sink(self.fft_len*gr.sizeof_gr_complex,
                                          'create-allocator.dat'))

            self.connect(self.ffter,
                         blocks.file_sink(self.fft_len*gr.sizeof_gr_complex,
                                          'create-ffter.dat'))

            self.connect(self.scale,
                         blocks.file_sink(self.fft_len*gr.sizeof_gr_complex,
                                          'create-scale.dat'))

            self.connect(self.cyclic_prefixer,
                         blocks.file_sink(gr.sizeof_gr_complex,
                                          'create-cyclic_prefixer.dat'))
