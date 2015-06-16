if (SKUNKWORKS_INCLUDES)
set (SKUNKWORKS_FIND_QUIETLY TRUE)
endif (SKUNKWORKS_INCLUDES)


find_path(SKUNKWORKS_CORE_INCLUDE G3Pipeline.h PATHS $ENV{SPT3G_SOFTWARE_PATH}/core/include/core/)
find_path(SKUNKWORKS_DFMUX_INCLUDE dfmux PATHS $ENV{SPT3G_SOFTWARE_PATH}/dfmux/include/)
find_path(SKUNKWORKS_HK_INCLUDE hkgetter.h PATHS $ENV{SPT3G_SOFTWARE_PATH}/hk/)
find_library(SKUNKWORKS_CORE_LIBRARY core.so PATHS $ENV{SPT3G_SOFTWARE_BUILD_PATH}/skunkworks/)
find_library(SKUNKWORKS_DFMUX_LIBRARY dfmux.so $ENV{SPT3G_SOFTWARE_BUILD_PATH}/skunkworks/)
find_library(SKUNKWORKS_HK_LIBRARY hk.so $ENV{SPT3G_SOFTWARE_BUILD_PATH}/skunkworks/)

include (FindPackageHandleStandardArgs)
#find_package_handle_standard_args(SKUNKWORKS DEFAULT_MSG SKUNKWORKS_CORE_INCLUDE SKUNKWORKS_CORE_LIBRARY)
find_package_handle_standard_args (SKUNKWORKS DEFAULT_MSG 
  SKUNKWORKS_CORE_INCLUDE SKUNKWORKS_DFMUX_INCLUDE SKUNKWORKS_HK_INCLUDE 
  SKUNKWORKS_CORE_LIBRARY SKUNKWORKS_DFMUX_LIBRARY SKUNKWORKS_HK_LIBRARY)

mark_as_advanced(  SKUNKWORKS_CORE_INCLUDE SKUNKWORKS_DFMUX_INCLUDE SKUNKWORKS_HK_INCLUDE 
  SKUNKWORKS_CORE_LIBRARY SKUNKWORKS_DFMUX_LIBRARY SKUNKWORKS_HK_LIBRARY SKUNKWORKS_INCLUDES SKUNKWORKS_LIBRARIES)

set(SKUNKWORKS_INCLUDES ${SKUNKWORKS_CORE_INCLUDE} ${SKUNKWORKS_DFMUX_INCLUDE} ${SKUNKWORKS_HK_INCLUDE})
set(SKUNKWORKS_LIBRARIES ${SKUNKWORKS_CORE_LIBRARY} ${SKUNKWORKS_DFMUX_LIBRARY} ${SKUNKWORKS_HK_LIBRARY})

message(STATUS ${SKUNKWORKS_INCLUDES} ${SKUNKWORKS_LIBRARIES})
