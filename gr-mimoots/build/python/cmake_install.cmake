# Install script for directory: /home/zwobot/projects/mimoots/gr-mimoots/python

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/home/zwobot/gnuradio_3.7.5")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "Release")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/mimoots" TYPE FILE FILES
    "/home/zwobot/projects/mimoots/gr-mimoots/python/__init__.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_create_frames_bc.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/utils.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_receive_frames_cb.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/uhd_sink.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/uhd_source.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/uhd_sink2.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/uhd_source2.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_symbol_mapper_bc.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_symbols_to_frame_cc.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_symbol_demapper_cb.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_basebandsignal_to_frames_cvc.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_frame_to_symbols_vcc.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_frames_to_basebandsignal_vcc.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/ofdm_symbols_to_frame_cvc.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/file_sink2.py"
    "/home/zwobot/projects/mimoots/gr-mimoots/python/file_source2.py"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages/mimoots" TYPE FILE FILES
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/__init__.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_create_frames_bc.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/utils.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_receive_frames_cb.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_sink.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_source.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_sink2.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_source2.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbol_mapper_bc.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbols_to_frame_cc.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbol_demapper_cb.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_basebandsignal_to_frames_cvc.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_frame_to_symbols_vcc.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_frames_to_basebandsignal_vcc.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbols_to_frame_cvc.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/file_sink2.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/file_source2.pyc"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/__init__.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_create_frames_bc.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/utils.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_receive_frames_cb.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_sink.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_source.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_sink2.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/uhd_source2.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbol_mapper_bc.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbols_to_frame_cc.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbol_demapper_cb.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_basebandsignal_to_frames_cvc.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_frame_to_symbols_vcc.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_frames_to_basebandsignal_vcc.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/ofdm_symbols_to_frame_cvc.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/file_sink2.pyo"
    "/home/zwobot/projects/mimoots/gr-mimoots/build/python/file_source2.pyo"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

