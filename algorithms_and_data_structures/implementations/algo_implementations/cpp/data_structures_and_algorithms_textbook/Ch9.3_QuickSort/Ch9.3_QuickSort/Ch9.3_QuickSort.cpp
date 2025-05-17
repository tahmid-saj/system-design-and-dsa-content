#include <iostream>

using namespace std;

void quickSort(int data[], int first, int last) {
    int lower = first + 1, upper = last;

    swap(data[first], data[(first + last) / 2]);

    int bound = data[first];

    while (lower <= upper) {
        while (bound > data[lower]) {
            lower++;
        }

        while (bound < data[upper]) {
            upper--;
        }

        if (lower < upper) {
            swap(data[lower++], data[upper--]);
        }

        lower++;
    }

    swap(data[upper], data[first]);

    if (first < upper - 1) {
        quickSort(data, first, upper - 1);
    }

    if (upper + 1 < last) {
        quickSort(data, upper + 1, last);
    }
}

void quickSort(int data[], int n) {
    int i, max;

    if (n < 2) {
        return;
    }

    for (i = 1, max = 0; i < n; i++) {
        if (data[max] < data[i]) {
            max = i;
        }
    }

    swap(data[n - 1], data[max]);
    quickSort(data, 0, n - 2);

    // Displaying the sorted result
    for (int i = 0; i < n; i++) {
        cout << data[i] << endl;
    }
}

int main()
{
    int data[] = { 5, 3, 8, 2, 1 };

    quickSort(data, 5);
    
    return 0;
}