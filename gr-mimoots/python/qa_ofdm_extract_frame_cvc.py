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
from gnuradio import gr_unittest
from gnuradio import blocks
import mimoots_swig as mimoots
import random

class qa_ofdm_extract_frame_cvc(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None
        self.data_source = None
        self.trigger_source = None
        self.frames = None
        self.data_sink = None

    def genData(self, nframes, nsymbols, fft_len, cp_len):
        random.seed(42)
        frames = []
        cp = cp_len*[0]

        frames.extend(nsymbols*(fft_len+cp_len)*[0])

        for i in xrange(nsymbols*nframes):
            symbol = cp + [random.randint(0,255) for x in xrange(fft_len)]
            frames.extend(symbol)

        return frames

    def genTrigger(self, nframes, nsymbols, fft_len, cp_len):
        triggers = []
        trigger = (nsymbols*(cp_len+fft_len)-1)*[0]+[1]

        for i in xrange(nframes):
            triggers.extend(trigger)

        triggers.extend(nsymbols*(cp_len+fft_len)*[0])

        return triggers


    def genExpectedData(self, nframes, nsymbols, fft_len):
        random.seed(42)
        frames = []

        for i in xrange(nsymbols*nframes):
            symbol = [random.randint(0,255) for x in xrange(fft_len)]
            frames.extend(symbol)

        return frames

    def test_001_t(self):
        nframes = 15
        nsymbols = 30
        fft_len = 1024
        cp_len = 512

        data = self.genData(nframes, nsymbols, fft_len, cp_len)
        trigger = self.genTrigger(nframes, nsymbols, fft_len, cp_len)
        data_expected = self.genExpectedData(nframes, nsymbols, fft_len)

        self.data_source = blocks.vector_source_c(data=data, vlen=1)
        self.trigger_source = blocks.vector_source_b(data=trigger, vlen=1)

        self.frames = mimoots.ofdm_extract_frame_cvc(
                fft_len=fft_len,
                cp_len=cp_len,
                nsymbols_per_ofdmframe=nsymbols
                )

        self.data_sink = blocks.vector_sink_c(vlen=fft_len)

        self.tb.connect(self.data_source, (self.frames, 0))
        self.tb.connect(self.trigger_source, (self.frames, 1))
        self.tb.connect(self.frames, self.data_sink)

        self.tb.run()

        data_result = self.data_sink.data()

        self.assertComplexTuplesAlmostEqual(
                data_expected,
                data_result,
                nframes*nsymbols*fft_len
                )

    def test_002_t(self):
        nframes = 600
        nsymbols = 5
        fft_len = 20
        cp_len = 3

        data = self.genData(nframes, nsymbols, fft_len, cp_len)
        trigger = self.genTrigger(nframes, nsymbols, fft_len, cp_len)
        data_expected = self.genExpectedData(nframes, nsymbols, fft_len)

        self.data_source = blocks.vector_source_c(data=data, vlen=1)
        self.trigger_source = blocks.vector_source_b(data=trigger, vlen=1)

        self.frames = mimoots.ofdm_extract_frame_cvc(
                fft_len=fft_len,
                cp_len=cp_len,
                nsymbols_per_ofdmframe=nsymbols
                )

        self.data_sink = blocks.vector_sink_c(vlen=fft_len)

        self.tb.connect(self.data_source, (self.frames, 0))
        self.tb.connect(self.trigger_source, (self.frames, 1))
        self.tb.connect(self.frames, self.data_sink)

        self.tb.run()

        data_result = self.data_sink.data()

        self.assertComplexTuplesAlmostEqual(
                data_expected,
                data_result,
                nframes*nsymbols*fft_len
                )

    def test_003_t(self):
        nframes = 600
        nsymbols = 30
        fft_len = 256
        cp_len = 32

        data = self.genData(nframes, nsymbols, fft_len, cp_len)
        trigger = self.genTrigger(nframes, nsymbols, fft_len, cp_len)
        data_expected = self.genExpectedData(nframes, nsymbols, fft_len)

        self.data_source = blocks.vector_source_c(data=data, vlen=1)
        self.trigger_source = blocks.vector_source_b(data=trigger, vlen=1)

        self.frames = mimoots.ofdm_extract_frame_cvc(
                fft_len=fft_len,
                cp_len=cp_len,
                nsymbols_per_ofdmframe=nsymbols
                )

        self.data_sink = blocks.vector_sink_c(vlen=fft_len)

        self.tb.connect(self.data_source, (self.frames, 0))
        self.tb.connect(self.trigger_source, (self.frames, 1))
        self.tb.connect(self.frames, self.data_sink)

        self.tb.run()

        data_result = self.data_sink.data()

        self.assertComplexTuplesAlmostEqual(
                data_expected,
                data_result,
                nframes*nsymbols*fft_len
                )

if __name__ == '__main__':
    gr_unittest.run(qa_ofdm_extract_frame_cvc,
                    "qa_ofdm_extract_frame_cvc.xml")
