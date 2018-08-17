import re
import os

import re
class Input():
    def __init__(self, infile):
        self.setInfile(infile)

    def setMatrix(self, A, B, C, matrix):
        self.A = A
        self.B = B
        self.C = C
        self.matrix = matrix

    def parseInfile(self):
        self.tokens = self.getTokens()
        self.matrix,self.C = self.getMatrix()
        self.A = self.tokens[0][0]
        self.B = self.tokens[0][1]

    def getInput(self):
        return (self.A, self.B, self.C, self.matrix)

    def getTokens(self):
        tokens = []
        file = open(self.infile, "r")
        lines = file.readlines()
        file.close()
        for l in lines:
            tokens.append(l.split())
        return tokens

    def getInfile(self):
        return self.infile

    def setInfile(self, infile):
        self.infile = "/home/quentin/workspace/dnaparsTest/inputs/{}".format(infile)

    def getMatrix(self):
        matrix = []
        name_list = []
        for i in range(1, len(self.tokens)):
            matrix.append(list(self.tokens[i][1]))
            name_list.append(self.tokens[i][0])
        return matrix, name_list

    def writeInfile(self):
        temp_lines = [''.join(col) for col in self.matrix]
        new_lines = [" {:<5}{}\n".format(self.A, self.B)]
        for i in range(len(self.matrix)):
            new_lines.append("{:<10}{}\n".format(self.C[i], temp_lines[i]))
        temp_file = open(self.infile,"w")
        temp_file.writelines(new_lines)
        temp_file.close()

class Output():
    def __init__(self, outfile, outtree):
        self.tree = ""
        self.total_length = 0.0
        self.outfile_name = "/home/quentin/workspace/dnaparsTest/outputs/{}".format(outfile)
        self.outtree_name = "/home/quentin/workspace/dnaparsTest/outputs/{}".format(outtree)

    def parse(self):
        self.tree = self.getTree()
        self.total_length = self.getTotalLength()

    def setResults(self, tree, total_length):
        self.tree = tree
        self.total_length = total_length

    def getTotalLength(self):
        file = open(self.outfile_name,'r')
        lines = file.readlines()
        total_length = 0.0
        file.close()
        for line in lines:
            r = re.match(r"^requires a total of\s+([0-9]*.?[0-9]*)", line)
            if r is not None:
                total_length = float(r.group(1))
        return total_length

    def getTree(self):
        file = open(self.outtree_name, 'r')
        lines = file.readlines()
        tree = ''.join(lines)
        tree = tree.replace('\n','')
        tree = self.eliminateBranchLength(tree)
        return tree

    def eliminateBranchLength(self, tree):
        return re.sub(r":[0-9]+.?[0-9]+", '', tree)

class Dnapars():
    def __init__(self):
        self.workspace = "/home/quentin/workspace/dnaparsTest"

    def setInputOutputNames(self, infile_name, outfile_name, outtree_name):
        self.infile = infile_name
        self.outfile = outfile_name
        self.outtree = outtree_name

    def setVersion(self, version_num):
        self.version_num = version_num

    def executeDnapars(self):
        exit_code = os.system("bash -x {}/exe/run.sh {} {} {} {}".format(self.workspace,self.version_num, self.infile, self.outfile, self.outtree))
        #exit_code = os.system("bash -x {}/exe/run.sh {} {} {} {}".format(self.workspace,self.version_num, self.infile, self.outfile, self.outtree))
        if not exit_code == 0:
            print("error")

if __name__ == "__main__":
    dna = Dnapars()
    dna.executeDnapars()
    #print(dna.getTotalLength())
    #print(dna.getTree())

