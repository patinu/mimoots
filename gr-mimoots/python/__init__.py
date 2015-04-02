#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio MIMOOTS module. Place your Python package
description here (python/__init__.py).
'''

# ----------------------------------------------------------------
# Temporary workaround for ticket:181 (swig+python problem)
import sys
_RTLD_GLOBAL = 0
try:
    from dl import RTLD_GLOBAL as _RTLD_GLOBAL
except ImportError:
    try:
	from DLFCN import RTLD_GLOBAL as _RTLD_GLOBAL
    except ImportError:
	pass

if _RTLD_GLOBAL != 0:
    _dlopenflags = sys.getdlopenflags()
    sys.setdlopenflags(_dlopenflags|_RTLD_GLOBAL)
# ----------------------------------------------------------------


# import swig generated symbols into the mimoots namespace
try:
	# this might fail if the module is python-only
	from mimoots_swig import *
except ImportError:
	pass

# import any pure python here
from utils import utils
from ofdm_create_frames_bc import ofdm_create_frames_bc
from ofdm_receive_frames_cb import ofdm_receive_frames_cb
from uhd_sink import uhd_sink
from uhd_source import uhd_source
from uhd_sink2 import uhd_sink2
from uhd_source2 import uhd_source2
from ofdm_symbol_mapper_bc import ofdm_symbol_mapper_bc
from ofdm_symbols_to_frame_cc import ofdm_symbols_to_frame_cc


from ofdm_symbol_demapper_cb import ofdm_symbol_demapper_cb
from ofdm_basebandsignal_to_frames_cvc import ofdm_basebandsignal_to_frames_cvc
from ofdm_frame_to_symbols_vcc import ofdm_frame_to_symbols_vcc
from ofdm_frames_to_basebandsignal_vcc import ofdm_frames_to_basebandsignal_vcc
from ofdm_symbols_to_frame_cvc import ofdm_symbols_to_frame_cvc
from file_sink2 import file_sink2
from file_source2 import file_source2



#

# ----------------------------------------------------------------
# Tail of workaround
if _RTLD_GLOBAL != 0:
    sys.setdlopenflags(_dlopenflags)      # Restore original flags
# ----------------------------------------------------------------
