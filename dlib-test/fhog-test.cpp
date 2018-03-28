/*
    hanmaokun@outlook.com
*/


#include <vector>
#include <iostream>
#include <fstream>

#include "fhog_svm_detector.h"

// ----------------------------------------------------------------------------------------

using namespace std;

int main()
{  
    try
    {
        {
            std::ifstream fin("419207526.bmp");
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
            const double* rects = fhog_svm_det(data, "object_detector.svm", text.length());
            cout << rects[0] << endl;
            cout << rects[1] << endl;
            cout << rects[2] << endl;
            cout << rects[3] << endl;
            cout << rects[4] << endl;
        }

    }
    catch (exception& e)
    {
        cout << "\nexception thrown!" << endl;
        cout << e.what() << endl;
    }
}

// ----------------------------------------------------------------------------------------
