import sys

def parse_file(input_file, numTrials, starterStringInFile):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    averageTotalTime = 0
    averageDataTransferWithOverhead = 0
    averageDataTransferWithoutOverhead = 0
    averageclassificationWithOverhead = 0
    averageclassificationWithoutOverhead = 0
    i = 0
    while i < len(lines):
        items = lines[i].split()
        if items[0] == starterStringInFile:
            print(str(lines[i]))
            averageTotalTime = 0
            averageDataTransferWithOverhead = 0
            averageDataTransferWithoutOverhead = 0
            averageclassificationWithOverhead = 0
            averageclassificationWithoutOverhead = 0
            i+=1
        elif int(items[0]) == numTrials:
            #do this last one and do next batch

            averageTotalTime += float(lines[i + 1].replace('\n', ''))
            averageDataTransferWithOverhead += float(lines[i + 2].replace('\n', ''))
            averageDataTransferWithoutOverhead += float(lines[i + 3].replace('\n', ''))
            averageclassificationWithOverhead += float(lines[i + 4].replace('\n', ''))
            averageclassificationWithoutOverhead += float(lines[i + 5].replace('\n', ''))

            averageTotalTime /= numTrials
            averageDataTransferWithOverhead /= numTrials
            averageDataTransferWithoutOverhead /= numTrials
            averageclassificationWithOverhead /= numTrials
            averageclassificationWithoutOverhead /= numTrials

            print(" Average Total Time: "+"{:.5f}".format(averageTotalTime))
            print(" Average Data Transfer with Overhead: " +"{:.5f}".format(averageDataTransferWithOverhead))
            print(" Average Data Transfer Without Overhead: " +"{:.5f}".format(averageDataTransferWithoutOverhead))
            print(" Average Classification With Overhead: " +"{:.5f}".format(averageclassificationWithOverhead))
            print(" Average Classification Without Overhead: " +"{:.5f}".format(averageclassificationWithoutOverhead)+'\n')
            averageTotalTime = 0
            averageDataTransferWithOverhead = 0
            averageDataTransferWithoutOverhead = 0
            averageclassificationWithOverhead = 0
            averageclassificationWithoutOverhead = 0
            i+=6
        else:
            averageTotalTime += float(lines[i+1].replace('\n', ''))
            averageDataTransferWithOverhead += float(lines[i+2].replace('\n', ''))
            averageDataTransferWithoutOverhead += float(lines[i+3].replace('\n', ''))
            averageclassificationWithOverhead += float(lines[i+4].replace('\n', ''))
            averageclassificationWithoutOverhead += float(lines[i+5].replace('\n', ''))
            i += 6

if __name__ == "__main__":


    if len(sys.argv) != 4:
        print("Parameters: File_To_Read, Num_Trials, Key_Word_On_Lines")
        exit(420)

    input_file = sys.argv[1]
    parse_file(input_file, int(sys.argv[2]), sys.argv[3])


