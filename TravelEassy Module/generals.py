import random
import datetime
from passlib.hash import sha256_crypt

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
    
    def TokenAuthentication(self, user_token, all_tokens):
        for x in all_tokens:
            if x["token"] == user_token:
                pass

    def GenAccessToken(self, all_tokens:list):
        while True:
            access_token = self.GenRandomCode(size=30)
            state = True
            for x in all_tokens:
                if x["token"] == access_token:
                    state = False
                    break
            if state == True:
                return access_token   
    
    def SterilizeJSON(self):
        pass