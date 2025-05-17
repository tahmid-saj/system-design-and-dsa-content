class Codec:
    def __init__(self):
        self.chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.shortToLong = {}
    
    def getRandomHashString(self):
        res = []
        while len(res) < 6: res.append(random.choice(self.chars))
        return "".join(res)

    def encode(self, longUrl: str) -> str:
        """Encodes a URL to a shortened URL.
        """
        randomHashString = self.getRandomHashString()
        while randomHashString in self.shortToLong: randomHashString = self.getRandomHashString()
        self.shortToLong[f"http://tinyurl.com/{randomHashString}"] = longUrl
        return f"http://tinyurl.com/{randomHashString}"

    def decode(self, shortUrl: str) -> str:
        """Decodes a shortened URL to its original URL.
        """
        return self.shortToLong[shortUrl]
        

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(url))