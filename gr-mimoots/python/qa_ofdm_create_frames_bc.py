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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from gnuradio import digital
from gnuradio.gr import packet_utils
from ofdm_create_frames_bc import ofdm_create_frames_bc

class qa_ofdm_create_frames_bc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        packet_len_tag = "packet_length"

        self.payload_constellation = digital.constellation_bpsk()
        
        self.data = [[0,],]
        
        self.create_frames = ofdm_create_frames_bc(
                data=self.data,
                constellation=digital.constellation_8psk())
        
        self.data_sink = blocks.file_sink(gr.sizeof_gr_complex, 'testdata.dat')
        
        self.tb.connect(self.create_frames, self.data_sink)
        
        # set up fg
        self.tb.run ()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_ofdm_create_frames_bc, "qa_ofdm_create_frames_bc.xml")
