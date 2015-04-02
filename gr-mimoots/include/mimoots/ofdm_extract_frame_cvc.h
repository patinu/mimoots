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


#ifndef INCLUDED_MIMOOTS_OFDM_EXTRACT_FRAME_CVC_H
#define INCLUDED_MIMOOTS_OFDM_EXTRACT_FRAME_CVC_H

#include <mimoots/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace mimoots {

    /*!
     * \brief <+description of block+>
     * \ingroup mimoots
     *
     */
    class MIMOOTS_API ofdm_extract_frame_cvc : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<ofdm_extract_frame_cvc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of mimoots::ofdm_extract_frame_cvc.
       *
       * To avoid accidental use of raw pointers, mimoots::ofdm_extract_frame_cvc's
       * constructor is in a private implementation
       * class. mimoots::ofdm_extract_frame_cvc::make is the public interface for
       * creating new instances.
       */
      static sptr make(
        size_t fft_len,
        size_t cp_len, 
        size_t nsymbols_per_ofdmframe,
        bool info=false
      );
      
      // Getter
      virtual size_t fft_len() = 0;
      virtual size_t cp_len() = 0;
      virtual size_t nsymbols_per_ofdmframe() = 0;
      virtual bool info() = 0;
      
      // Setter
      virtual void set_fft_len(size_t) = 0;
      virtual void set_cp_len(size_t) = 0;
      virtual void set_nsymbols_per_ofdmframe(size_t) = 0;
      virtual void set_info(bool) = 0;
    };

  } // namespace mimoots
} // namespace gr

#endif /* INCLUDED_MIMOOTS_OFDM_EXTRACT_FRAME_CVC_H */

