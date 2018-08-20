import random
import re
from Execution import *
from TestCase import *

class MR():
    def __init__(self):
        self.set = ['A','G','C','T']

    def setExecutor(self, executor):
        self.executor = executor

    def setTestCase(self, ts):
        self.original_ts = ts

    def process(self):
        self.executeTestCase(self.original_ts)
        original_input = Input(self.original_ts.infile)
        original_input.parseInfile()                                    # load the A,B,C and matrix information
        original_output= self.getResults(self.original_ts)
        followup_ts = self.generateFollowupTestCase(original_input)
        self.executeTestCase(followup_ts)
        followup_output = self.getResults(followup_ts)
        expected_output = self.getExpectedOutput(original_output)
        self.isViolate = self.assertViolation(expected_output, followup_output)
        if self.isViolate:
            print("True")
        else:
            print("False")


    def generateFollowupTestCase(self, original_input):
        ts = TestCase()
        followup_infile = "{}_f".format(self.original_ts.infile)
        followup_outfile = "{}_f".format(self.original_ts.outfile)
        followup_outtree = "{}_f".format(self.original_ts.outtree)
        ts.setInputOutput(followup_infile, followup_outfile,followup_outtree)
        followup_input = self.getExpectedMatrix(original_input)
        followup_input.setInfile(followup_infile)
        followup_input.writeInfile()
        return ts

    def assertViolation(self, exp_output, followup_output):
        if exp_output.tree == followup_output.tree and exp_output.total_length == followup_output.total_length:
            return False
        else:
            return True

    def getExpectedOutput(self, original_output):
        expected_output = Output(original_output.outfile_name, original_output.outtree_name)
        expected_output.tree = original_output.tree
        expected_output.total_length = original_output.total_length
        return expected_output

    def getResults(self,ts):
        result = Output(ts.outfile, ts.outtree)
        result.parse()
        return result

    def executeTestCase(self,ts):
        self.executor.setInputOutputNames(ts.infile, ts.outfile, ts.outtree)
        self.executor.executeDnapars()

    def getExpectedMatrix(self, original_input):
        return original_input

    def setKilledMutantsTable(self,table):
        self.table = table


class MR1(MR):

    def __init__(self):
        super(MR1, self).__init__()
        self.a = 3
        self.b = 4

    def getExpectedMatrix(self, original_input):
        self.a = random.randint(0, len(original_input.matrix[0])-1)
        self.b = self.a -3
        for i in range(len(original_input.matrix)):
            temp = original_input.matrix[i][self.a]
            original_input.matrix[i][self.a] = original_input.matrix[i][self.b]
            original_input.matrix[i][self.b] = temp
        return original_input

class MR2(MR):
    def __init__(self):
        super(MR2, self).__init__()
        self.insert_index = 3
        self.site_count = 50
        self.insert_site = random.choice(self.set) # randomly choice an element from a list. Don't use sample(), which will return a list object.

    def getExpectedMatrix(self,original_input):
        original_input.B = str(int(original_input.B)+self.site_count)
        for i in range(len(original_input.matrix)):
            for j in range(self.site_count):
                original_input.matrix[i].insert(self.insert_index, self.insert_site)
        return original_input

class MR3(MR):

    def getExpectedMatrix(self, original_input):
        row = len(original_input.matrix)
        col = len(original_input.matrix[0])
        candidates = []
        for c in range(col):
            for r in range(1,row):
                if not original_input.matrix[r][c] == original_input.matrix[0][c]:
                    candidates.append(c)
                    break
        temp_matrix = []
        for r in range(row):
            temp = []
            for c in candidates:
                temp.append(original_input.matrix[r][c])
            temp_matrix.append(temp)

        original_input.B = str(len(candidates))
        original_input.matrix = temp_matrix
        return original_input


class MR4(MR):
    def getExpectedMatrix(self, original_input):
        original_input.B = str(2 * int(original_input.B))
        col = len(original_input.matrix[0])
        for i in range(len(original_input.matrix)):
            for j in range(col):
                original_input.matrix[i].append(original_input.matrix[i][j])
        return original_input

    def getExpectedOutput(self, original_output):
        expected_output = Output(original_output.outfile_name, original_output.outtree_name)
        expected_output.tree = original_output.tree
        expected_output.total_length = float(original_output.total_length)*2
        return expected_output

class MR5(MR):
    def __init__(self):
        super(MR5, self).__init__()

    def getExpectedMatrix(self, original_input):
        if len(original_input.matrix) == 4:
            insert_index = random.randint(0, len(original_input.matrix[0])-1)
            for i in range(4):
                original_input.matrix[i].insert(insert_index, self.set[i])
            original_input.B =str(int(original_input.B)+1)
            return original_input
        else:
            print("Cannot compound for this testcase\n")
            return None

    def assertViolation(self, exp_output, followup_output):
        if exp_output.tree == followup_output.tree:
            return False
        else:
            return True


class MR6(MR):
    def __init__(self):
        super(MR6, self).__init__()
        #self.permutation_set = dict(zip(self.set, random.sample(self.set, len(self.set))))
        self.permutation_set = []
        for i in range(len(self.set)):
            self.permutation_set.append(self.set[i-1])
        self.permutation_set = dict(zip(self.set, self.permutation_set))
        # self.permutation_set = dict(zip(self.set, random.sample(self.set, len(self.set))))

    def getExpectedMatrix(self, original_input):
        row = len(original_input.matrix)
        col = len(original_input.matrix[0])
        for i in range(row):
            for j in range(col):
                original_input.matrix[i][j] = self.permutation_set[original_input.matrix[i][j]]
        return original_input

class MR7(MR):
    def __init__(self):
        super(MR7, self).__init__()
        self.new_taxon = ""
        self.picked_taxon = ""
        self.source_index = 0

    def getExpectedMatrix(self, original_input):
        self.source_index = 2
        #self.source_index = random.randint(0,len(original_input.C)-1) # a<= N <= b
        self.picked_taxon = original_input.C[self.source_index]
        self.new_taxon = self.picked_taxon+"_1"
        original_input.C.insert(self.source_index, self.new_taxon)
        original_input.A = str(int(original_input.A)+1)
        original_input.matrix.insert(self.source_index, original_input.matrix[self.source_index])
        return original_input

    def getExpectedOutput(self, original_output):
        expected_output = Output(original_output.outfile_name, original_output.outtree_name)
        tree = original_output.tree
        tree = re.sub(r"{}".format(self.picked_taxon), "({},{})".format(self.picked_taxon,self.new_taxon), tree)
        expected_output.tree = tree
        expected_output.total_length = original_output.total_length
        return expected_output

class CompositionMR(MR):
    def __init__(self):
        super(CompositionMR, self).__init__()
        self.MRs = [MR7(), MR4()]
        self.MRs.reverse()

    def setMRs(self, mr_list):
        self.MRs = mr_list
        self.MRs.reverse()

    def getExpectedOutput(self, original_output):
        for mr in self.MRs:
            original_output = mr.getExpectedOutput(original_output)
        return original_output

    def getExpectedMatrix(self, original_input):
        for mr in self.MRs:
            original_input = mr.getExpectedMatrix(original_input)
        return original_input

    def assertViolation(self, exp_output, followup_output):
        return self.MRs[-1].assertViolation(exp_output, followup_output)


if __name__ == "__main__":
    killed_v = []
    ts =TestCase()
    dna = Dnapars()
    cmr = CompositionMR()
    cmr.setMRs([MR5(),MR2()])
    mr_list = [MR1(),MR3(), MR2(), MR4(),MR6()]
    mutants_list = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"]
    for mr in mr_list:
        table = dict(zip(mutants_list, [0]*len(mutants_list)))
        for i in range(100):
            ts.setInputOutput("infile_{}".format(i), "outfile_{}".format(i),"outtree_{}".format(i))
            ts.generateRandomTestcase()
            mr.setTestCase(ts)
            mr.setExecutor(dna)
            for v in mutants_list:
                dna.setVersion(v)
                mr.process()
                if mr.isViolate:
                    table[v] = table[v]+1
        mr.setKilledMutantsTable(table)
    for mr in mr_list:
        print(mr.__class__.__name__)
        for v, t in mr.table.items():
            print("{}: {}\t,".format(v, t))
        print("\n")

