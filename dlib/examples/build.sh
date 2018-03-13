#!/bin/sh
g++ -std=c++11 -O3 -I.. ../dlib/all/source.cpp -lpthread -lX11 $1 -o $2