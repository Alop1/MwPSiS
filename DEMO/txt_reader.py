# from Crypto.Cipher import AES

class Textfile:
    def __init__(self, textfile, cipher = False):
        f = open(textfile, 'r')
        self.data = f.read()
        # if cipher:
        #     obj = AES.new('This is a key123', AES.MODE_OFB, 'This is an IV456')
        #     self.data = obj.encrypt(self.data)
        self.len_bytes = len(self.data)
        self.len_bits = len(self.data) * 7
        print "tyle znakow w wiadomosci", self.len_bytes



