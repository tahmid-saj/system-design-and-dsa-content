class MyQueue {
public:
    MyQueue() {

    }

    void push(int x) {
        if (stk1.empty()) {
            stk1.push(x);
            return;
        }

        while (!stk1.empty()) {
            stk2.push(stk1.top());
            stk1.pop();
        }

        stk1.push(x);

        while (!stk2.empty()) {
            stk1.push(stk2.top());
            stk2.pop();
        }
    }

    int pop() {
        int top = 0;

        if (!stk1.empty()) {
            top = stk1.top();
            stk1.pop();
        }
        
        return top;
    }

    int peek() {
        return stk1.top();
    }

    bool empty() {
        return stk1.empty();
    }

    stack<int> stk1, stk2;
};

/**
 * Your MyQueue object will be instantiated and called as such:
 * MyQueue* obj = new MyQueue();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->peek();
 * bool param_4 = obj->empty();
 */