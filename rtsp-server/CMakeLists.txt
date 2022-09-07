cmake_minimum_required(VERSION 3.18)
project(rtsp_server)
find_package(PkgConfig REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(GST REQUIRED
        gobject-2.0
        glib-2.0
        gstreamer-sdp-1.0
        gstreamer-pbutils-1.0
        gstreamer-rtsp-server-1.0
        gstreamer-check-1.0)

set(CMAKE_CXX_STANDARD 20)

add_executable(rtsp_server main.cpp)

target_include_directories(rtsp_server PRIVATE ${GST_INCLUDE_DIRS})
target_link_libraries(rtsp_server ${GST_LIBRARIES})
