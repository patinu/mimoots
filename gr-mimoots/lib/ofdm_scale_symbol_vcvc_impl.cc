/* -*- c++ -*- */
/* 
 * Copyright 2014 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "ofdm_scale_symbol_vcvc_impl.h"

namespace gr {
  namespace mimoots {

    ofdm_scale_symbol_vcvc::sptr
    ofdm_scale_symbol_vcvc::make(size_t symbol_len, float scale)
    {
      return gnuradio::get_initial_sptr
        (new ofdm_scale_symbol_vcvc_impl(symbol_len, scale));
    }

    /*
     * The private constructor
     */
    ofdm_scale_symbol_vcvc_impl::ofdm_scale_symbol_vcvc_impl(size_t symbol_len, float scale)
      : gr::sync_block("ofdm_scale_symbol_vcvc",
              gr::io_signature::make(1, 1, symbol_len*sizeof(gr_complex)),
              gr::io_signature::make(1, 1, symbol_len*sizeof(gr_complex))),
      d_symbol_len(symbol_len),
      d_scale(scale)
    {}

    /*
     * Our virtual destructor.
     */
    ofdm_scale_symbol_vcvc_impl::~ofdm_scale_symbol_vcvc_impl()
    {
    }

    int
    ofdm_scale_symbol_vcvc_impl::work(int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items)
    {
      const gr_complex *frame = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];
      
      float max_abs = 1;
      float abs = 1;
      float factor = 1;
      for (size_t frame_index = 0; frame_index < noutput_items; frame_index++) {
        max_abs = std::abs(frame[ frame_index*d_symbol_len ]);
        
        // Find max value in frame
        for (size_t value_index=1; value_index<d_symbol_len; value_index++) {
          abs = std::abs(frame[ frame_index*d_symbol_len + value_index ]);
          if (abs > max_abs) {
            max_abs = abs;
          }
        }
        
        if (max_abs < 1) {
          max_abs = 1;
        }
        
        factor = max_abs/d_scale;

        for (size_t value_index= 0 ; value_index < d_symbol_len; value_index++) {
          out[ frame_index*d_symbol_len + value_index ] = 
              frame[ frame_index*d_symbol_len + value_index ];
          
          out[ frame_index*d_symbol_len + value_index ] /= factor;
        }
      }
        
      return noutput_items;
    }

  } /* namespace mimoots */
} /* namespace gr */

