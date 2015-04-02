#!/usr/bin/env python

from gnuradio import gr
from gnuradio import digital
from gnuradio import blocks
from gnuradio.gr import packet_utils
import mimoots
from mimoots import utils
import argparse
import time

def main():
    args = get_arguments()
    constellation = {
            1:digital.constellation_bpsk(),
            2:digital.constellation_qpsk(),
            3:digital.constellation_8psk(),
    }
    
    packet_len_tag = "packet_length"
    fft_len = 64
    cp_len = 16
    
    occupied_carriers=(range(-26, -21) + range(-20, -7) +
                       range(-6, 0) + range(1, 7) +
                       range(8, 21) + range(22, 27),)
    pilot_carriers=((-21, -7, 7, 21),)
    pilot_symbols=tuple([(1, -1, 1, -1),])
    
    data_len = utils.ofdm_get_data_len(
            nofdm_symbols=args.nsymbols,
            noccupied_carriers=len(occupied_carriers[0]),
            constellation=constellation[args.bits]
    )
    
    data = args.nframes*[[1 for x in xrange(data_len)],]
    
    tb = gr.top_block()

    (data_tosend, tags) = packet_utils.packets_to_vectors(
            data,
            packet_len_tag
    )

    data_source = blocks.vector_source_b(
            data=data_tosend,
            vlen=1,
            tags=tags,
            repeat=False
    )

    ofdm_mapper = mimoots.ofdm_symbol_mapper_bc(
            constellation=constellation[args.bits],
            packet_len_tag=packet_len_tag
    )
    
    ofdm_framer = mimoots.ofdm_symbols_to_frame_cvc(
            fft_len=fft_len,
            cp_len=cp_len,
            occupied_carriers=occupied_carriers,
            pilot_carriers=pilot_carriers,
            pilot_symbols=pilot_symbols,
            packet_len_tag=packet_len_tag
    )
    
    ofdm_basebander = mimoots.ofdm_frames_to_basebandsignal_vcc(
            fft_len=fft_len,
            cp_len=cp_len,
            packet_len_tag=packet_len_tag
    )
    
    shifter = blocks.delay(
            itemsize=gr.sizeof_gr_complex,
            delay=(fft_len+cp_len)*(3)
    )
    
    xor_source = blocks.vector_source_c(
            data=5*[0]+(3*(fft_len+cp_len)-10)*[1]+5*[0]+3*(fft_len+cp_len)*[0],
            repeat=True
    )
    
    xor1 = blocks.multiply_cc()
    xor2 = blocks.multiply_cc()
    
    if args.freq == None:
        data_sink = mimoots.file_sink2(
                itemsize=(gr.sizeof_gr_complex, gr.sizeof_gr_complex),
                filename=(
                        '1.'.join(args.to_file.rsplit('.',1)),
                        '2.'.join(args.to_file.rsplit('.',1))
                )
        )

    else:
        data_sink = mimoots.uhd_sink2(freq=args.freq, gain=args.gain)
    
    
    tb.connect(xor_source, (xor1, 1))
    tb.connect(xor_source, (xor2, 1))
    tb.connect(data_source, ofdm_mapper, ofdm_framer, ofdm_basebander)
    tb.connect(ofdm_basebander, (xor1, 0), (data_sink, 0))
    tb.connect(ofdm_basebander, (xor2, 0), shifter, (data_sink, 1))

    tb.run()

    time.sleep(5)

def get_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--to-file', default='signal.dat',
                        help='Read complex baseband-signal from file')
    group.add_argument('-f', '--freq', default=None, type=int,
                        help='Uses frequency for signal')
    parser.add_argument('--nframes', default=10, type=int,
                        help='Count of how many ofdm-frames to send')
    parser.add_argument('--nsymbols', default=1, type=int,
                        help='Count of how many ofdm-symbols per frame'
                              ' to send')
    parser.add_argument('--bits', default=1, type=int,
                        help='Count of bits for complex symbols')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, dest='debug',
                        help='Count of bits for complex symbols')
    parser.add_argument('--gain', default=None, type=int,
                        help='Gain')
    parser.add_argument('--scale', default=1.0, type=float,
                        help='Scale signal (0.00 - 1.00)')

    return parser.parse_args()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
