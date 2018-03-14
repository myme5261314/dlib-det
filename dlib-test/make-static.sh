#!/bin/bash
g++ fhog-test.cpp -g -std=c++0x -L../dlib/build/dlib/ -ldlib -llapack -lpng -o fhogtest-static
