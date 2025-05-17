#include <iostream>

using namespace std;

void shellSort(int data[], int n) {
    register int i, j, hCnt, h;
    int increments[20], k;

    // create an appropriate number of increments h
    for (h = 1, i = 0; h < n; i++) {
        increments[i] = h;
        h = 3 * h + 1;
    }

    // loop on the number of different increments h
    for (i--; i >= 0; i--) {
        h = increments[i];

        // insertion sort for subarray containing every hth element
        for (hCnt = h; hCnt < 2 * h; hCnt++) {
            for (j = hCnt; j < n; ) {
                int tmp = data[j];
                k = j;

                while (k - h >= 0 && tmp < data[k - h]) {
                    data[k] = data[k - h];
                    k -= h;
                }

                data[k] = tmp;
                j += h;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        cout << data[i] << endl;
    }
}

int main()
{
    int data[] = { 5, 3, 8, 2, 1 };

    shellSort(data, 5);

    return 0;
}