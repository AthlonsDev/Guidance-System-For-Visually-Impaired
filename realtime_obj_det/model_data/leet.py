from typing import List

class Solution:
    def romanToInt(self, s: str) -> int:
        #store in dict 
        rn = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500,'M':1000}
        #iterate through string
        for i in range (len(s)):
            #if the current value is less than the next value
            if s[i] < s[i+1]:
                #subtract current valu from next value
                s[i] = s[i+1] - s[i]
            else:
                #add current value to next value
                s[i] = s[i] + s[i+1]
            rn[s[i]] = rn[s[i]] + rn[s[i+1]]
            print(rn[s[i]])


    def main(self):
        s = ["III"]
        print(self.romanToInt(s))

Solution().main()

