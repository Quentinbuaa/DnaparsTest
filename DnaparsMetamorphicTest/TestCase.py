import random
from Execution import *
#from MRs import *

class TestCase():
    def __init__(self):
        self.set = ['A','T','C','G']

    def setInputOutput(self, infile_name, outfile_name, outtree_name):
        self.infile = infile_name
        self.outfile = outfile_name
        self.outtree = outtree_name

    def generateRandomTestcase(self):
        self.A = random.randint(3,8)
        self.B = random.randint(100,300)
        self.C = self.getNameList()
        self.matrix = self.getMatrix()
        myInput = Input(self.infile)
        myInput.setMatrix(self.A, self.B, self.C, self.matrix)
        myInput.writeInfile()

    def setTestCase(self, A, B, C, matrix):
        self.A = A
        self.B = B
        self.C = C
        self.matrix = matrix

    def getMatrix(self):
        matrix = []
        for row in range(self.A):
            temp = []
            for col in range(self.B):
                temp.append(random.choice(self.set))
            matrix.append(temp)
        return matrix

    def getNameList(self):
        names = ["spe_{}".format(i+1) for i in range(self.A)]
        return names

class TestCase_V1(TestCase):
    def __init__(self):
        super(TestCase_V1, self).__init__()

    def generateRandomTestcase(self):
        self.A = 4
        self.B = random.randint(100,300)
        self.C = self.getNameList()
        self.matrix = self.getMatrix()
        myInput = Input(self.infile)
        myInput.setMatrix(self.A, self.B, self.C, self.matrix)
        myInput.writeInfile()




if __name__ == "__main__":
    ts = TestCase()
    ts.setInputOutput("infile_random", "outfile_random","outtree_random")
    ts.generateTestCase()
