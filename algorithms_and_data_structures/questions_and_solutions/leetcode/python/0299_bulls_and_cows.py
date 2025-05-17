class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        # return self.twoHashmaps(secret, guess)
        # return self.twoPasses(secret, guess)
        return self.onePass(secret, guess)

    def twoHashmaps(self, secret, guess):
        # update the frequency of freqSecret and freqGuess as you go + / -
        # if secret[i] == guess[i]: bulls += 1
        # if secret[i] in freqGuess: cows += 1, freqGuess[secret[i]] -= 1
        # if guess[i] in freqSecret: cows += 1, freqSecret[guess[i]] -= 1
        freqSecret, freqGuess, bulls, cows = {}, {}, 0, 0
        for i in range(len(secret)):
            if secret[i] == guess[i]: 
                bulls += 1
                continue
            if secret[i] in freqGuess:
                cows += 1
                freqGuess[secret[i]] -= 1
                if freqGuess[secret[i]] == 0: freqGuess.pop(secret[i])
            else: freqSecret[secret[i]] = freqSecret.get(secret[i], 0) + 1
            if guess[i] in freqSecret:
                cows += 1
                freqSecret[guess[i]] -= 1
                if freqSecret[guess[i]] == 0: freqSecret.pop(guess[i])
            else: freqGuess[guess[i]] = freqGuess.get(guess[i], 0) + 1

        return f"{bulls}A{cows}B"
    
    def twoPasses(self, secret, guess):
        freq, bulls, cows = Counter(secret), 0, 0

        for i in range(len(guess)):
            if guess[i] in freq:
                if secret[i] == guess[i]:
                    bulls += 1
                    cows -= int(freq[guess[i]] <= 0)
                else: cows += int(freq[guess[i]] > 0)
                freq[guess[i]] -= 1
        
        return f"{bulls}A{cows}B"
    
    def onePass(self, secret, guess):
        freq, bulls, cows = defaultdict(int), 0, 0

        for i in range(len(secret)):
            s, g = secret[i], guess[i]
            if s == g: bulls += 1
            else:
                cows += int(freq[s] < 0) + int(freq[g] > 0)
                freq[s] += 1
                freq[g] -= 1
        
        return f"{bulls}A{cows}B"