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
import mimoots_swig as mimoots

class qa_ofdm_scale_symbol_vcvc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        data = (2j,1-2j,3+4j,-4, 4j, 3+4j, 3+3j, 2-3j, 3+4j)
        data_expected = (0.4j, 0.2-0.4j, 0.6+0.8j, -0.8, 0.8j, 0.6+0.8j, 0.6+0.6j, 0.4-0.6j, 0.6+0.8j)
        vlen = 3
        scale = 0.8
        
        source = blocks.vector_source_c(data=data, vlen=vlen)
        normalize = mimoots.ofdm_scale_symbol_vcvc(symbol_len=vlen, scale=scale)
        sink = blocks.vector_sink_c(vlen=vlen)
        
        self.tb.connect(source, normalize, sink)
        
        self.tb.run()
        
        data_expected = [scale*x for x in data_expected]
        data_result = sink.data()
        
        self.assertComplexTuplesAlmostEqual(data_expected, data_result, vlen)

if __name__ == '__main__':
    gr_unittest.run(qa_ofdm_scale_symbol_vcvc, "qa_ofdm_scale_symbol_vcvc.xml")
