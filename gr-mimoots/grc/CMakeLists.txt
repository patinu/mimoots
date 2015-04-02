# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
install(FILES
    mimoots_logcsv_cb.xml
    mimoots_ofdm_extract_frame_cvc.xml
    mimoots_ofdm_scale_symbol_vcvc.xml
    mimoots_ofdm_create_frames_bc.xml
    mimoots_ofdm_receive_frames_cb.xml
    mimoots_uhd_sink.xml
    mimoots_uhd_source.xml
    mimoots_uhd_sink2.xml
    mimoots_uhd_source2.xml
    mimoots_ofdm_symbol_mapper_bc.xml
    mimoots_ofdm_symbols_to_frame_cc.xml
    mimoots_ofdm_symbol_demapper_cb.xml
    mimoots_ofdm_basebandsignal_to_frames_cvc.xml
    mimoots_ofdm_frame_to_symbols_vcc.xml
    mimoots_ofdm_frames_to_basebandsignal_vcc.xml
    mimoots_ofdm_symbols_to_frame_cvc.xml
    mimoots_file_sink2.xml
    mimoots_file_source2.xml DESTINATION share/gnuradio/grc/blocks
)
