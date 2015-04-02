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
from gnuradio import uhd

class uhd_sink(gr.hier_block2):
    """
    docstring for block uhd_sink
    """
    def __init__(self, freq, gain=None, samp_rate=500000, antenna="TX/RX"):
        gr.hier_block2.__init__(
                self, "uhd_sink",
                gr.io_signature(1, 1, gr.sizeof_gr_complex),
                gr.io_signature(0, 0, 0)
        )
                
        self.u = uhd.usrp_sink(
                ",".join(("", "")),
                uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(1),
                ),
        )
            
        self.u.set_antenna(antenna, 0)
        self.u.set_samp_rate(samp_rate)
        self.u.set_center_freq(freq, 0)
        
        if gain is None:
            g = self.u.get_gain_range()
            gain = float(g.start()+g.stop())/2
        self.u.set_gain(gain, 0)
        
        self.connect(self, self.u)
