#!/bin/sh
g++ fhog-test.cpp -g -std=c++0x -I./ -L../dlib/build/dlib/ -ldlib -o fhogtest
