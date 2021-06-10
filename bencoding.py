class Decoder:

    """
    Decodes Bencoded sequence of bytes
    """
    def __init__(self,data):
        if not isinstance(data,bytes):
            raise TypeError('Argument is not of type "bytes" ')
        self.data=data.decode() #converting bytes to string type
        self.index=-1
        self.character=None

    def getCharacter(self):
        self.index+=1
        if self.index>=len(self.data):
            self.character=None
        else:
            self.character= self.data[self.index]
    def getLength(self):
        lenOfString=''
        while self.character!=':':
            lenOfString+=self.character
            self.getCharacter()

        return int(lenOfString)
    def getString(self,lenOfString):
        output=''
        for _ in range(lenOfString):
            self.getCharacter()
            output+=self.character

        return output

    def decode(self):
        self.getCharacter()
        if self.character == None:
            raise EOFerror('Unexpected end of file')
        elif self.character == 'i':
            ##code for integerInput
            self.getCharacter()
            output=''
            while self.character!='e':
                output+=self.character
                self.getCharacter()
            return int(output)
        elif self.character == 'd':
            ##code for dictionary input
            output={}
            while self.character!='e':
                key=self.decode()
                if key!=None:
                    value=self.decode()
                    output[key]=value
            return output
        elif self.character == 'l':
            ##code for list input
            output=[]
            while self.character!='e':
                item=self.decode()
                if item!=None:
                    output.append(item)
            return output
        elif self.character in '0123456789':
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
            return str(len(data)).encode()+data
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
