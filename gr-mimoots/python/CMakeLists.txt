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

########################################################################
# Include python install macros
########################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

########################################################################
# Install python sources
########################################################################
GR_PYTHON_INSTALL(
    FILES
    __init__.py
    ofdm_create_frames_bc.py
    utils.py
    ofdm_receive_frames_cb.py
    uhd_sink.py
    uhd_source.py
    uhd_sink2.py
    uhd_source2.py
    ofdm_symbol_mapper_bc.py
    ofdm_symbols_to_frame_cc.py
    ofdm_symbol_demapper_cb.py
    ofdm_basebandsignal_to_frames_cvc.py
    ofdm_frame_to_symbols_vcc.py
    ofdm_frames_to_basebandsignal_vcc.py
    ofdm_symbols_to_frame_cvc.py
    file_sink2.py
    file_source2.py DESTINATION ${GR_PYTHON_DIR}/mimoots
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-mimoots)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)
GR_ADD_TEST(qa_logcsv_cb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_logcsv_cb.py)
GR_ADD_TEST(qa_ofdm_extract_frame_cvc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_extract_frame_cvc.py)
GR_ADD_TEST(qa_ofdm_scale_symbol_vcvc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_scale_symbol_vcvc.py)
GR_ADD_TEST(qa_ofdm_create_frames_bc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_create_frames_bc.py)
GR_ADD_TEST(qa_ofdm_receive_frames_cb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_receive_frames_cb.py)
GR_ADD_TEST(qa_uhd_sink ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_uhd_sink.py)
GR_ADD_TEST(qa_uhd_source ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_uhd_source.py)
GR_ADD_TEST(qa_uhd_sink2 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_uhd_sink2.py)
GR_ADD_TEST(qa_uhd_source2 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_uhd_source2.py)
GR_ADD_TEST(qa_ofdm_symbol_mapper_bc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_symbol_mapper_bc.py)
GR_ADD_TEST(qa_ofdm_symbols_to_frame_cc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_symbols_to_frame_cc.py)
GR_ADD_TEST(qa_ofdm_symbol_demapper_cb ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_symbol_demapper_cb.py)
GR_ADD_TEST(qa_ofdm_basebandsignal_to_frames_cvc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_basebandsignal_to_frames_cvc.py)
GR_ADD_TEST(qa_ofdm_frame_to_symbols_vcc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_frame_to_symbols_vcc.py)
GR_ADD_TEST(qa_ofdm_frames_to_basebandsignal_vcc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_frames_to_basebandsignal_vcc.py)
GR_ADD_TEST(qa_ofdm_symbols_to_frame_cvc ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_ofdm_symbols_to_frame_cvc.py)
GR_ADD_TEST(qa_file_sink2 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_file_sink2.py)
GR_ADD_TEST(qa_file_source2 ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_file_source2.py)
