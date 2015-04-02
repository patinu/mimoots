#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/zwobot/projects/mimoots/gr-mimoots/python
export PATH=/home/zwobot/projects/mimoots/gr-mimoots/build/python:$PATH
export LD_LIBRARY_PATH=/home/zwobot/projects/mimoots/gr-mimoots/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/zwobot/projects/mimoots/gr-mimoots/build/swig:$PYTHONPATH
/usr/bin/python2 /home/zwobot/projects/mimoots/gr-mimoots/python/qa_ofdm_extract_frame_cvc.py 
