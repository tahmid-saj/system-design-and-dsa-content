class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> parens;
        string paren;
        generate(n, 0, 0, paren, parens);
        return parens;
    }

private:
    void generate(int n, int l, int r, string paren, vector<string>& parens) {
        if (l == n && r == n) {
            parens.push_back(paren);
        } else {
            if (l < n) {
                generate(n, l + 1, r, paren + '(', parens);
            }
            if (r < l) {
                generate(n, l, r + 1, paren + ')', parens);
            }
        }
    }
};