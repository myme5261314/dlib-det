/*
    hanmaokun@outlook.com
*/


#include <vector>
#include <iostream>
#include "fhog_svm_detector.h"

// ----------------------------------------------------------------------------------------

using namespace std;

int main()
{  
    try
    {
        {
            // Run the detector on images
            cout << "1" << endl;
            const int* rects = fhog_svm_det("03903.jpg");
            cout << rects[0] << endl;
        }

    }
    catch (exception& e)
    {
        cout << "\nexception thrown!" << endl;
        cout << e.what() << endl;
    }
}

// ----------------------------------------------------------------------------------------
