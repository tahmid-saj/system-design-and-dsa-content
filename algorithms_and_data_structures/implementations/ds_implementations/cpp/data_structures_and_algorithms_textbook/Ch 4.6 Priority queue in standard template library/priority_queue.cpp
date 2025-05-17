#include <iostream>
#include <queue>
#include <functional>

using namespace std;

int main() {
    priority_queue<int> pq1;
    priority_queue<int, vector<int>, greater<int> > pq2;

    pq1.push(3);
    pq1.push(1);
    pq1.push(2);

    pq2.push(3);
    pq2.push(1);
    pq2.push(2);

    int a[] = {4, 6, 5};

    priority_queue<int> pq3(a, a + 3);

    while (!pq1.empty()) {
        cout << pq1.top() << "  ";
        pq1.pop();
    }

    cout << endl;

    while (!pq2.empty()) {
        cout << pq2.top() << "  ";
        pq2.pop();
    }

    cout << endl;

    while (!pq3.empty()) {
        cout << pq3.top() << "  ";
        pq3.pop();
    }

    return 0;
}