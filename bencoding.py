import re


class Decoder:

    """
    Decodes Bencoded sequence of bytes
    """
    def __init__(self,data):
        if not isinstance(data,bytes):
            raise TypeError('Argument is not of type "bytes" ')
        self.data=data.decode() #converting bytes to string type
        self.index=-1
    def getCharacter(self):
        self.index+=1
        if self.index>len(self.data):
            return None
        return self.data[self.index]
    def decode(self):
        character=self.getCharacter()
        if character == None:
            raise EOFerror('Unexpected end of file')
        elif character == i:
            ##code for integerInput
            pass
        elif character == d:
            ##code for dictionary input
            pass
        elif character == l:
            ##code for list input
            pass
        elif character in '0123456789':
            ##code for a string input
            pass
