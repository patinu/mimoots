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


#ifndef INCLUDED_MIMOOTS_OFDM_SCALE_SYMBOL_VCVC_H
#define INCLUDED_MIMOOTS_OFDM_SCALE_SYMBOL_VCVC_H

#include <mimoots/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace mimoots {

    /*!
     * \brief   Takes an OFDM-Symbol and divides every value by the maximum 
     *           value in this OFDM-Symbol that every value has an absolute 
     *           smaller or equal than 1.
     * \ingroup mimoots
     * \details The input is a vector with the size of fft_len. It should be an
     *           OFDM-Symbol. To keep every absolute value of all complex values
     *           lower or equal than 1, the block searches for the value with
     *           the largest absolute and devides every value by it.
     *           It is possible to scale all normalized values with a parameter
     *           called scale.
     *           The output is a normalized vector with the length of fft_len.
     */
    class MIMOOTS_API ofdm_scale_symbol_vcvc : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<ofdm_scale_symbol_vcvc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of mimoots::ofdm_scale_symbol_vcvc.
       *
       * To avoid accidental use of raw pointers, mimoots::ofdm_scale_symbol_vcvc's
       * constructor is in a private implementation
       * class. mimoots::ofdm_scale_symbol_vcvc::make is the public interface for
       * creating new instances.
       */
      static sptr make(size_t symbol_len, float scale=1);
    };

  } // namespace mimoots
} // namespace gr

#endif /* INCLUDED_MIMOOTS_OFDM_SCALE_SYMBOL_VCVC_H */

