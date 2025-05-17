#include <iostream>

using namespace std;

template <class T> // overloaded operator < is used;
int binarySearch(const T arr[], int arrSize, const T &key)
{
    int lo = 0, mid, hi = arrSize - 1;

    while (lo <= hi)
    {
        mid = (lo + hi) / 2;
        if (key < arr[mid])
            hi = mid - 1;
        else if (arr[mid] < key)
            lo = mid + 1;
        else
            return mid; // success: return the index of
    }                   // the cell occupied by key;
    return -1;          // failure: key is not in the array;
}

int main() {
    int a[9] = {0, 1, 2, 3, 4, 5, 6, 7, 8};

    cout << binarySearch(a, 8, 6);

    return 0;
}