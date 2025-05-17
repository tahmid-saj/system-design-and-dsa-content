#include <iostream>

using namespace std;

void insertionSort(int data[], int n) {
	for (int i = 1, j; i < n; i++) {
		int tmp = data[i];

		for (j = i; j > 0 && tmp < data[j - 1]; j--) {
			data[j] = data[j - 1];
		}

		data[j] = tmp;
	}

	for (int i = 0; i < n; i++) {
		cout << data[i] << endl;
	}
}

int main()
{
	int data[] = { 5, 2, 3, 8, 1 };

	insertionSort(data, 5);

	return 0;
}
