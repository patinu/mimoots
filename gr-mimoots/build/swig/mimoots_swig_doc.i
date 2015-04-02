
/*
 * This file was automatically generated using swig_doc.py.
 *
 * Any changes to it will be lost next time it is regenerated.
 */




%feature("docstring") gr::mimoots::logcsv_cb "<+description of block+>"

%feature("docstring") gr::mimoots::logcsv_cb::make "Return a shared_ptr to a new instance of mimoots::logcsv_cb.

To avoid accidental use of raw pointers, mimoots::logcsv_cb's constructor is in a private implementation class. mimoots::logcsv_cb::make is the public interface for creating new instances.

Params: (fft_length, used_tones)"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc "<+description of block+>"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::make "Return a shared_ptr to a new instance of mimoots::ofdm_extract_frame_cvc.

To avoid accidental use of raw pointers, mimoots::ofdm_extract_frame_cvc's constructor is in a private implementation class. mimoots::ofdm_extract_frame_cvc::make is the public interface for creating new instances.

Params: (fft_len, cp_len, nsymbols_per_ofdmframe, info)"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::fft_len "

Params: (NONE)"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::cp_len "

Params: (NONE)"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::nsymbols_per_ofdmframe "

Params: (NONE)"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::info "

Params: (NONE)"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::set_fft_len "

Params: ()"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::set_cp_len "

Params: ()"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::set_nsymbols_per_ofdmframe "

Params: ()"

%feature("docstring") gr::mimoots::ofdm_extract_frame_cvc::set_info "

Params: ()"

%feature("docstring") gr::mimoots::ofdm_scale_symbol_vcvc "Takes an OFDM-Symbol and divides every value by the maximum value in this OFDM-Symbol that every value has an absolute smaller or equal than 1.

The input is a vector with the size of fft_len. It should be an OFDM-Symbol. To keep every absolute value of all complex values lower or equal than 1, the block searches for the value with the largest absolute and devides every value by it. It is possible to scale all normalized values with a parameter called scale. The output is a normalized vector with the length of fft_len."

%feature("docstring") gr::mimoots::ofdm_scale_symbol_vcvc::make "Return a shared_ptr to a new instance of mimoots::ofdm_scale_symbol_vcvc.

To avoid accidental use of raw pointers, mimoots::ofdm_scale_symbol_vcvc's constructor is in a private implementation class. mimoots::ofdm_scale_symbol_vcvc::make is the public interface for creating new instances.

Params: (symbol_len, scale)"