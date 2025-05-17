#include <iostream>

using namespace std;

void selectionSort(int data[], int n) {
    for (int i = 0, j, least; i < n - 1; i++) {
        for (j = i + 1, least = i; j < n; j++) {
            if (data[j] < data[least]) {
                least = j;
            }
            swap(data[least], data[i]);
        }
    }

    for (int i = 0; i < n; i++) {
        cout << data[i] << endl;
    }
}

int main()
{
    int data[] = { 5, 2, 3, 8, 1 };

    selectionSort(data, 5);

    return 0;
}