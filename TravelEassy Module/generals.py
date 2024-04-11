import random
import datetime
from passlib.hash import sha256_crypt
import json

class Generals:
    def __init__(self):
        self.alphabets_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabets_lower = self.alphabets_upper.lower()
        self.numerics = "0123456789"
        self.symbols = "~!@#$%^&*()_+~"
        self.combinations = self.alphabets_upper + self.alphabets_lower + self.numerics + self.symbols

    def GenRandomCode(self, size=4):
        code = ""
        for _ in range(size):
            unit_code = random.choice(self.combinations)
            code += unit_code
        return code
    
    def GetPasswordHash(self, password):
        return sha256_crypt.hash(password)
    
    def VerifyHash(self, password_hash, secret):
        return sha256_crypt.verify(secret, password_hash)
    
    def GetCurrentTime(self):
        return datetime.datetime.now()
    