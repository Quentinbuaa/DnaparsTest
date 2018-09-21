from MRs import *
from TestCase import *


class MetamorphicTesting:
    def __init__(self):
        self.max_combination = 5
        self.executor = Dnapars()
        self.mutants_list = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"]

    def getCMRTestMR5List(self):
        mr_list = [[MR5(),MR1()],[MR5(),MR2()],[MR5(),MR3()],[MR5(),MR4()],[MR5(),MR6()]]
        cmr_list = []
        for cmr_c in mr_list:
            temp = CompositionMR()
            temp.setMRs(cmr_c)
            cmr_list.append(temp)
        return cmr_list

    def getCMRPermutationsList(self,mr_list):
        cmr_list = []
        for num_combination in range(2, self.max_combination):
            cmr_permutations = itertools.permutations(mr_list, num_combination)
            for cmr_p in cmr_permutations:
                temp = CompositionMR()
                temp.setMRs(list(cmr_p))
                cmr_list.append(temp)
        return cmr_list

    def recordResult(self,record_file_name, mr_list):
        result = open("../results/"+record_file_name,"w")
        temp = [v+"\t" for v in self.mutants_list]
        temp.insert(0, "\t")
        temp.append("\n")
        for cmr in mr_list:
            temp.append("{}\t".format(cmr.name))
            for v in self.mutants_list:
                temp.append(str(cmr.table[v])+"\t")
            temp.append("\n")
        result.writelines(temp)
        result.close()

    def SetTestCases(self, num_of_samples):
        self.list_ts_type_1 = []
        self.list_ts_type_2 = []
        for i in range(num_of_samples):
            test_case_type_1 = TestCase()
            test_case_type_2 = TestCase_V1()
            test_case_type_1.setInputOutput("infile_{}".format(i), "outfile_{}".format(i),"outtree_{}".format(i))
            test_case_type_1.generateRandomTestcase()
            test_case_type_2.setInputOutput("infile_{}".format(i), "outfile_{}".format(i),"outtree_{}".format(i))
            test_case_type_2.generateRandomTestcase()
            self.list_ts_type_1.append(test_case_type_1)
            self.list_ts_type_2.append(test_case_type_2)

    def MetamorphicTesting(self, mr_list, list_of_ts):
        for mr in mr_list:
            table = dict(zip(self.mutants_list, [0]*len(self.mutants_list)))
            mr.setExecutor(self.executor)
            for ts in list_of_ts:
                mr.setTestCase(copy.deepcopy(ts))
                for v in self.mutants_list:
                    self.executor.setVersion(v)
                    mr.process()
                    if mr.isViolate:
                        table[v] = table[v]+1
            mr.setKilledMutantsTable(table)

    def testCMR(self):
        result_to_save_1= "CMR_1000_part1.result"
        result_to_save_2 = "CMR_1000_part2.result"
        mr_list = [MR1(),MR2(), MR3(), MR4(),MR6()]
        cmr_list_1 = self.getCMRPermutationsList(mr_list)
        cmr_list_2 = self.getCMRTestMR5List()
        self.MetamorphicTesting(cmr_list_1, self.list_ts_type_1)
        self.recordResult(result_to_save_1, cmr_list_1)
        self.MetamorphicTesting(cmr_list_2, self.list_ts_type_2)
        self.recordResult(result_to_save_2, cmr_list_2)

    def testSingleMR(self):
        result_to_save_1 = "SMR_1000_part1.result"
        result_to_save_2 = "SMR_1000_part2.result"
        mr_list_1 = [MR1(),MR2(), MR3(), MR4(),MR6()]
        mr_list_2 = [MR5()]
        self.MetamorphicTesting(mr_list_1, self.list_ts_type_1)
        self.MetamorphicTesting(mr_list_2, self.list_ts_type_2)
        self.recordResult(result_to_save_1, mr_list_1)
        self.recordResult(result_to_save_2, mr_list_2)


if __name__ == "__main__":
    myenv = MyEnv()
    myenv.CreateWorkingDirs()
    mt = MetamorphicTesting()
    mt.SetTestCases(3)
    mt.testSingleMR()
    mt.testCMR()

