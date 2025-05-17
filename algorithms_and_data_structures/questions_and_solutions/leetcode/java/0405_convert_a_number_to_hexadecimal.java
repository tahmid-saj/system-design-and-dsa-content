class Solution {
    static char[] hex = new char[]{'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};

    public String toHex(int num) {
        if (num == 0) return "0";
        long val = num;

        if (num < 0) val = 4_294_967_296L + num; // 2 ^ 32

        List<Integer> list = new ArrayList<>();

        while (val > 0) {
            list.add((int) (val % 16));
            val /= 16;
        }

        StringBuilder sb = new StringBuilder();
        
        for (int i = list.size() - 1; i >= 0; i--) {
            sb.append(hex[list.get(i)]);
        }
        
        return sb.toString();
    }
}