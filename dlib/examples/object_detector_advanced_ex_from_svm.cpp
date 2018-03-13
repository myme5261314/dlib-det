// The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
/*

    This is an example illustrating the process for defining custom
    bag-of-visual-word style feature extractors for use with the
    structural_object_detection_trainer.

    NOTICE: This example assumes you are familiar with the contents of the
    object_detector_ex.cpp example program.  Also, if the objects you want to
    detect are somewhat rigid in appearance (e.g.  faces, pedestrians, etc.)
    then you should try the methods shown in the fhog_object_detector_ex.cpp
    example program before trying to use the bag-of-visual-word tools shown in
    this example.  
*/

#include <dlib/svm_threaded.h>
#include <dlib/gui_widgets.h>
#include <dlib/array.h>
#include <dlib/array2d.h>
#include <dlib/image_keypoint.h>
#include <dlib/image_processing.h>
#include <dlib/data_io.h>

#include <iostream>
#include <fstream>

using namespace std;
using namespace dlib;

// ----------------------------------------------------------------------------------------

int main()
{  
    try
    {
        dlib::array<array2d<unsigned char> > images_test;
        std::vector<std::vector<rectangle> > boxes_test;
        load_image_dataset(images_test, boxes_test, "/home/nlp/bigsur/devel/dlib/tools/imglab/build/testing.xml");

        /*
            It is also worth pointing out that you don't have to use dlib::array2d objects to 
            represent your images.  In fact, you can use any object, even something like a struct
            of many images and other things as the "image".  The only requirements on an image
            are that it should be possible to pass it to scanner.load().  So if you can say 
            scanner.load(images[0]), for example, then you are good to go.  See the documentation 
            for scan_image_pyramid::load() for more details.
        */
        typedef scan_fhog_pyramid<pyramid_down<6> > image_scanner_type;
        object_detector<image_scanner_type> detector2;
        deserialize("/home/nlp/bigsur/devel/dlib/examples/build/object_detector.svm") >> detector2;

        // Let's display the output of the detector along with our training images.
        image_window win;
        for (unsigned long i = 0; i < images_test.size(); ++i)
        {
            // Run the detector on images[i] 
            const std::vector<rectangle> rects = detector2(images_test[i]);
            cout << "Number of detections: "<< rects.size() << endl;

            // Put the image and detections into the window.
            win.clear_overlay();
            win.set_image(images_test[i]);
            win.add_overlay(rects, rgb_pixel(255,0,0));

            cout << "Hit enter to see the next image.";
            cin.get();
        }

    }
    catch (exception& e)
    {
        cout << "\nexception thrown!" << endl;
        cout << e.what() << endl;
    }
}

// ----------------------------------------------------------------------------------------


