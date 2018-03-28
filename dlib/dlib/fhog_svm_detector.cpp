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

const double* fhog_svm_det(const char* img_path, const char* model_path, int length){
    //array2d<unsigned char> sizeImg(450, 500);
    int L_tmpname = 200;
    array2d<unsigned char> loadedImg;
    if(isfile(img_path)){
        cout << "is image." << endl;
        load_image(loadedImg, img_path);

        //resize_image(loadedImg, sizeImg);
    }else{
        char *img_content = (char *)img_path;
        char name_buffer[L_tmpname];
        tmpnam(name_buffer);
        FILE *tempfile = fopen(name_buffer, "wb");
        fwrite(img_content, sizeof(char), length, tempfile);
        fflush(tempfile);
        //imemstream in(img_content, length);
        //load_bmp(images[0], in);
        //resize_image(images[0], sizeImg);
        load_image(loadedImg, name_buffer);
        remove(name_buffer);
    }

    typedef scan_fhog_pyramid<pyramid_down<6> > image_scanner_type;
    object_detector<image_scanner_type> detector;
    deserialize(model_path) >> detector;

    const std::vector<rectangle> rects = detector(loadedImg);
    std::vector<rect_detection> dets;
    detector(loadedImg, dets);
    cout << "Number of detections: "<< dets.size() << endl;

    double* ret_rect = new double[5];
    if(rects.size() > 0){
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


int test_dlib_add(int x, int y) {
  return x+y;
}
