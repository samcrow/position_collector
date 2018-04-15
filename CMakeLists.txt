cmake_minimum_required(VERSION 3.1)

set(TARGET position_collector)
set(HEADERS
    src/position.h
    src/vr_position.h
    src/pozyx_position.h
    src/rate_printer.h
)
set(SOURCES
    src/main.cpp
    src/vr_position.cpp
    src/pozyx_position.cpp
    src/rate_printer.cpp
)

set(CMAKE_CXX_STANDARD 11)

find_library(OPENVR_LIBRARIES NAMES openvr_api REQUIRED PATHS openvr/lib)
include_directories(openvr/include)
set(OPENVR_HEADERS openvr/include/openvr.h)

find_package(Threads REQUIRED)


add_executable(${TARGET} ${SOURCES} ${OPENVR_HEADERS})
target_link_libraries(${TARGET} ${OPENVR_LIBRARIES} ${CMAKE_DL_LIBS} ${CMAKE_THREAD_LIBS_INIT})

if ( CMAKE_COMPILER_IS_GNUCC )
    target_compile_options(${TARGET} PRIVATE -Wall -Wextra -pedantic)
endif ( CMAKE_COMPILER_IS_GNUCC )
