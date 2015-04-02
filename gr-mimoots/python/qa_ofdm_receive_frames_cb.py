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
from ofdm_receive_frames_cb import ofdm_receive_frames_cb
from ofdm_create_frames_bc import ofdm_create_frames_bc

class qa_ofdm_receive_frames_cb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        self.create_frames = ofdm_create_frames_bc(constellation = digital.constellation_8psk())
        self.receive_frames = ofdm_receive_frames_cb(constellation = digital.constellation_8psk())
        
        self.data_sink = blocks.vector_sink_b()
        
        self.tb.connect(self.create_frames, self.receive_frames, self.data_sink)
        self.tb.run ()
        # check data
        print(self.data_sink.data())

if __name__ == '__main__':
    gr_unittest.run(qa_ofdm_receive_frames_cb, "qa_ofdm_receive_frames_cb.xml")
