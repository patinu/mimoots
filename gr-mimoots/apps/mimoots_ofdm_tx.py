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
    #self.data = ( [[random.randint(0,255) for x in xrange(self.data_len)]
    #              +50*[0,],] )
    #self.data = [[0 for x in xrange(self.data_len)],] \
    #            + self.nofdm_frames*[[random.randint(0,255) \
    #            for x in xrange(self.data_len)],]
    #self.data = self.nofdm_frames*[[x for x in xrange(self.data_len)],]\
    #            + [50*[0,],]


    args = get_arguments()
    constellation = {
            1:digital.constellation_bpsk(),
            2:digital.constellation_qpsk(),
            3:digital.constellation_8psk(),
    }

    packet_len_tag = "packet_length"
    #fft_len = 64
    #cp_len = 16

    #occupied_carriers = (range(-26, -21) + range(-20, -7) +
    #                     range(-6, 0) + range(1, 7) +
    #                     range(8, 21) + range(22, 27),)
    #pilot_carriers = ((-21, -7, 7, 21),)
    #pilot_symbols = tuple([(1, -1, 1, -1),])
    
    fft_len = 16
    cp_len = 4

    occupied_carriers = ((-5, -4, -2, -1, 1, 2, 4, 5),)
    pilot_carriers = ((-3, 3),)
    pilot_symbols = tuple([(1, -1),])

    data_len = utils.ofdm_get_data_len(
            nofdm_symbols=args.nsymbols,
            noccupied_carriers=len(occupied_carriers[0]),
            constellation=constellation[args.bits]
    )

    data = args.nframes*[[39 for x in xrange(data_len)],]

    # sometimes Schmidl-Cox-Correlator ignores first frame
    # so a dummy-frame is a good idea
    if args.dummy_frame_start == True:
        data.insert(0, data_len*[0])

    # if file-output GNURadio needs extra frame at the and to loop over all
    # OFDM-Frames before, last OFDM-Frame is ignored
    # not so in case of using UHD-devices because there exists incoming
    # input-data all the time
    if args.dummy_frame_end == True:
        data.append(data_len*[0])


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
            packet_len_tag=packet_len_tag,
            verbose=args.verbose
    )

    ofdm_framer = mimoots.ofdm_symbols_to_frame_cvc(
            fft_len=fft_len,
            cp_len=cp_len,
            occupied_carriers=occupied_carriers,
            pilot_carriers=pilot_carriers,
            pilot_symbols=pilot_symbols,
            packet_len_tag=packet_len_tag,
            verbose=args.verbose
    )

    ofdm_basebander = mimoots.ofdm_frames_to_basebandsignal_vcc(
            fft_len=fft_len,
            cp_len=cp_len,
            packet_len_tag=packet_len_tag,
            verbose=args.verbose
    )

    if args.freq == None:
        data_sink = blocks.file_sink(
                itemsize=gr.sizeof_gr_complex,
                filename=args.to_file
        )

    else:
        data_sink = mimoots.uhd_sink(freq=args.freq, gain=args.gain)

    tb.connect(data_source, ofdm_mapper, ofdm_framer, ofdm_basebander,
               data_sink)

    tb.run()

    # need to wait until the GNURadio-graph is finished
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
    parser.add_argument('--nsymbols', default=2, type=int,
                        help='Count of how many ofdm-symbols per frame'
                              ' to send')
    parser.add_argument('--bits', default=1, type=int,
                        help='Count of bits for complex symbols')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, dest='verbose',
                        help='Count of bits for complex symbols')
    parser.add_argument('--dummy-frame-start', action='store_true',
                        default=False, dest='dummy_frame_start',
                        help='Makes an OFDM-Frame as dummy in front'
                             ' of all OFDM-Frames')
    parser.add_argument('--dummy-frame-end', action='store_true',
                        default=False, dest='dummy_frame_end',
                        help='Makes an OFDM-Frame as dummy behind'
                             ' all OFDM-Frames')
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
