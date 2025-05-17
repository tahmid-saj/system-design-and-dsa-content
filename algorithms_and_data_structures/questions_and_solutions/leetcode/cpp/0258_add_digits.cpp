class Solution {
public:
    int addDigits(int num) {
        if (num < 10) {
            return num;
        }
        
        int newNum = 0;
        
        while (num > 0) {
            newNum += num % 10;
            num /= 10;
        }
        
        if (newNum < 10) {
            return newNum;
        }
        
        return addDigits(newNum);
    }
};