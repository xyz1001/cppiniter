######################################################################
# Automatically generated by cppiniter {{{date_time}}}
######################################################################

add_executable(unittest)

target_include_directories(unittest PRIVATE ${CMAKE_CURRENT_LIST_DIR})

file(GLOB SRC "*/*.h"
              "*/*.cpp"
              "*.hpp"
              "*.cpp")
target_sources(unittest PRIVATE ${SRC})

find_package(doctest REQUIRED CONFIG)

target_link_libraries(unittest doctest::doctest {{{project_name}}})

if(LINUX)
    set_target_properties(unittest PROPERTIES INSTALL_RPATH "$ORIGIN/../lib")
elseif(APPLE)
    set_target_properties(unittest PROPERTIES INSTALL_RPATH "@executable_path/../lib")
endif()
INSTALL(TARGETS unittest RUNTIME DESTINATION bin)
