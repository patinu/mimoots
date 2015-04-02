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

class uhd_sink2(gr.hier_block2):
    """
    docstring for block uhd_sink2
    """
    def __init__(self, freq, gain=None, samp_rate=500000, antenna="TX/RX",
                 addr=("addr0=192.168.10.2", "addr1=192.168.10.3")):
        gr.hier_block2.__init__(
                self, "uhd_sink2",
                gr.io_signature(2, 2, gr.sizeof_gr_complex),
                gr.io_signature(0, 0, 0)
        )
        
        if not isinstance(addr , (list, tuple)):
            raise TypeError("{}: has to be a list or tuple!".format("addr"))
        else:
            self.addr = addr;
            
        self.samp_rate = samp_rate
        
        self.freq = self.__single_parameter_to_list(freq)
        self.gain = self.__single_parameter_to_list(gain)
        self.antenna = self.__single_parameter_to_list(antenna)
        
        self.u = uhd.usrp_sink(
                ",".join(addr),
                uhd.stream_args(
                    cpu_format="fc32",
                    channels=range(2),
                ),
        )

        self.u.set_samp_rate(samp_rate)
        self.u.set_clock_source("mimo", 1)
        self.u.set_time_source("mimo", 1)
        
        for chan in range(2):
            self.u.set_antenna(self.antenna[chan], chan)
            self.u.set_center_freq(self.freq[chan], chan)
        
            if self.gain[chan] is None:
                g = self.u.get_gain_range(chan)
                self.gain[chan] = float(g.start()+g.stop())/2
            self.u.set_gain(self.gain[chan], chan)
        
        self.connect((self, 0), (self.u, 0))
        self.connect((self, 1), (self.u, 1))
        
    def __single_parameter_to_list(self, param):
        if isinstance(param, (list, tuple)):
            if len(param) == 1:
                return (param[0], param[0])
            else:
                return param
        else:
            return [param, param]
