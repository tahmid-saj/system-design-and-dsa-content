class Bucket:
  def __init__(self):
    self.bucket = []
  
  def update(self, key, value):
    for i, kv in enumerate(self.bucket):
      if kv[0] == key:
        self.bucket[i] = (key, value)
        return
    self.bucket.append((key, value))

  def get(self, key):
    for i, kv in enumerate(self.bucket):
      if kv[0] == key:
          return kv[1]
    return -1

  def remove(self, key):
    for i, kv in enumerate(self.bucket):
      if kv[0] == key: del self.bucket[i]

class MyHashMap:
  def __init__(self):
    self.keySpace = 2069
    self.hashMap = [Bucket() for _ in range(self.keySpace)]
    
  def hashFunction(self, key):
    return key % self.keySpace

  def put(self, key: int, value: int) -> None:
    index = self.hashFunction(key)
    self.hashMap[index].update(key, value)

  def get(self, key: int) -> int:
    index = self.hashFunction(key)
    return self.hashMap[index].get(key)

  def remove(self, key: int) -> None:
    index = self.hashFunction(key)
    self.hashMap[index].remove(key)