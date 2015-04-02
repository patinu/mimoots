# Install script for directory: /home/zwobot/projects/mimoots/gr-mimoots/grc

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
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks" TYPE FILE FILES
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_logcsv_cb.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_extract_frame_cvc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_scale_symbol_vcvc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_create_frames_bc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_receive_frames_cb.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_uhd_sink.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_uhd_source.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_uhd_sink2.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_uhd_source2.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_symbol_mapper_bc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_symbols_to_frame_cc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_symbol_demapper_cb.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_basebandsignal_to_frames_cvc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_frame_to_symbols_vcc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_frames_to_basebandsignal_vcc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_ofdm_symbols_to_frame_cvc.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_file_sink2.xml"
    "/home/zwobot/projects/mimoots/gr-mimoots/grc/mimoots_file_source2.xml"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

