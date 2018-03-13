/*
    hanmaokun@outlook.com
*/


#include <vector>
#include "fhog_svm_detector.h"

// ----------------------------------------------------------------------------------------

using namespace std;

int main()
{  
    try
    {
        {
            // Run the detector on images
            const dlibRect rects = fhog_svm_det("./03903.jpg");
            cout << rects.left << endl;
        }

    }
    catch (exception& e)
    {
        cout << "\nexception thrown!" << endl;
        cout << e.what() << endl;
    }
}

// ----------------------------------------------------------------------------------------
