class MyStack {
public:
    MyStack() {

    }

    void push(int x) {
        q1.push(x);

        for (int i = 0; i < q1.size() - 1; i++) {
            q1.push(q1.front());
            q1.pop();
        }
    }

    int pop() {
        int top = q1.front();
        q1.pop();

        return top;
    }

    int top() {
        return q1.front();
    }

    bool empty() {
        return q1.empty();
    }

    queue<int> q1;
};

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack* obj = new MyStack();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->top();
 * bool param_4 = obj->empty();
 */