class library():
    def __init__(self,f):
        line = f.readline().split()
        self.bookqtt = int(line[0])
        self.signup =  int(line[1])
        self.shiping = int(line[2])

        self.books = []
        line = f.readline().split()
        for i in line:
            self.books.append(int(i))
        

def loadfile (filename):
    with open(filename) as f:
        line = f.readline()
        line = line.split()
        books = int(line[0])
        libs =  int(line[1])
        days =  int(line[2])

        bookscores = []
        line = f.readline()
        line = line.split()
        for i in line:
            bookscores.append(int(i))
        


