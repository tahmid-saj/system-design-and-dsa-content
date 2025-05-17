class Solution {
public:
    string intToRoman(int num) {
        string ret = "";
        vector<string> romans = { "I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"};
        vector<int> values = { 1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000 };
        int index = values.size() - 1;

        while (num > 0) {
            while (values[index] <= num) {
                ret += romans[index];
                num -= values[index];
            }

            index--;
        }

        return ret;
    }
};