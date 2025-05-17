#include <iostream>

using namespace std;

void moveDown(int data[], int first, int last) {
    int largest = 2 * first + 1;

    while (largest <= last) {
        if (largest < last && data[largest] < data[largest + 1]) {
            largest++;
        }

        if (data[first] < data[largest]) {
            swap(data[first], data[largest]);
            first = largest;
            largest = 2 * first + 1;
        }
        else {
            largest = last + 1;
        }
    }
}

void heapSort(int data[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--) {
        moveDown(data, i, n - 1);
    }

    for (int i = n - 1; i >= 1; i--) {
        swap(data[0], data[i]);
        moveDown(data, 0, i - 1);
    }

    // Printing the elements
    for (int i = 0; i < n; i++) {
        cout << data[i] << endl;
    }
}

int main()
{
    int data[] = { 5, 3, 2, 8, 1 };

    heapSort(data, 5);

    return 0;
}