/*
    hanmaokun@outlook.com
*/
#include <iostream>
#include <fstream>
#include <strstream>

#include "../dlib/svm_threaded.h"
#include "../dlib/array.h"
#include "../dlib/array2d.h"
#include "../dlib/image_keypoint.h"
#include "../dlib/image_processing.h"
#include "../dlib/data_io.h"

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

const int* fhog_svm_det(const char* img_path, const char* model_path, int length){
    dlib::array<array2d<unsigned char> > images;

    images.resize(1);

    array2d<unsigned char> sizeImg(450, 500);
    array2d<unsigned char> loadedImg;
    if(isfile(img_path)){
        cout << "is image." << endl;
        load_image(loadedImg, img_path);

        resize_image(loadedImg, sizeImg);
    }else{
        char *img_content = (char *)img_path;
        imemstream in(img_content, length);
        load_bmp(images[0], in);
        resize_image(images[0], sizeImg);
    }

    typedef scan_fhog_pyramid<pyramid_down<6> > image_scanner_type;
    object_detector<image_scanner_type> detector;
    deserialize(model_path) >> detector;

    const std::vector<rectangle> rects = detector(sizeImg);
    cout << "Number of detections: "<< rects.size() << endl;

    int* ret_rect = new int[4];
    if(rects.size() > 0){
        ret_rect[0] = rects[0].left();
        ret_rect[1] = rects[0].top();
        ret_rect[2] = rects[0].right();
        ret_rect[3] = rects[0].bottom();
    } else {
        ret_rect[0] = 0;
        ret_rect[1] = 0;
        ret_rect[2] = 0;
        ret_rect[3] = 0;
    }

    return ret_rect;
}


int test_dlib_add(int x, int y) {
  return x+y;
}

/* test. */
// int main()
// {  
//     try
//     {
//         image_window win;
//         {
//             // Run the detector on images
//             const std::vector<rectangle> rects = fhog_svm_det("/home/nlp/bigsur/data/data_ssd_id_train_resized/03903.jpg");
//             cout << "Number of detections: "<< rects.size() << endl;

//             // Put the image and detections into the window.
//             win.clear_overlay();
//             dlib::array<array2d<unsigned char> > images_test;

//             images_test.resize(1);
//             load_image(images_test[0], "/home/nlp/bigsur/data/data_ssd_id_train_resized/03903.jpg");
//             win.set_image(images_test[0]);
//             win.add_overlay(rects, rgb_pixel(255,0,0));

//             cout << "Hit enter to see the next image.";
//             cin.get();
//         }

//     }
//     catch (exception& e)
//     {
//         cout << "\nexception thrown!" << endl;
//         cout << e.what() << endl;
//     }
// }

// ----------------------------------------------------------------------------------------
