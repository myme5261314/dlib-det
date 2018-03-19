/*
	hanmaokun@outlook.com
*/

#ifndef FHOG_SVM_DETECTOR_H_
#define FHOG_SVM_DETECTOR_H_

bool isfile(const char* str);

// Return [0, 0, 0, 0] if not detected, [left, top, right, bottom] if detected.
const int* fhog_svm_det(const char* img_path, const char* model_path, int length);

#endif // FHOG_SVM_DETECTOR_H_
