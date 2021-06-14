class Decoder:

    """
    Decodes Bencoded sequence of bytes
    """
    def __init__(self,data):
        if not isinstance(data,bytes):
            raise TypeError('Argument is not of type "bytes" ')
        self.data=data
        self.index=-1
        self.character=None

    def getCharacter(self):
        self.index+=1
        if self.index>=len(self.data):
            self.character=None
        else:
            self.character= self.data[self.index:self.index+1]

    def getLength(self):
        lenOfString=b''
        while self.character!=b':':

            lenOfString+=self.character
            self.getCharacter()

        return int(lenOfString)
    def getString(self,lenOfString):
        output=b''
        for _ in range(lenOfString):
            self.getCharacter()
            output+=self.character

        return output

    def decode(self):

        if self.character == None:
            self.getCharacter()
            if self.character==None:
                raise EOFerror('Unexpected end of file')
        if self.character == b'i':
            ##code for integerInput
            self.getCharacter()
            output=b''
            while self.character!=b'e':

                output+=self.character
                self.getCharacter()
            return int(output)
        elif self.character == b'd':
            ##code for dictionary input
            output={}
            self.getCharacter()
            while self.character!=b'e':

                key=self.decode()
                if key!=None:
                    self.getCharacter()
                    value=self.decode()
                    output[key]=value

                    self.getCharacter()

            return output
        elif self.character == b'l':
            ##code for list input
            output=[]
            self.getCharacter()
            while self.character!=b'e':
                item=self.decode()
                if item!=None:
                    output.append(item)
                    self.getCharacter()
            return output
        elif self.character in b'0123456789':
            ##code for a string input
            lenOfString=self.getLength()
            return self.getString(lenOfString)


class Encoder:
    def __init__(self,data):
        self.data=data
        self.index=-1
        self.character=None


    def startEncoding(self):
        #start encoding if every element
        return self.encode(self.data)

    def encode(self,data):
        if type(data) == bytes:
            #handle byte data
            return str(len(data)).encode()+b':'+data
        elif type(data) == list:
            #handle list data
            benlist=b''
            for item in data:
                benlist += self.encode(item)
            return b'l'+benlist+b'e'
        elif type(data) == dict:
            #handle dict data
            bendict=b''
            for key,value in data.items():
                bendict += self.encode(key)+self.encode(value)
            return b'd'+bendict+b'e'
        elif type(data) == int:
            #handle int type
            return ('i'+str(data)+'e').encode()
        elif type(data)== str:
            #handle string type of data
            return (str(len(data))+':'+data).encode()
        else:
            raise TypeError('This type of data is not supported in bencoding')
