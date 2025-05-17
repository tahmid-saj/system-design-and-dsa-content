#include <iostream>

using namespace std;

int main() {
    int i, sum, j;
    int a[5];
    int n = 5;

    for (i = 0; i < n; i++) {
        for (j = 1, sum = a[0]; j <= i; j++) {
            sum += a[j];
        }
        cout << "sum for subarray 0 through " << i << " is " << sum << endl;
    }

    return 0;
}