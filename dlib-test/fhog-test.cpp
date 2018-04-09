/*
    hanmaokun@outlook.com
*/


#include <vector>
#include <iostream>
#include <fstream>
#include <strstream>
#include <stdio.h>

#include "fhog_svm_detector.h"

//#include "../dlib/dlib/svm_threaded.h"
#include "../dlib/dlib/array.h"
//#include "../dlib/dlib/array2d.h"
//#include "../dlib/dlib/image_keypoint.h"
//#include "../dlib/dlib/image_processing.h"
//#include "../dlib/dlib/data_io.h"
//#include "../dlib/dlib/image_io.h"
#include "../dlib/dlib/gui_widgets.h"

// ----------------------------------------------------------------------------------------

using namespace std;
using namespace dlib;

int main(int argc, char** argv)
{  
    try
    {
        {
            char *image_file_name = argv[1];
            std::ifstream fin(image_file_name);
            if (!fin)
                cout << "failed to open file." << endl;

            std::string line, text;
            int ctr = 0;
            while(std::getline(fin, line))
            {
                text += line + '\n';

                ctr += 1;
            }
            cout << ctr << endl;
            cout << text.length() << endl;
            const char* data = text.c_str();

            const double* rects = fhog_svm_det(data, "object_detector_yz.svm", text.length());
            cout << rects[0] << endl;
            cout << rects[1] << endl;
            cout << rects[2] << endl;
            cout << rects[3] << endl;
            cout << rects[4] << endl;

            // dlib::image_window win;
            // win.clear_overlay();
            // win.set_image(image_file_name);
            // //std::vector<dlib::rectangle> rects_[1];
            // dlib::rectangle rec(rects[0], rects[1], rects[2], rects[3]);
            // win.add_overlay(rec, dlib::rgb_pixel(255,0,0));
            // cin.get();
        }

    }
    catch (exception& e)
    {
        cout << "\nexception thrown!" << endl;
        cout << e.what() << endl;
    }
}

// ----------------------------------------------------------------------------------------
