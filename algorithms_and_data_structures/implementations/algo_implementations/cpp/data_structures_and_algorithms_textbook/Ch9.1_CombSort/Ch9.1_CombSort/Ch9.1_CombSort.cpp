#include <iostream>

using namespace std;

void combSort(int data[], int n) {
    int step = n, j, k;

    while ((step = int(step / 1.3)) > 1) {
        for (j = n - 1; j >= step; j--) {
            k = j - step;

            if (data[j] < data[k]) {
                swap(data[j], data[k]);
            }
        }
    }

    bool again = true;

    for (int i = 0; i < n - 1 && again; i++) {
        for (j = n - 1, again = false; j > i; j--) {
            if (data[j] < data[j - 1]) {
                swap(data[j], data[j - 1]);
                again = true;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        cout << data[i] << endl;
    }
}

int main()
{
    int data[] = { 41, 11, 18, 7, 16, 25, 4, 23 };

    combSort(data, 8);

    return 0;
}