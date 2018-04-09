/*
	hanmaokun@outlook.com
*/

#ifndef FHOG_SVM_DETECTOR_H_
#define FHOG_SVM_DETECTOR_H_

extern bool isfile(const char* str);

// Return [0, 0, 0, 0, 0.0] if not detected, [left, top, right, bottom, score] if detected.
// score is a signed float
extern const double* fhog_svm_det(const char* img_path, const char* model_path, int length);

extern double fdetect_blur(const char* img_path, int length);

extern int test_dlib_add(int x, int y);

#endif // FHOG_SVM_DETECTOR_H_
