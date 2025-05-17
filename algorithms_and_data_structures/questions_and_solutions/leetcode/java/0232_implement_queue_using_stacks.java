class MyQueue {
    Stack<Integer> stk = new Stack<Integer>();

    public MyQueue() {
        
    }
    
    public void push(int x) {
        if (stk.size() == 0) {
            stk.push(x);
            return;
        }

        Stack<Integer> stk1 = new Stack<Integer>();
        while (!stk.isEmpty()) {
            stk1.push(stk.pop());
        }
        stk.push(x);
        while (!stk1.isEmpty()) {
            stk.push(stk1.pop());
        }
    }
    
    public int pop() {
        return stk.pop();
    }
    
    public int peek() {
        return stk.peek();
    }
    
    public boolean empty() {
        return stk.isEmpty();
    }
}

/**
 * Your MyQueue object will be instantiated and called as such:
 * MyQueue obj = new MyQueue();
 * obj.push(x);
 * int param_2 = obj.pop();
 * int param_3 = obj.peek();
 * boolean param_4 = obj.empty();
 */