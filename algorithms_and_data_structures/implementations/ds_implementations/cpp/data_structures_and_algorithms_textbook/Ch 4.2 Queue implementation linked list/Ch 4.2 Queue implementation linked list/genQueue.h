#ifndef DLL_QUEUE
#define DLL_QUEUE

#pragma once

#include <iostream>

using namespace std;

template<class T>
class Queue
{
public:
	Queue() {

	}

	void clear() {
		lst.clear();
	}

	bool isEmpty() const {
		return lst.empty();
	}

	T& front() {
		return lst.front();
	}

	T dequeue() {
		T el = lst.front();
		lst.pop_front();
		return el;
	}

	void enqueue(const T& el) {
		lst.push_back(el);
	}
	
private:
	list<T> lst;
};

#endif