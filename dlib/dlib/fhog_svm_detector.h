/*
	hanmaokun@outlook.com
*/

#ifndef FHOG_SVM_DETECTOR_H_
#define FHOG_SVM_DETECTOR_H_

#include "iostream"
#include "fstream"

typedef struct _dlibRect
{
	long left;
	long top;
	long right;
	long bottom;
}dlibRect;

extern const dlibRect fhog_svm_det(const char* img_file_name);

#endif // FHOG_SVM_DETECTOR_H_
