/* -*- c++ -*- */

#define MIMOOTS_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "mimoots_swig_doc.i"

%{
#include "mimoots/logcsv_cb.h"
#include "mimoots/ofdm_extract_frame_cvc.h"
#include "mimoots/ofdm_scale_symbol_vcvc.h"
%}


%include "mimoots/logcsv_cb.h"
GR_SWIG_BLOCK_MAGIC2(mimoots, logcsv_cb);

%include "mimoots/ofdm_extract_frame_cvc.h"
GR_SWIG_BLOCK_MAGIC2(mimoots, ofdm_extract_frame_cvc);

%include "mimoots/ofdm_scale_symbol_vcvc.h"
GR_SWIG_BLOCK_MAGIC2(mimoots, ofdm_scale_symbol_vcvc);
