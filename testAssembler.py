from Assembler import Assembler
import os

#ISaac Morales R11453173
def Menu():
    print('hello choose a file to create a list file for \n')
    fileName =[]
    for root,dirs,files in os.walk("."):
        index = 0
        for fname in files:
            if fname.endswith('.s43'):
                fileName.append(fname)
                print(index,':',fname)
                index += 1
    choice = int(input('\n '))
    thing = fileName[choice]

    return thing


def main():
    #Display a menu of all the .s43 files in the current directory
    thing = Menu()
    ChosenFile = Assembler()
    ChosenFile.reader(thing)
    ChosenFile.tableMaker(thing)

if __name__ == '__main__':
    main()
