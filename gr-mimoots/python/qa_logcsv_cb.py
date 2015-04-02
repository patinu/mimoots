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

class qa_logcsv_cb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        flags =  (1,1,1,1,1,1)
        src_data = 6*(100*(0+0j,)+100*(3+3j,)+100*(0+0j,))
        expected_result = flags.count(1)*100*(3+3j,)
        
        src = blocks.vector_source_c(data=src_data,vlen=300)
        #trigger = blocks.vector_source_b(data=flags)
        dst = blocks.vector_sink_c(vlen=100);
        csv = mimoots.logcsv_cb(fft_length=300, used_tones=100)
        
        self.tb.connect(src, (csv,0))
        #self.tb.connect(trigger, (csv,1))
        self.tb.connect(csv, dst)

        self.tb.run()
        
        result_data = dst.data()
        
        self.assertComplexTuplesAlmostEqual(expected_result, result_data, flags.count(1)*100)

if __name__ == '__main__':
    gr_unittest.run(qa_logcsv_cb, "qa_logcsv_cb.xml")
