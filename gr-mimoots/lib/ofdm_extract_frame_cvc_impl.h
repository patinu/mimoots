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

#ifndef INCLUDED_MIMOOTS_OFDM_EXTRACT_FRAME_CVC_IMPL_H
#define INCLUDED_MIMOOTS_OFDM_EXTRACT_FRAME_CVC_IMPL_H

#include <mimoots/ofdm_extract_frame_cvc.h>

namespace gr {
  namespace mimoots {

    enum state_t {
        STATE_FIND_TRIGGER,
        STATE_SYMBOL
    };

    class ofdm_extract_frame_cvc_impl : public ofdm_extract_frame_cvc
    {
     private:
      size_t d_fft_len;
      size_t d_cp_len;
      size_t d_nsymbols_per_ofdmframe;
      size_t d_current_symbol;
      enum state_t d_state;
      bool d_info;

     public:
      ofdm_extract_frame_cvc_impl(
        size_t fft_len,
        size_t cp_len,
        size_t nsymbols_per_ofdmframe,
        bool info);
      ~ofdm_extract_frame_cvc_impl();

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
        gr_vector_int &ninput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items);

      // Getter
      size_t fft_len();
      size_t cp_len();
      size_t nsymbols_per_ofdmframe();
      bool info();

      // Setter
      void set_fft_len(size_t);
      void set_cp_len(size_t);
      void set_nsymbols_per_ofdmframe(size_t);
      void set_info(bool);
    };

  } // namespace mimoots
} // namespace gr

#endif /* INCLUDED_MIMOOTS_OFDM_EXTRACT_FRAME_CVC_IMPL_H */

