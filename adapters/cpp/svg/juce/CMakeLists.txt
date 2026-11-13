cmake_minimum_required(VERSION 3.22)
project(parsarium_juce_svg VERSION 1.0.0 LANGUAGES C CXX)

add_subdirectory("${JUCE_SOURCE_DIR}" juce)
juce_add_console_app(parsarium_juce_svg PRODUCT_NAME ParsariumJuceSvg
    NEEDS_WEB_BROWSER FALSE NEEDS_CURL FALSE)
target_sources(parsarium_juce_svg PRIVATE ../juce.cpp)
target_link_libraries(parsarium_juce_svg PRIVATE juce::juce_graphics)
target_compile_definitions(parsarium_juce_svg PRIVATE JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0)
