import random
import re
from Execution import *
from TestCase import *
import itertools
import copy

class MR():
    def __init__(self):
        self.set = ['A','G','C','T']
        self.name = self.__class__.__name__

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
        #if self.isViolate:
        #    print("True")
        #else:
        #    print("False")


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
        followup_input = copy.deepcopy(original_input)
        self.a = random.randint(0, len(followup_input.matrix[0])-1)
        self.b = self.a -3
        for i in range(len(followup_input.matrix)):
            temp = followup_input.matrix[i][self.a]
            followup_input.matrix[i][self.a] = followup_input.matrix[i][self.b]
            followup_input.matrix[i][self.b] = temp
        return followup_input

class MR2(MR):
    def __init__(self):
        super(MR2, self).__init__()
        self.insert_index = 3
        self.site_count = 50
        self.insert_site = random.choice(self.set) # randomly choice an element from a list. Don't use sample(), which will return a list object.

    def getExpectedMatrix(self,original_input):
        followup_input = copy.deepcopy(original_input)
        followup_input.B = str(int(followup_input.B)+self.site_count)
        for i in range(len(followup_input.matrix)):
            for j in range(self.site_count):
                followup_input.matrix[i].insert(self.insert_index, self.insert_site)
        return followup_input

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
        followup_input = copy.deepcopy(original_input)
        self.source_index = 2
        #self.source_index = random.randint(0,len(original_input.C)-1) # a<= N <= b
        self.picked_taxon = followup_input.C[self.source_index]
        self.new_taxon = self.picked_taxon+"_1"
        followup_input.C.insert(self.source_index, self.new_taxon)
        followup_input.A = str(int(followup_input.A)+1)
        followup_input.matrix.insert(self.source_index, followup_input.matrix[self.source_index])
        return followup_input

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
        self.name = self.getName()
        self.MRs.reverse()

    def setMRs(self, mr_list):
        self.MRs = mr_list
        self.name = self.getName()
        self.MRs.reverse()

    def getName(self):
        return ''.join([mr.__class__.__name__ for mr in self.MRs])

    def getExpectedOutput(self, original_output):
        for mr in self.MRs:
            original_output = mr.getExpectedOutput(original_output)
        return original_output

    def getExpectedMatrix(self, original_input):
        followup_input = copy.deepcopy(original_input)
        for mr in self.MRs:
            followup_input = mr.getExpectedMatrix(followup_input)
        return followup_input

    def assertViolation(self, exp_output, followup_output):
        return self.MRs[-1].assertViolation(exp_output, followup_output)

def getCMRTestMR5List():
    mr_list = [[MR5(),MR1()],[MR5(),MR2()],[MR5(),MR3()],[MR5(),MR4()],[MR5(),MR6()]]
    cmr_list = []
    for cmr_c in mr_list:
        temp = CompositionMR()
        temp.setMRs(cmr_c)
        cmr_list.append(temp)
    return cmr_list

def getCMRPermutationsList(mr_list):
    cmr_list = []
    cmr_permutations = itertools.permutations(mr_list, 2)
    for cmr_p in cmr_permutations:
        temp = CompositionMR()
        temp.setMRs(list(cmr_p))
        cmr_list.append(temp)
    return cmr_list

def recordResult(file_name, mutants_list, mr_list):
    result = open("../results/"+file_name,"w")
    temp = [v+"\t" for v in mutants_list]
    temp.insert(0, "\t")
    temp.append("\n")
    for cmr in mr_list:
        temp.append("{}\t".format(cmr.name))
        for v in mutants_list:
            temp.append(str(cmr.table[v])+"\t")
        temp.append("\n")
    result.writelines(temp)
    result.close()

def MetamorphicTesting(executor, mutants_list, mr_list, test_case, num_of_samples):
    for mr in mr_list:
        table = dict(zip(mutants_list, [0]*len(mutants_list)))
        for i in range(num_of_samples):
            mr.setTestCase(test_case)
            mr.original_ts.setInputOutput("infile_{}".format(i), "outfile_{}".format(i),"outtree_{}".format(i))
            mr.original_ts.generateRandomTestcase()
            mr.setExecutor(executor)
            for v in mutants_list:
                executor.setVersion(v)
                mr.process()
                if mr.isViolate:
                    table[v] = table[v]+1
        mr.setKilledMutantsTable(table)

def testCMR():
    dna = Dnapars()
    num_of_samples = 1
    result_to_save_1= "CMR_1000_part1.result"
    result_to_save_2 = "CMR_1000_part2.result"
    mr_list = [MR1(),MR2(), MR3(), MR4(),MR6(), MR7()]
    mutants_list = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"]
    cmr_list_1 = getCMRPermutationsList(mr_list)
    cmr_list_2 = getCMRTestMR5List()
    MetamorphicTesting(dna, mutants_list, cmr_list_1, TestCase(), num_of_samples)
    recordResult(result_to_save_1, mutants_list, cmr_list_1)
    MetamorphicTesting(dna, mutants_list, cmr_list_2, TestCase_V1(), num_of_samples)
    recordResult(result_to_save_2, mutants_list, cmr_list_2)

def testSingleMR():
    ts_1 =TestCase()
    ts_2 = TestCase_V1()
    dna = Dnapars()
    num_of_samples = 1
    result_to_save_1 = "SMR_1000_part1.result"
    result_to_save_2 = "SMR_1000_part2.result"
    mr_list_1 = [MR1(),MR2(), MR3(), MR4(),MR6(), MR7()]
    mr_list_2 = [MR5()]
    mutants_list = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"]
    MetamorphicTesting(dna, mutants_list, mr_list_1, ts_1, num_of_samples)
    MetamorphicTesting(dna, mutants_list, mr_list_2, ts_2, num_of_samples)
    recordResult(result_to_save_1, mutants_list, mr_list_1)
    recordResult(result_to_save_2, mutants_list, mr_list_2)


def testSinglMRWithOneTestCase():
    ts =TestCase_V2()
    ts.setInputOutput("infile_{}".format("t"), "outfile_{}".format("t"),"outtree_{}".format("t"))
    ts.generateRandomTestcase()
    dna = Dnapars()
    cmr_list = [MR7()]
    mutants_list = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"]
    for cmr in cmr_list:
        table = dict(zip(mutants_list, [0]*len(mutants_list)))
        cmr.setTestCase(ts)
        cmr.setExecutor(dna)
        dna.setVersion("v0")
        cmr.process()
        if cmr.isViolate:
            table["v1"] = table["v1"]+1
        cmr.setKilledMutantsTable(table)


def testCMRWithOneTestCase():
    ts =TestCase_V2()
    ts.setInputOutput("infile_{}".format("t"), "outfile_{}".format("t"),"outtree_{}".format("t"))
    ts.generateRandomTestcase()
    dna = Dnapars()
    cmr1 = CompositionMR()
    cmr2 = CompositionMR()
    cmr1.setMRs([MR1(),MR7()])
    cmr2.setMRs([MR7(),MR1()])
    cmr_list = [cmr1,cmr2]
    mutants_list = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"]
    for cmr in cmr_list:
        table = dict(zip(mutants_list, [0]*len(mutants_list)))
        cmr.setTestCase(ts)
        cmr.setExecutor(dna)
        dna.setVersion("v1")
        cmr.process()
        if cmr.isViolate:
            table["v1"] = table["v1"]+1
        cmr.setKilledMutantsTable(table)


if __name__ == "__main__":
    myenv = MyEnv()
    myenv.CreateWorkingDirs()
    testSingleMR()
