/*
    hanmaokun@outlook.com
*/
#include <iostream>
#include <fstream>
#include <strstream>
#include <stdio.h>

#include "../dlib/svm_threaded.h"
#include "../dlib/array.h"
#include "../dlib/array2d.h"
#include "../dlib/image_keypoint.h"
#include "../dlib/image_processing.h"
#include "../dlib/data_io.h"
#include "../dlib/image_io.h"
#include "../dlib/image_transforms.h"
#include "../dlib/matrix.h"
#include "../dlib/matrix/matrix_utilities.h"

#include "fhog_svm_detector.h"

// ----------------------------------------------------------------------------------------

using namespace std;
using namespace dlib;

// struct membuf : std::streambuf
// {
//     membuf(char* begin, char* end) {
//         this->setg(begin, begin, end);
//     }
// };

struct membuf : std::streambuf {
    membuf(char const *base, size_t size) {
        char *p(const_cast<char *>(base));
        this->setg(p, p, p + size);
    }
};

struct imemstream : virtual membuf, std::istream {
    imemstream(char const *base, size_t size)
            : membuf(base, size), std::istream(static_cast<std::streambuf *>(this)) {
    }
};

bool isfile(const char* str){
    std::ifstream test(str); 
    if (!test)
    {
      //std::cout << "The file doesn't exist" << std::endl;
        return 0;
    }
    return 1;
}

template <typename T>
int image_binary_to_array2d(const char* binary, int length, array2d<T> &out) {
    char name_buffer[] = "/tmp/scan-detect-XXXXXX";
    if (mkstemp(name_buffer) != 0) {
        FILE *tempfile = fopen(name_buffer, "wb");
        fwrite(binary, sizeof(char), length, tempfile);
        fflush(tempfile);
        load_image(out, name_buffer);
        remove(name_buffer);
        return 1;
    }
    return 0;
}

const double* fhog_svm_det(const char* img_path, const char* model_path, int length){
    //array2d<unsigned char> sizeImg(450, 500);
    array2d<float> loadedImg;
    if(isfile(img_path)){
        cout << "is image." << endl;
        load_image(loadedImg, img_path);

        //resize_image(loadedImg, sizeImg);
    }else{
        image_binary_to_array2d(img_path, length, loadedImg);
    }

    typedef scan_fhog_pyramid<pyramid_down<6> > image_scanner_type;
    object_detector<image_scanner_type> detector;
    deserialize(model_path) >> detector;

    std::vector<rect_detection> dets;
    detector(loadedImg, dets);
    cout << "Number of detections: "<< dets.size() << endl;

    double* ret_rect = new double[5];
    if(dets.size() > 0){
        ret_rect[0] = dets[0].rect.left();
        ret_rect[1] = dets[0].rect.top();
        ret_rect[2] = dets[0].rect.right();
        ret_rect[3] = dets[0].rect.bottom();
        ret_rect[4] = dets[0].detection_confidence;
    } else {
        ret_rect[0] = 0;
        ret_rect[1] = 0;
        ret_rect[2] = 0;
        ret_rect[3] = 0;
        ret_rect[4] = 0.0;
    }

    return ret_rect;
}



double fdetect_blur(const char* img_path, int length) {
    //array2d<unsigned char> sizeImg(450, 500);
    array2d<unsigned char> loadedImg;
    if(isfile(img_path)){
        cout << "is image." << endl;
        load_image(loadedImg, img_path);
    }else{
        image_binary_to_array2d(img_path, length, loadedImg);
    }
    float laplacian_raw [] = {0, 1, 0, 1, -4, 1, 0, 1, 0};
    array2d<float> laplacian_filt(3, 3);
    for (int r = 0; r < 3; r++) {
        for (int c = 0; c < 3; c++) {
            laplacian_filt[r][c] = laplacian_raw[3*r + c];
        }
    }
    array2d<float> imout(loadedImg.nr(), loadedImg.nc());
    spatially_filter_image(loadedImg, imout, mat(laplacian_filt));
    double var = variance(mat(imout));
    return var;

}


int test_dlib_add(int x, int y) {
  return x+y;
}
