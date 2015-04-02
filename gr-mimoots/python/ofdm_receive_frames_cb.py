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
from gnuradio import analog
from mimoots import utils
import mimoots


class ofdm_receive_frames_cb(gr.hier_block2):
    """
    docstring for block ofdm_receive_frames_cb
    """
    def __init__(self, 
                 fft_len = 64, 
                 cp_len = 16,
                 nofdm_symbols = 10,
                 nofdm_frames = 1,
                 ofdm_symbol_scale = 1,
                 constellation = digital.constellation_bpsk(),
                 occupied_carriers = (range(-26, -21) + range(-20, -7) + 
                                      range(-6, 0) + range(1, 7) + 
                                      range(8, 21) + range(22, 27),),
                 pilot_carriers = ((-21, -7, 7, 21),),
                 pilot_symbols = tuple([(1, -1, 1, -1),]),
                 seq_seed = 42,
                 debug = False
    ):
        gr.hier_block2.__init__(self,
            "ofdm_receive_frames_cb",
            gr.io_signature(1, 1, gr.sizeof_gr_complex),  # Input signature
            gr.io_signature(1, 1, gr.sizeof_char)) # Output signature
            
        # =====================================================================
        # Generate class-members
        # =====================================================================
        
        self._def_occupied_carriers = occupied_carriers
        self._def_pilot_carriers = pilot_carriers
        self._def_pilot_symbols = pilot_symbols
        self._seq_seed = seq_seed
        self.fft_len = fft_len
        self.cp_len = cp_len
        self.ofdm_symbol_scale = ofdm_symbol_scale
        self.constellation = constellation
            
        self.packet_len_tag = "packet_length"
        self.frame_len_tag_key = "frame_length"
        self.nofdm_symbols = nofdm_symbols
        self.nofdm_frames = nofdm_frames
        
        self.debug = debug

        # =====================================================================
        # Create all blocks
        # =====================================================================
        # TODO: rename some blocks

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
    
        fft_payload = fft.fft_vcc(
                fft_size = self.fft_len, 
                forward = True, 
                window = (), 
                shift = True
        )
    
        chanest = digital.ofdm_chanest_vcvc(
                sync_symbol1 = utils.ofdm_make_sync_word1(self.fft_len, 
                                            self._def_occupied_carriers, 
                                            self._def_pilot_carriers),
                sync_symbol2 = utils.ofdm_make_sync_word2(self.fft_len,
                                            self._def_occupied_carriers,
                                            self._def_pilot_carriers),
                n_data_symbols = self.nofdm_symbols
        )
            
        payload_equalizer = digital.ofdm_equalizer_simpledfe(
                fft_len = self.fft_len,
                constellation = self.constellation.base(),
                occupied_carriers = self._def_occupied_carriers,
                pilot_carriers = self._def_pilot_carriers,
                pilot_symbols = self._def_pilot_symbols,
                symbols_skipped = 0,
        )
        
        payload_eq = digital.ofdm_frame_equalizer_vcvc(
                equalizer = payload_equalizer.base(),
                cp_len = cp_len,
                len_tag_key = self.frame_len_tag_key,
                propagate_channel_state = True,
                fixed_frame_len = self.nofdm_symbols
        )
    
        # doesn't accept names of parameters
        payload_serializer = digital.ofdm_serializer_vcc(
                self.fft_len, # fft_len = 
                self._def_occupied_carriers, # occupied_carriers = 
                self.frame_len_tag_key, # len_tag_key =
                self.packet_len_tag, # packet_len_tag = 
                0 # symbolsskipped = 
        )
    
        payload_demod = digital.constellation_decoder_cb(
                constellation = self.constellation.base()
        )
    
        payload_pack = blocks.repack_bits_bb(
                k = self.constellation.bits_per_symbol(),
                l = 8,
                len_tag_key = self.packet_len_tag,
                align_output = True
        )
        
        # =====================================================================
        # Connect all blocks
        # =====================================================================
        # TODO: Clean up graph
       
        self.connect(self, sync_detect)
              
        self.connect((sync_detect,0), oscillator, (mixer,0))
        self.connect((self,0), delay, (mixer,1))
        self.connect((sync_detect,1), (frames,1))
    
        self.connect(mixer, (frames,0), fft_payload, chanest,
                     payload_eq, payload_serializer, payload_demod, 
                     payload_pack, self)
            
        # =====================================================================
        # Debug-Output
        # =====================================================================
        if self.debug == True:
            self.connect(self, 
                         blocks.file_sink(gr.sizeof_gr_complex,
                                          'receive-self.dat'))

            self.connect((sync_detect,0), 
                         blocks.file_sink(gr.sizeof_float,
                                          'receive-sync_detect-0.dat'))

            self.connect((sync_detect,1), 
                         blocks.file_sink(gr.sizeof_char,
                                          'receive-sync_detect-1.dat'))

            self.connect(mixer, 
                         blocks.file_sink(gr.sizeof_gr_complex,
                                          'receive-mixer.dat'))
                                          
            self.connect(frames, 
                         blocks.file_sink(fft_len*gr.sizeof_gr_complex,
                                          'receive-frames.dat'))
                                          
            self.connect(fft_payload, 
                         blocks.file_sink(self.fft_len*gr.sizeof_gr_complex,
                                          'receive-fft_payload.dat'))

            self.connect(chanest, 
                         blocks.file_sink(self.fft_len*gr.sizeof_gr_complex,
                                          'receive-chanest.dat'))
            self.connect(payload_eq, 
                         blocks.file_sink(self.fft_len*gr.sizeof_gr_complex,
                                          'receive-payload_eq.dat'))
            self.connect(payload_serializer, 
                         blocks.file_sink(gr.sizeof_char*8,
                                          'receive-payload_serializer.dat'))

