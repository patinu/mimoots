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
#include "logcsv_cb_impl.h"

#include <ctime>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>

namespace gr {
  namespace mimoots {

    logcsv_cb::sptr
    logcsv_cb::make(int fft_length, int used_tones)
    {
      return gnuradio::get_initial_sptr
        (new logcsv_cb_impl(fft_length, used_tones));
    }
    
    /*
     * The private constructor
     */
    logcsv_cb_impl::logcsv_cb_impl(int fft_length, int used_tones)
      : gr::block("logcsv_cb",
              gr::io_signature::make(1, 1, sizeof(gr_complex)*fft_length),
              gr::io_signature::make(1, 1, sizeof(gr_complex)*used_tones)),
      d_fft_length(fft_length), d_used_tones(used_tones)
    {
      time_t t = time(0);
      struct tm* now = localtime(&t);
      std::ostringstream filename;
      
      filename << "csvlog_"
               << now->tm_mday
               << std::setw(2) << std::setfill('0')
               << now->tm_mon
               << now->tm_year+1900
               << "_" 
               << now->tm_hour 
               << now->tm_min
               << now->tm_sec
               << ".csv";
      
      d_csvfile.open(filename.str().c_str());
      
      d_fft_tones_start = (d_fft_length-d_used_tones)/2;
      d_fft_tones_end = fft_length - d_fft_tones_start;
    }

    /*
     * Our virtual destructor.
     */
    logcsv_cb_impl::~logcsv_cb_impl()
    {
      d_csvfile.close();
    }
    
    void
    logcsv_cb_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
      //ninput_items_required[1] = noutput_items;
    }

    int
    logcsv_cb_impl::general_work(
      int noutput_items,
      gr_vector_int &ninput_items,
      gr_vector_const_void_star &input_items,
      gr_vector_void_star &output_items)
    {
      //if (ninput_items[0] != ninput_items[1]) {
      //    std::stringstream ss;
      //    ss << "csvlog_cb_impl: length of input 1 and 2 are different! "
      //       << "(" << ninput_items[0] << "," << ninput_items[1] << ")";
      //                         
      //    throw std::invalid_argument(ss.str());
	  //}
      
      const gr_complex *in0 = reinterpret_cast<const gr_complex *>(input_items[0]);
      //const char *flag = reinterpret_cast<const char *>(input_items[1]);

      gr_complex *out = reinterpret_cast<gr_complex *>(output_items[0]);
      
      unsigned int item_consumed=0;
      
      for (unsigned int item_index=0; item_index<ninput_items[0]; item_index++ ) {
        //if (flag[item_index] == 1) {
          std::memcpy(&out[ item_consumed*d_used_tones ],
                      &in0[ item_index*d_fft_length+d_fft_tones_start ],
                      d_used_tones*sizeof(gr_complex));
          item_consumed++;
        //}
      }
      
      consume(0, ninput_items[0]); //consume port 0 input
      //consume(1, ninput_items[1]); //consume port 1 input

      return item_consumed;
    }
    
    int logcsv_cb_impl::fft_tones_start()
    {
      return d_fft_tones_start;
    }
	
	int logcsv_cb_impl::fft_tones_end()
    {
      return d_fft_tones_end;
    }

  } /* namespace mimoots */
} /* namespace gr */

