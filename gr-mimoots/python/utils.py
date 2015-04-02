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
import numpy

class utils():
    def __init__(self):
        pass
        
    @staticmethod
    def ofdm_get_active_carriers(fft_len, occupied_carriers, pilot_carriers):
        """ Returns a list of all carriers that at some point carry data or pilots. """
        active_carriers = list()
        for carrier in list(occupied_carriers[0]) + list(pilot_carriers[0]):
            if carrier < 0:
                carrier += fft_len
            active_carriers.append(carrier)
        return active_carriers
    
    @staticmethod    
    def ofdm_make_sync_word1(fft_len, occupied_carriers, pilot_carriers):
        """ Creates a random sync sequence for fine frequency offset and timing
        estimation. This is the first of typically two sync preamble symbols
        for the Schmidl & Cox sync algorithm.
        The relevant feature of this symbols is that every second sub-carrier
        is zero. In the time domain, this results in two identical halves of
        the OFDM symbols.
        Symbols are always BPSK symbols. Carriers are scaled by sqrt(2) to keep
        total energy constant.
        Carrier 0 (DC carrier) is always zero. If used, carrier 1 is non-zero.
        This means the sync algorithm has to check on odd carriers!
        """
        active_carriers = utils.ofdm_get_active_carriers(fft_len, occupied_carriers, pilot_carriers)
        numpy.random.seed(42)
        bpsk = {0: numpy.sqrt(2), 1: -numpy.sqrt(2)}
        sw1 = [bpsk[numpy.random.randint(2)]  if x in active_carriers and x % 2 else 0 for x in range(fft_len)]
        return numpy.fft.fftshift(sw1)
    
    @staticmethod
    def ofdm_make_sync_word2(fft_len, occupied_carriers, pilot_carriers):
        """ Creates a random sync sequence for coarse frequency offset and channel
        estimation. This is the second of typically two sync preamble symbols
        for the Schmidl & Cox sync algorithm.
        Symbols are always BPSK symbols.
        """
        active_carriers = utils.ofdm_get_active_carriers(fft_len, occupied_carriers, pilot_carriers)
        numpy.random.seed(42)
        bpsk = {0: 1, 1: -1}
        sw2 = [bpsk[numpy.random.randint(2)] if x in active_carriers else 0 for x in range(fft_len)]
        sw2[0] = 0j
        return numpy.fft.fftshift(sw2)
    
    @staticmethod    
    def ofdm_get_data_len(nofdm_symbols, noccupied_carriers, constellation):
        return int(round( (
            nofdm_symbols*
            noccupied_carriers*
            constellation.bits_per_symbol() )/
            (8) ))

if __name__ == '__main__':
    try:
        pass
    except KeyboardInterrupt:
        pass
