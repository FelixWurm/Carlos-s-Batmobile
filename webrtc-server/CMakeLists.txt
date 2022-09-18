cmake_minimum_required(VERSION 3.18)
project(webrtc_server)
find_package(PkgConfig REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(GST REQUIRED
        gobject-2.0
        glib-2.0
        gstreamer-sdp-1.0
        gstreamer-webrtc-1.0
        libsoup-2.4
        json-glib-1.0)

set(CMAKE_C_STANDARD 11)

add_executable(webrtc_server main.c)

target_include_directories(webrtc_server PRIVATE ${GST_INCLUDE_DIRS})
target_link_libraries(webrtc_server ${GST_LIBRARIES})
