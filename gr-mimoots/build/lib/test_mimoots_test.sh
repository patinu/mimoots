#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/zwobot/projects/mimoots/gr-mimoots/lib
export PATH=/home/zwobot/projects/mimoots/gr-mimoots/build/lib:$PATH
export LD_LIBRARY_PATH=/home/zwobot/projects/mimoots/gr-mimoots/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-mimoots 
