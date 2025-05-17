#include <iostream>
#include <algorithm>
#include <deque>

using namespace std;

int main() {
    deque<int> dq1;
    dq1.push_front(1); 
    //dq1=(1)
    dq1.push_front(2); 
    //dq1=(21)
    dq1.push_back(3); 
    //dq1=(213)
    dq1.push_back(4); 
    //dq1=(2134)
    deque<int> dq2(dq1.begin()+1,dq1.end()-1); 
    //dq2=(13)
    dq1[1]=5; 
    //dq1=(2534)
    dq1.erase(dq1.begin()); 
    //dq1=(534)
    dq1.insert(dq1.end()-1,2,6); 
    //dq1=(53664)
    sort(dq1.begin(),dq1.end()); 
    //dq1=(34566)
    deque<int> dq3;
    dq3.resize(dq1.size()+dq2.size());         
    //dq3=(0000000)
    merge(dq1.begin(),dq1.end(),dq2.begin(),dq2.end(),dq3.begin());
    //dq1=(34566)anddq2=(13)==>dq3=(1334566)
    return 0;
}