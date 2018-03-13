#!/bin/bash
g++ fhog-test.cpp -g -std=c++0x -I./ -L./ -ldlib -llapack -lpng -o fhogtest-static
