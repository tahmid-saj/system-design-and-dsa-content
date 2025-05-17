class Solution {
public: 
        string addStrings(string num1, string num2)
        {
            int p1=num1.length()-1;
            int p2=num2.length()-1;
            string sum;
            int carry=0;
            while(p1>=0 || p2>=0)
            {
            int sum2=carry+((p1>=0) ? (num1[p1]-'0') :0)+((p2>=0) ? (num2[p2]-'0') :0);
            sum.push_back(sum2%10+'0');
            carry=sum2/10;
            p1--;
            p2--;
            }
            if(carry>0)sum.push_back(carry+'0');
            reverse(sum.begin(),sum.end());
            return sum;
        }
         
         string multiply1(string num1, char x)
         {
            int p1=num1.length()-1;
            string ans="";
            int carry=0;
            while(p1>=0)
            {
            int sum2=carry+((p1>=0) ? (num1[p1]-'0') :0)*(x-'0');
            ans.push_back(sum2%10+'0');
            carry=sum2/10;
            p1--;
            }
            if(carry>0)ans.push_back(carry+'0');
            reverse(ans.begin(),ans.end());
            return ans;
         }
        
         string multiply(string num1, string num2) {
             if(num1=="0" || num2=="0")return "0";
             string x=multiply1(num1,num2.back());
             int j=num2.size()-2;
             int t=1;
             while(j>=0){
                 string y=multiply1(num1,num2[j]);
                 for(int i=1;i<=t;i++)y+="0";
                 x=addStrings(x,y);
                 j--;
                 t++;
             }
             return x;
             
    }
};