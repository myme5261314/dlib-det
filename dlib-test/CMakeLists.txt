cmake_minimum_required(VERSION 3.6)
project(dlib_test)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        fhog-test.cpp
        fhog_svm_detector.h
        make.sh)

add_executable(dlib_test ${SOURCE_FILES})