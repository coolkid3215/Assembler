# Isaac Morales

from InstructionSet import Opcode,OperandType,Registers,allowed

class Assembler:
#All the class variables we need
    def __init__(self):
        self.useful = []    #[lineNum,self.address,self.command,self.type])
        self.file = ''
        self.address = '0000'
        self.label = []
        self.error = []
        self.command = ''
        self.type = ''
        self.Atype = '--------'
        self.source = ' '
        self.dest = ' '
        self.B3 = ''
        self.values = []


        self.obFile = ['IsaacMorales00']
        self.orgs = []
        self.bytes = []
        self.unique = 'FF00AA55'

    def reader(self,fileName):      #Read the .s43 file line by line
        cutOut = fileName.find('.s43')
        listFile = open(fileName[:cutOut]+'.lst','w')
        listFile.write('Isaac Morales \t RNumber \n')
        sentence = ' '
        self.address = '0200'
        self.file = open(fileName, "r")
        lineNum = 1
        nextA = '0000'
        ocount = -1
        if self.file.mode == 'r':
            lineNum = 1
            for line in self.file:
                self.address = nextA    #next line's address
                self.command,self.type = self.OpcodeFinder(line)    #look at opcodes
                self.source,self.dest = self.CommandInfo(line)  #look at S-Reg and D-Reg
                self.source,self.dest,self.Atype,self.B3 = self.Addressing(self.source,self.dest)
                # print(lineNum,"\t", line)   # prints line by line
                punk = line
                code = self.encoder(lineNum)

                for word in line:

                    if word.isupper():
                        if "ORG" in line:   #use this to track addresses
                            ocount += 1
                            sentence = line
                            sentence = str(sentence)
                            before = sentence.find("0x")
                            nextA = sentence[before+2:before + 6]
                            # address = extracter(sentence)
                            # print(len(sentence))    #do something clever with this?
                            line = line.strip ('\t')
                            self.orgs.append([ocount,nextA])
                            break
                        elif "DB" in line:  #add 1
                            nextA = int(nextA ,16)
                            nextA += 1
                            nextA = hex(nextA)
                            nextA = str(nextA[2:].upper())
                            self.bytes.append([ocount,self.address])
                            # address = str(address)
                            break
                        elif "DW" in line:  #add 2
                            nextA = int(nextA,16)
                            nextA += 2
                            nextA = hex(nextA)
                            nextA = str(nextA[2:].upper())
                            self.bytes.append([ocount,self.address])                            # address = str(address)
                            break
                        elif "DS" in line:  #add next number
                            nextA = int(nextA,16)
                            nextA += int(self.DSfinder(line))
                            nextA = hex(nextA)
                            nextA = str(nextA[2:].upper())
                            self.bytes.append([ocount,self.address])
                            # address = str(address)
                            break
                        elif "$" in line: #calculate value
                            self.sizeDealer(line,lineNum)
                            break
                        elif self.Atype == 'IMM':   #immediate values
                            nextA = int(nextA,16)
                            nextA += 4
                            nextA = hex(nextA)
                            nextA = str(nextA[2:].upper())
                self.label.append([punk.strip(':'),self.address,lineNum])
                self.useful.append([lineNum,self.address,self.command,self.type,self.Atype,self.source,self.dest])
                print(lineNum, '\t',self.address,code, line)  #prints ORG then the address
                listFile.write(str(lineNum) + '\t' + self.address +'\t' +code + '\t' + line + '\n')
                lineNum += 1
        print('all orgs',self.orgs)
        print('all bytes',self.bytes)
        self.file.close()
        listFile.close()

    def tableMaker(self,fileName):  #creates label table
        cutOut = fileName.find('.s43')
        listFile = open(fileName[:cutOut]+'.lst','a')
        listFile.write('Label'+'\t'*12+ 'Value' + '\n')
        listFile.write('-----'*10+'\n')
        self.label.sort()
        for val in range(len(self.label)):
            for h in range(len(self.values)):

                if self.values[h][0] in self.label[val][0]:
                    self.label[val][1] = self.values[h][1]

                    break
            else:
                continue
        for column1 in range(len(self.label)):
            if self.label[column1][0][0] == ' ' or ';' in self.label[column1][0][0] or '\t' in self.label[column1][0][0:5]:
                # print(column1,'not valid')
                continue
            # else:

            else:       #error handling, illegal characters and duplicates
                lengthOf = len(self.label[column1][0][:30])
                if self.label[column1][0][:30].find(':') < 0:
                    fill = 30 - self.label[column1][0][:30].find(' ')
                else:
                    fill = 29 - self.label[column1][0][:30].find(':')
                if fill > 30:
                    fill = fill-30 + 5
                # print(fill)
                if lengthOf == 1 :
                    continue
                else:

                    sis = self.label[column1][0].find(' ')

                    for character in self.label[column1][0][:sis]:

                        if character in allowed:
                            continue
                        elif character == ':':
                            # character = character.replace(' ',':')
                            continue
                        else:
                            err = 'Illegal Character ' + str(character)+' '
                            self.error.append([self.label[column1][0][:sis],self.label[column1][2],err ])
                            # print('we->',character,'<-')
                            break
                    if self.label[column1][0][0] == '_':
                        self.error.append([self.label[column1][0][:sis],self.label[column1][2],'Ilegal First character' ])

                    for m in range(len(self.label)):
                        # self.label[column1][0].strip('\t')
                        if self.label[column1][0][:sis] == self.label[m][0][:sis] and column1 != m and self.label[column1][1] == self.label[m][1]:# or self.label[column1][1] != self.label[m][1]:
                            print(self.label[m][0])
                            self.error.append([self.label[m][0][:sis],self.label[m][2],' Duplicate '])
                            self.label[column1]= ['\t','\t']
                            # print('duplicate spotted')

                        else:
                            continue
                    space = self.label[column1][0].find(' ')
                    # print('here')
                    if len(self.error)> 0:
                        for m in range(len(self.error)):
                            if self.label[column1][0][:sis] in self.error[m][0]:
                                continue
                            else:
                                print( self.label[column1][0][:space],' '* fill,self.label[column1][1])
                                listFile.write(self.label[column1][0][:space]+' '* fill+self.label[column1][1]+'\n')
                                break
                    else:
                        print( self.label[column1][0][:space],' '* fill,self.label[column1][1])
                        listFile.write(self.label[column1][0][:space]+' '* fill+self.label[column1][1]+'\n')

        listFile.write( str(len(self.error)) + ' Error(s) found: \n')
        for i in range(len(self.error)):
            if i == len(self.error)-1:
                listFile.write(self.error[i][2] +self.error[i][0] + ' on line ' + str(self.error[i][1]) + '\n')
            else:
                listFile.write(self.error[i][2] +self.error[i][0] + ' on line ' + str(self.error[i][1]) + ', ')


        listFile.close()
        self.ObjectFile(fileName)

    def DSfinder(self,line):            #handles DS
        for DS in line.split():
            if DS.isdigit():
                # print('this is the DS val',DS)
                return DS
                break

    def OpcodeFinder(self,line):
        # words = line.split()
        # for words in line:
        for key in Opcode.keys():
            # print(key)
            if key in line:
                words = line.split()
                for i in words:
                    if key == i:
                        return i, OperandType[key]
                # break
            else:
                continue
        return ' ',' '

    def CommandInfo(self,line):     #looks at actual opcode in line and determines operand type
        Source  = ' '
        Destination = ' '
        for i in Opcode.keys():
            if i in line:
                start = line.find(i)
                space = line[start:].find(' ')
                if line.find(';') > -1:
                    end = line.find(';')
                    if end < start:
                        # print('here sis')   #there's a comment here
                        continue
                else:
                    end  = len(line)
                line = line[space:end]
                if i in line:
                        newstart = line.find(i)
                        line = line[newstart:]

                        pieces  = line.split()
                        if len(pieces) == 2:
                            # print('this should be a value', pieces[1])
                            Source = '----N/A'
                            Destination = pieces[1]
                        elif len(pieces) == 3:
                            # print('source', pieces[1],'destination', pieces[2])
                            Source = pieces[1]
                            Destination = pieces[2]
                        else:
                            Source  = ' '
                            Destination = ' '

                        # print('okayyyy'*9,'------->'*4,pieces)
                        # break
        return Source, Destination

    def Addressing(self,Source,Destination):        #deals with addresing information
        src = 'R0'
        dest = 'R0'
        As = 0
        Ad = 0
        Mode = ' '
        byte3 = ''
        for key in Registers.keys():    #find source register first
            if key in Source:
                src = key
                #register mode
                if src == Source:
                    As = 0
                #indexed mode
            elif '(' in Source or '&' in Source:
                As = 1
        #FInd a way to include symbolic mode
            #indirect register mode
            elif '@' in Source:
                As = 2
                #indirect auto increment
                if '+' in Source:
                    As = 3
            #immediate mode
            elif '#' in Source:
                As = 4


            # else:
                # continue

            if key in Destination:
                dest = key
                if dest == Destination:
                    Ad = 0
                #indexed mode
            elif '(' in Destination:
                Ad = 1
            #find a way to include symbolic
            #Absolute
            elif '&' in Destination:
                Ad = 2
            else:
                continue
            # else:
            #     continue
        if As == 0:
            if Ad == 0:
                Mode = 'REG'
                if self.command.find('.b') > -1:
                    byte3 = '0100'
                else:
                    byte3 = '0000'
            elif Ad == 1:
                Mode = 'IDX'
                if self.command.find('.b') > -1:
                    byte3 = '1100'
                else:
                    byte3 = '1000'
            elif Ad == 2:
                Mode = 'ABS'
                if self.command.find('.b') > -1:
                    byte3 = '1100'
                else:
                    byte3 = '1000'

        elif As == 1:
            if Ad == 0:
                Mode = 'IDX'
                if self.command.find('.b') > -1:
                    byte3 = '0101'
                else:
                    byte3 = '0001'
            elif Ad == 1:
                Mode = 'IDX'
                if self.command.find('.b') > -1:
                    byte3 = '1101'
                else:
                    byte3 = '1001'
            elif Ad == 2:
                Mode = 'ABS'
                if self.command.find('.b') > -1:
                    byte3 = '1101'
                else:
                    byte3 = '1001'

        elif As == 2:
            Mode = 'I REG'
            if self.command.find('.b') > -1:
                byte3 = '0110'
            else:
                byte3 = '0010'

        elif As == 3:
            Mode = 'IA REG'
            if self.command.find('.b') > -1:
                byte3 = '0111'
            else:
                byte3 = '0011'

        elif As == 4:
            Mode = 'IMM'
            if self.command.find('.b') > -1:
                byte3 = '0111'
            else:
                byte3 = '0011'
            src = 'R0'
            if Destination == 'SP':
                dest = 'R1'
        else:
            Mode = 'unknown'
        if self.command == 'inc' or self.command == 'dec':
            byte3 = '0001'
            src = 'R3'
        return src,dest,Mode,byte3
        # print('Source is',src)
        # print('Destination is', dest)


    def encoder (self,lineNum):     #creates bit pattern. doesnt work with immediate mode
        code = '\t'
        if self.type == 'Double':
            # print(Opcode[self.command],Registers[self.source],str(hex(int(self.B3,2)))[2:],Registers[self.dest])
            code = str(hex(int(self.B3,2)))[2:]+Registers[self.dest] + Opcode[self.command]+Registers[self.source]

        # elif self.type == 'JMP':
            # print('branch type thing detected')
            # print(Opcode[self.command])
        return code
    def sizeDealer (self,line,lineNum): #deals with $

        math = line.find('$')
        item = line[:math]
        item = item.split()

        ending = line.find(';')
        if ending != -1:
            calc = line[math:ending]
            # print(calc)
            calc = calc.split()
            if calc[1] == '-':
                for n in range(len(self.label)):
                    for i in range(len(self.label[n])):
                        if calc[2] in self.label[n][0]:
                            # print(self.label[n][1])
                            subThis = '0x0' + self.label[n][1]
                            subThis = int(subThis,16)
                            # subThis = hex(subThis)
                            fromThis = '0x0' + self.address
                            fromThis = int(fromThis,16)
                            # fromThis = hex(fromThis)
                            result = fromThis - subThis
                            # print(hex(fromThis),'-',hex(subThis))
                            # print(result)
                            lab = self.label[n][0].split()
                            self.values.append([item[0],str(result)])
                            # self.label[n][1] = str(result)
                            break
            if calc[1] == '+':
                for n in range(len(self.label)):
                    for i in range(len(self.label[n])):
                        if calc[2] in self.label[n][0]:
                            # print(self.label[n][1])
                            subThis = '0x0' + self.label[n][1]
                            subThis = int(subThis,16)
                            # subThis = hex(subThis)
                            fromThis = '0x0' + self.address
                            fromThis = int(fromThis,16)
                            # fromThis = hex(fromThis)
                            result = fromThis + subThis
                            # print(hex(fromThis),'+',hex(subThis))
                            # print(result)
                            lab = self.label[n][0].split()
                            self.values.append([item[0],str(result)])
                            # self.label[n][1] = str(result)
                            break

        else:
            calc = line[math:]
            calc = calc.split()
            if calc[1] == '-':
                for n in range(len(self.label)):
                    for i in range(len(self.label[n])):
                        if calc[2] in self.label[n][0]:
                            # print(self.label[n][1])
                            subThis = '0x0' + self.label[n][1]
                            subThis = int(subThis,16)
                            # subThis = hex(subThis)
                            fromThis = '0x0' + self.address
                            fromThis = int(fromThis,16)
                            # fromThis = hex(fromThis)
                            result = fromThis - subThis
                            # print(hex(fromThis),'-',hex(subThis))
                            # print(result)
                            lab = self.label[n][0].split()
                            self.values.append([item[0],str(result)])
                            # self.label[n][1] = str(result)
                            break
            if calc[1] == '+':
                for n in range(len(self.label)):
                    for i in range(len(self.label[n])):
                        if calc[2] in self.label[n][0]:
                            # print(self.label[n][1])
                            subThis = '0x0' + self.label[n][1]
                            subThis = int(subThis,16)
                            # subThis = hex(subThis)
                            fromThis = '0x0' + self.address
                            fromThis = int(fromThis,16)
                            # fromThis = hex(fromThis)
                            result = fromThis + subThis
                            # print(hex(fromThis),'+',hex(subThis))
                            # print(result)
                            lab = self.label[n][0].split()
                            self.values.append([item[0],str(result)])
                            # self.label[n][1] = str(result)
                            break
#building the object file
    def ObjectFile(self,fileName):  #creates object file
        print(len(self.error))
        if len(self.error) <= 0:
            cutOut = fileName.find('.s43')
            OF = open(fileName[:cutOut]+'.txt','w')
            size = '0000'

            self.obFile.append(self.unique)
            for o in range(len(self.orgs)):
                self.obFile.append(self.orgs[o][1])
                for i in range(len(self.bytes)-1):
                    if self.bytes[i][0] == self.orgs[o][0] and self.bytes[i][0] < self.bytes[i+1][0] and i <len(self.bytes):
                         size = '0x0'+ str(self.bytes[i][1])
                         size = int(size,16)
                         buff = '0x0' + str(self.orgs[o][1])
                         buff = int(buff,16)
                         size = size - buff
                         size = hex(size)
                         length = len(size)
                         if length < 6:
                             size = ('0' * (6-length)) + size[2:]
                         else:
                             size = size[2:]
                         print(size)
                    else:
                        size = '0000'
                        continue
                self.obFile.append(size)

                for b in range(len(self.bytes)):
                    if self.bytes[b][0] == self.orgs[o][0]:
                        self.obFile.append(self.bytes[b][1])
                    else:
                        continue
                self.obFile.append(self.unique)

            print(self.obFile)
            for object in range(len(self.obFile)):
                OF.write(self.obFile[object])
            OF.close()
        else:
            print('there are errors in this file, so not object file was created.')
