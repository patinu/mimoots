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

#ifndef INCLUDED_MIMOOTS_LOGCSV_CB_IMPL_H
#define INCLUDED_MIMOOTS_LOGCSV_CB_IMPL_H

#include <mimoots/logcsv_cb.h>

#include <fstream>

namespace gr {
  namespace mimoots {

    class logcsv_cb_impl : public logcsv_cb
    {
     private:
      std::ofstream d_csvfile;
      int d_fft_length;
      int d_used_tones;
      int d_fft_tones_start;
      int d_fft_tones_end;

     public:
      logcsv_cb_impl(int fft_length, int used_tones);
      ~logcsv_cb_impl();
      
      void set_csvline(std::string csvline);
      std::string csvline();
      
      void set_fft_length(int fft_length);
      int fft_length();
      
      void set_used_tones(int used_tones);
      int used_tones();
      
      void set_fft_tones_start(int fft_tones_start);
      int fft_tones_start();
      
      void set_fft_tones_end(int fft_tones_end);
      int fft_tones_end();
      
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items);
    };

  } // namespace mimoots
} // namespace gr

#endif /* INCLUDED_MIMOOTS_LOGCSV_CB_IMPL_H */

