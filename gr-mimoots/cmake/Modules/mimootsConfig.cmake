INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MIMOOTS mimoots)

FIND_PATH(
    MIMOOTS_INCLUDE_DIRS
    NAMES mimoots/api.h
    HINTS $ENV{MIMOOTS_DIR}/include
        ${PC_MIMOOTS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MIMOOTS_LIBRARIES
    NAMES gnuradio-mimoots
    HINTS $ENV{MIMOOTS_DIR}/lib
        ${PC_MIMOOTS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MIMOOTS DEFAULT_MSG MIMOOTS_LIBRARIES MIMOOTS_INCLUDE_DIRS)
MARK_AS_ADVANCED(MIMOOTS_LIBRARIES MIMOOTS_INCLUDE_DIRS)

