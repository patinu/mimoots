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
#include "ofdm_extract_frame_cvc_impl.h"

#include <assert.h>

namespace gr {
  namespace mimoots {

    ofdm_extract_frame_cvc::sptr
    ofdm_extract_frame_cvc::make(
      size_t fft_len,
      size_t cp_len,
      size_t nsymbols_per_ofdmframe,
      bool info
    )
    {
      return gnuradio::get_initial_sptr
        (new ofdm_extract_frame_cvc_impl(
                fft_len, cp_len, nsymbols_per_ofdmframe, info
              ));
    }

    /*
     * The private constructor
     */
    ofdm_extract_frame_cvc_impl::ofdm_extract_frame_cvc_impl(
      size_t fft_len,
      size_t cp_len,
      size_t nsymbols_per_ofdmframe,
      bool info
    )
      : gr::block("ofdm_extract_frame_cvc",
          gr::io_signature::make2(2, 2, sizeof(gr_complex), sizeof(char)),
          gr::io_signature::make(1, 1, fft_len*sizeof(gr_complex))
      ),
      d_fft_len(fft_len),
      d_cp_len(cp_len),
      d_nsymbols_per_ofdmframe(nsymbols_per_ofdmframe),
      d_current_symbol(0),
      d_state(STATE_FIND_TRIGGER),
      d_info(info)
    {
    }

    /*
     * Our virtual destructor.
     */
    ofdm_extract_frame_cvc_impl::~ofdm_extract_frame_cvc_impl()
    {
    }

    void
    ofdm_extract_frame_cvc_impl::forecast(
      int noutput_items, 
      gr_vector_int &ninput_items_required
    )
    {
      size_t items_required = 1; // Is there a good init-value to avoid hidden bugs?
      size_t ofdmsymbol_len = d_fft_len + d_cp_len;
        
      switch(d_state) {
      case STATE_FIND_TRIGGER: {
        items_required = ofdmsymbol_len;
        break;
      }
      case STATE_SYMBOL: {
        items_required = ofdmsymbol_len;
        break;
      }
      default: {
        throw std::runtime_error("invalid state");
        break;
      }
      }
        
      size_t ninputs = ninput_items_required.size();
      for (size_t inputs_index = 0; inputs_index < ninputs; inputs_index++) {
        ninput_items_required[inputs_index] = items_required;
      }
      
      return;
    }

    int
    ofdm_extract_frame_cvc_impl::general_work(
      int noutput_items,
      gr_vector_int &ninput_items,
      gr_vector_const_void_star &input_items,
      gr_vector_void_star &output_items
    )
    {
      const gr_complex *data = (const gr_complex *) input_items[0];
      const char *flags = (const char *) input_items[1];
      gr_complex *out = (gr_complex *) output_items[0];

      size_t nitem_consumed = 0;
      size_t nitem_ret = 0;
      
      switch(d_state) {
      case STATE_FIND_TRIGGER: {
        size_t nitems = std::min(
          std::min(ninput_items[0], ninput_items[1]),
          noutput_items
        );
          
        nitem_consumed = nitems;
        nitem_ret=0;
          
        for (size_t item_index = 0; item_index < nitems; item_index++) {
          if (flags[item_index] == 1) {
            nitem_consumed=item_index+1;

            d_state=STATE_SYMBOL;
            break;
          }
        }
          
        break;
      }
      case STATE_SYMBOL: {
        std::memcpy(out, &data[d_cp_len], d_fft_len*sizeof(gr_complex));
          
        if (d_current_symbol < d_nsymbols_per_ofdmframe-1) {
          d_current_symbol++;
            
          nitem_consumed = (d_fft_len+d_cp_len);
          nitem_ret = 1;
        } else {
          d_current_symbol = 0;
          d_state = STATE_FIND_TRIGGER;
            
          nitem_consumed = 0;
          nitem_ret = 1;
        }

        break;
      }
      }

      consume_each(nitem_consumed);
      return nitem_ret;
    }
    
    //------------------------------------------------------------------------
    // Getter
    //------------------------------------------------------------------------
    size_t
    ofdm_extract_frame_cvc_impl::fft_len()
    {
      return d_fft_len;
    }
    
    size_t
    ofdm_extract_frame_cvc_impl::cp_len()
    {
      return d_cp_len;
    }
    
    size_t
    ofdm_extract_frame_cvc_impl::nsymbols_per_ofdmframe()
    {
      return d_nsymbols_per_ofdmframe;
    }
    
    bool
    ofdm_extract_frame_cvc_impl::info()
    {
      return d_info;
    }
    
    //------------------------------------------------------------------------
    // Setter
    //------------------------------------------------------------------------
    void
    ofdm_extract_frame_cvc_impl::set_fft_len(size_t fft_len)
    {
      d_fft_len = fft_len;
    }
    
    void
    ofdm_extract_frame_cvc_impl::set_cp_len(size_t cp_len)
    {
      d_cp_len = cp_len;
    }
    
    void
    ofdm_extract_frame_cvc_impl::set_nsymbols_per_ofdmframe(size_t nsymbols)
    {
      d_nsymbols_per_ofdmframe = nsymbols;
    }
    
    void
    ofdm_extract_frame_cvc_impl::set_info(bool info)
    {
      d_info = info;
    }
  } /* namespace mimoots */
} /* namespace gr */

