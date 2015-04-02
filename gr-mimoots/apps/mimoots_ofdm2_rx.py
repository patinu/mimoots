#!/usr/bin/env python

from gnuradio import gr
from gnuradio import digital
from gnuradio import blocks
import mimoots
from mimoots import utils
import argparse
import random
import itertools

def main():
    args = get_arguments()
    constellation = {
            1:digital.constellation_bpsk(),
            2:digital.constellation_qpsk(),
            3:digital.constellation_8psk(),
    }
    
    occupied_carriers=(range(-26, -21) + range(-20, -7) +
                       range(-6, 0) + range(1, 7) +
                       range(8, 21) + range(22, 27),)
    pilot_carriers=((-21, -7, 7, 21),)
    pilot_symbols=tuple([(1, -1, 1, -1),])
    
    packet_len_tag = "packet_length"
    fft_len = 64
    cp_len = 16
    
    tb = gr.top_block()
    
    if args.freq == None:
        data_source = mimoots.file_source2(
                itemsize=(gr.sizeof_gr_complex, gr.sizeof_gr_complex),
                filename=(
                        '1.'.join(args.from_file.rsplit('.',1)),
                        '2.'.join(args.from_file.rsplit('.',1))
                )
        )
        
    else:
        data_source = mimoots.uhd_source(freq=args.freq, gain=args.gain)
       
    skip0 = blocks.skiphead(
            itemsize=gr.sizeof_gr_complex,
            nitems_to_skip=args.skiphead
    )
    
    skip1 = blocks.skiphead(
            itemsize=gr.sizeof_gr_complex,
            nitems_to_skip=args.skiphead
    )
    
    #ofdm_frames1 = mimoots.ofdm_receive_frames_cb(
    #        nofdm_frames=args.nframes,
    #        nofdm_symbols=args.nsymbols,
    #        constellation=constellation[args.bits],
    #        occupied_carriers=occupied_carriers,
    #        pilot_carriers=pilot_carriers,
    #        pilot_symbols=pilot_symbols,
    #        debug=args.debug
    #)
    
    #ofdm_frames2 = mimoots.ofdm_receive_frames_cb(
    #        nofdm_frames=args.nframes,
    #        nofdm_symbols=args.nsymbols,
    #        constellation=constellation[args.bits],
    #        occupied_carriers=occupied_carriers,
    #        pilot_carriers=pilot_carriers,
    #        pilot_symbols=pilot_symbols,
    #        debug=args.debug
    #)
    
    ofdm_framer0 = mimoots.ofdm_basebandsignal_to_frames_cvc(
            fft_len=fft_len,
            cp_len=cp_len,
            nofdm_symbols=args.nsymbols
    )
    ofdm_framer1 = mimoots.ofdm_basebandsignal_to_frames_cvc(
            fft_len=fft_len,
            cp_len=cp_len,
            nofdm_symbols=args.nsymbols
    )
    
    ofdm_symboler0 = mimoots.ofdm_frame_to_symbols_vcc(
            fft_len=fft_len,
            cp_len=cp_len,
            occupied_carriers=occupied_carriers,
            pilot_carriers=pilot_carriers,
            pilot_symbols=pilot_symbols,
            constellation=constellation[args.bits],
            nofdm_symbols=args.nsymbols,
            packet_len_tag=packet_len_tag
    )
    ofdm_symboler1 = mimoots.ofdm_frame_to_symbols_vcc(
            fft_len=fft_len,
            cp_len=cp_len,
            occupied_carriers=occupied_carriers,
            pilot_carriers=pilot_carriers,
            pilot_symbols=pilot_symbols,
            constellation=constellation[args.bits],
            nofdm_symbols=args.nsymbols,
            packet_len_tag=packet_len_tag
    )
    
    ofdm_demapper0 = mimoots.ofdm_symbol_demapper_cb(
            constellation=constellation[args.bits],
            packet_len_tag=packet_len_tag
    )
    ofdm_demapper1 = mimoots.ofdm_symbol_demapper_cb(
            constellation=constellation[args.bits],
            packet_len_tag=packet_len_tag
    )
    
    data_sink0 = blocks.vector_sink_b()
    data_sink1 = blocks.vector_sink_b()
    
    tb.connect((data_source, 0), skip0, ofdm_framer0, ofdm_symboler0, 
               ofdm_demapper0, data_sink0)
    tb.connect((data_source, 1), skip1, ofdm_framer1, ofdm_symboler1, 
               ofdm_demapper1, data_sink1)
    
    tb.run()
    
    random.seed(42)
    #data_expected = tuple(args.nframes*[random.randint(0,255) for x in xrange(args.bits*60)])
    
    
    data_len = utils.ofdm_get_data_len(
            nofdm_symbols=args.nsymbols,
            noccupied_carriers=len(occupied_carriers[0]),
            constellation=constellation[args.bits]
    )
    
    if args.dummy_frame == True:
        data_expected = [
                tuple(data_len*[0] + args.nframes*[1 for x in xrange(data_len)]),
                tuple(data_len*[0] + args.nframes*[2 for x in xrange(data_len)])
        ]
    else:
        data_expected = [
                tuple(args.nframes*[1 for x in xrange(data_len)]),
                tuple(args.nframes*[2 for x in xrange(data_len)])
        ]
    
    data = [data_sink0.data(), data_sink1.data()] 
    
    len_data = []
    len_data_expected = []
    ignored_correlations = []
    biterrors_complete = []
    biterrorrate_complete = []
    
    for data_index in range(2):
        biterror = 0
        index = 0
        for i,j in itertools.izip_longest(data[data_index], data_expected[data_index]):
            index += 1
            if i != j:
                if i is None or j is None:
                    biterror += 8
                else:
                    #print("Index: {} data: {} expected: {}".format(index, i, j))
                    biterror += bin(i^j).count("1")

        bits = args.bits
    
        len_data = len(data[data_index])
        len_data_expected = len(data_expected[data_index])
        ignored_correlations = (len(data_expected[data_index])-len(data[data_index]))/(args.bits*60)
        biterrors_complete = float(biterror)/float(8*len(data_expected[data_index]))
        biterrorrate_complete = float(biterror)/float(8*len(data_expected[data_index]))
    
        print '{}:len(data): {}'.format(data_index, len_data)
        print '{}:len(data_expected): {}'.format(data_index, len_data_expected)
        print '{}:Correlation didn\'t work: {} times'.format(data_index, ignored_correlations)
        print '{}:biterrors: {} biterrorrate: {}'.format(data_index, biterror, biterrorrate_complete)
        print "\n"
    
def get_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--from-file', default='signal.dat',
                        help='Read complex baseband-signal from file')
    group.add_argument('-f', '--freq', default=None, type=int,
                       nargs='+',
                       help='Uses frequency for signal')
    parser.add_argument('--nframes', default=10, type=int,
                        help='Count of how many ofdm-frames to send')
    parser.add_argument('--nsymbols', default=2, type=int,
                        help='Count of how many ofdm-symbols per frame'
                              ' to send')
    parser.add_argument('--bits', default=1, type=int,
                        help='Count of bits for complex symbols')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, dest='debug',
                        help='Count of bits for complex symbols') 
    parser.add_argument('-d', '--dummy-frame', action='store_true',
                        default=False, dest='dummy_frame',
                        help='Interpretes first OFDM-Frame as dummy')    
    parser.add_argument('--skiphead', default=0, type=int,
                        help='Ignore N samples at beginning of stream')
    parser.add_argument('--gain', default=None, type=int,
                        help='Gain')
    
    return parser.parse_args()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
