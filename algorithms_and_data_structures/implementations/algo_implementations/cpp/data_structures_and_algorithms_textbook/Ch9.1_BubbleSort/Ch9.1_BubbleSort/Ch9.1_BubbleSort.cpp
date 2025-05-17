#include <iostream>

using namespace std;

void bubbleSort(int data[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = n - 1; j > i; --j) {
            if (data[j] < data[j - 1]) {
                swap(data[j], data[j - 1]);
            }
        }
    }

    for (int i = 0; i < n; i++) {
        cout << data[i] << endl;
    }
}

int main()
{
    int data[] = { 5, 2, 3, 8, 1 };

    bubbleSort(data, 5);

    return 0;
}