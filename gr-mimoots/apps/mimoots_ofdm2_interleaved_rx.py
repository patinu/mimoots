#!/usr/bin/env python

from gnuradio import gr
from gnuradio import digital
from gnuradio import blocks
from gnuradio.gr import packet_utils
import mimoots
from mimoots import utils
import argparse
import time

def extract_channeldata(l, c, length):
    buf = zip(*[iter(l)]*length*6)
    r = list()
    for dframe in buf:
        r.extend(dframe[c*3*length:(c+1)*3*length])
        
    return r
    

def main():
    args = get_arguments()
    constellation = {
            1:digital.constellation_bpsk(),
            2:digital.constellation_qpsk(),
            3:digital.constellation_8psk(),
    }
    
    fft_len = 64
    cp_len = 16
    
    occupied_carriers=(range(-26, -21) + range(-20, -7) +
                       range(-6, 0) + range(1, 7) +
                       range(8, 21) + range(22, 27),)
    pilot_carriers=((-21, -7, 7, 21),)
    pilot_symbols=tuple([(1, -1, 1, -1),])

    tb1 = gr.top_block()
    tb2 = gr.top_block()
    
    if args.freq == None:
        data_source = mimoots.file_source2(
                itemsize=(gr.sizeof_gr_complex, gr.sizeof_gr_complex),
                filename=(
                        '1.'.join(args.from_file.rsplit('.',1)),
                        '2.'.join(args.from_file.rsplit('.',1))
                )
        )
    else:
        data_source = mimoots.uhd_source2(freq=args.freq, gain=args.gain)

    skip1 = blocks.skiphead(
            itemsize=gr.sizeof_gr_complex,
            nitems_to_skip=args.skiphead
    )
    
    skip2 = blocks.skiphead(
            itemsize=gr.sizeof_gr_complex,
            nitems_to_skip=args.skiphead
    )
    
    ofdm_frames1 = mimoots.ofdm_basebandsignal_to_frames_cvc(
            fft_len=fft_len,
            cp_len=cp_len,
            nofdm_symbols=args.nsymbols
    )
    
    ofdm_frames2 = mimoots.ofdm_basebandsignal_to_frames_cvc(
            fft_len=fft_len,
            cp_len=cp_len,
            nofdm_symbols=args.nsymbols
    )
    
    buffer1 = blocks.vector_sink_c(vlen=fft_len)
    buffer2 = blocks.vector_sink_c(vlen=fft_len)
    
    tb1.connect((data_source,0), skip1, ofdm_frames1, buffer1)
    tb1.connect((data_source,1), skip2, ofdm_frames2, buffer2)

    tb1.connect(ofdm_frames1, blocks.file_sink(gr.sizeof_gr_complex*fft_len, 'd1.gr'))
    tb1.connect(ofdm_frames2, blocks.file_sink(gr.sizeof_gr_complex*fft_len, 'd2.gr'))

    tb1.run()
    
    data1 = buffer1.data()
    data2 = buffer2.data()
    
    data1 = extract_channeldata(data1, 0, fft_len)
    data2 = extract_channeldata(data2, 1, fft_len)
    
    buf_source1 = blocks.vector_source_c(data1)
    buf_source2 = blocks.vector_source_c(data2)
    
    data_sink = mimoots.file_sink2(
            itemsize=(gr.sizeof_gr_complex, gr.sizeof_gr_complex),
            filename=('s1r1.gr', 's2r2.gr')
    )
    
    tb2.connect(buf_source1, (data_sink, 0))
    tb2.connect(buf_source2, (data_sink, 1))
    
    tb2.run()
    
def get_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--from-file', default='signal.dat',
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
    parser.add_argument('--skiphead', default=0, type=int,
                        help='Ignore N samples at beginning of stream')

    return parser.parse_args()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
