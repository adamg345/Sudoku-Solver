import pandas as pd
import numpy as np
import math as m

#CSV file name of sudoku board
CSV_FILE = 'sudokuboard4.csv'

#Row an column names for the dataframe
col_names = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')
row_names = range(1,10)

#Class used for a particular square
class square:
    def __init__(self, val, col, row):
        self.val = val
        self.col = col
        self.row = row
        self.sqrNum = (int((ord(col)-65)/3)+1) + (3*int((row-1)/3))
        self.idx = (col, row)

    def returnAttr(sqr):
        return([sqr.val, (sqr.col, sqr.row), sqr.sqrNum])
#---

#Makes sure that mistakes are not being made. If a number appears more than once in a row/column/square, it raises an error
def errorChecker(list0):
    for i in range(1,10):
        if list0.count(i) > 1:
            print(df)
            raise TypeError("Program is making a mistake!!")
#-----

#Returns a list of DataFrame indices for given row/col/sqr1/sqr2
def getIndicies(type, idx):
    idx_list = []

    #If it's a row, is sets the idx_list with appropriate indices and sets orientation to 'H' for horizontal 
    if(type == 'row'):
        for col in col_names:
            idx_list.append((col, idx))

    #If it's a column, is sets the idx_list with appropriate indices and sets orientation to 'V' for vertical 
    elif(type == 'col'):
        for row in row_names:
            idx_list.append((idx, row))

    #If it's sqr1, it's a 3x3 being observed horizontally. It sets idx_list with appropriate indices and sets orientation to 'H'. 
    elif(type == 'sqr1'):
        for i in range(1,10):
            col = chr(int(65 + 3*((idx-1) % 3) + ((i-1) % 3)))
            row = int(3*int((idx-1)/3) + int((i-1)/3) + 1)

            idx_list.append((col, row))

    #If it's sqr2, it's a 3x3 being observed vertically. It sets idx_list with appropriate indices and sets orientation to 'V'.
    elif(type == 'sqr2'):
        for i in range(1,10):
            col = chr(int(65 + 3*((idx-1) % 3) + int((i-1)/3)))
            row = int(3*int((idx-1)/3) + ((i-1) % 3) + 1)
            idx_list.append((col, row))

    return idx_list
#-----

#Checks for strings that have been narrowed down to one number and converts them to integers. It also converts np.int64 to int.
def updateInt(list0):
    for i,el in enumerate(list0):        
        if(isinstance(el, str)):
            if(len(el) == 1):
                list0[i] = int(el)
        elif(isinstance(el, np.int64)):
            list0[i] = int(el)
        
    return list0
#-----

#Removes any integers that appear in a row/column/square from the strings. 
#Ex: If 5 appears in a row and another square in that same row contains the string '123456', it will change it to "12346"
def updateStr(list0):
    
    #Creates list containing all numbers that solved in list0 (exist as an int in list0)
    numbers = [str(i) for i in range(1,10) if i in list0]
    
    for i,el in enumerate(list0):
        if(isinstance(el, str)):
            for num in numbers:
                list0[i] = list0[i].replace(num, '')

    return list0
#-----

#Returns a list with the element at every possible location that a particular number can appear in a row/col/sqr
def checkOcc(list0, num):
    str_elms, indicies = [], []
    for i, el in enumerate(list0):
        if str(num) in str(el):
            str_elms.append(el)
            indicies.append(i)

    count = len(str_elms)

    return str_elms, indicies, count

#---

#Checks a row/column/square to see how many possible locations there are where a number can appear, for each number 1-9.
#If there's only 1 possible location, it'll set the value at that location to that number (int).
#Ex: If a row is ["23", 9, "23", 1, "78", "78", "45", "45", "456"], it'll change it to ["23", 9, "23", 1, "78", "78", "45", "45", 6]
def checkNum(list0):
        #List of numbers as strings from 1 to 9, inclusive
    numbers = [str(i) for i in range(1,10)]

    #Creates an empty list for any elements in a row/column/square that are a string and not a determined integer
    str_elms = []
    
    #Removes any numbers from numbers list that are already in the row/col/square; Adds any string elements to str_elms list
    for i in list0:
        if(isinstance(i, int) or isinstance(i, np.int64)):
            numbers.remove(str(i))
        else:
            str_elms.append(i)

    for num in numbers:
        #Creates a list that contains all string elements where that number can possibly appear
        pos_str = [str0 for str0 in str_elms if num in str0]

        #The number of possible locations in the row/column/square where that number can possibly appear
        count = len(pos_str)

        #If there's only one place in the row/col/sqr where that particular number can appear, it'll set the value at that location to the number
        if(count == 1):
            list0[list0.index(pos_str[0])] = int(num)

    return list0
#-----

#This class is used for making objects that consist of up to three consecutive squares in the same 3x3 and the same row/column
class groupObj:
    def __init__(self, str1, str2, num):
        #Creates objects for each individual square in the group
        self.str1 = str1
        self.str2 = str2
        self.num = num
        
        #Determines whether the orientation is horizontal or vertical, and determines the row/col index from that
        if(self.str1.row == self.str2.row):
            self.orientation = 'H'
            self.rowcolidx = self.str1.row
        else:
            self.orientation = 'V'
            self.rowcolidx = self.str1.col

        self.sqrNum = self.str1.sqrNum

        self.allIndicies = []

    def returnAttr(group):
        return([group.str1.returnAttr(), group.str2.returnAttr(), group.orientation], group.num, group.rowcolidx, group.sqrNum, group.allIndicies)
#---

#
def checkGroup(list0, type, idx):
    numbers = [str(i) for i in range(1,10)]
    tests = []

    idx_list = getIndicies(type, idx)
    #
    for num in numbers:
        temp, strgs = [], []
        #Iterates over each element in the row/col/sqr
        for i, el in enumerate(list0):
            
            temp.append(int(num in str(el)))
            if(num in str(el)):
                strg0 = tuple([el] + list(idx_list[i]))
                strgs.append(square(*strg0))
            
        #Continues if the number occurs more than once.
        if(sum(temp) > 1):
            if((sum(temp) == 2) and sum([int(not(not sum(temp[:3]))), int(not(not sum(temp[3:6]))), int(not(not sum(temp[6:9])))]) == 1):
                
                group = groupObj(*strgs, num)
                tests.append(group)

    return list0, tests
#-----

#Checks for instances such as ['123', '123', '123', 4, '56', '56', '5678', '56789', '789'], where because there are 2 locations where only 5 or 6 can appear, it cannot appear anywhere else.
#The updated list would look like ['123', '123', '123', 4, '56', '56', '78', '789', '789']
def checkGroup2(list0):
    nums, groups = set(), set()
    for el in list0:
        if(isinstance(el, str)):   
            n, n_occur = len(el), list0.count(el)
            if(n == n_occur and n > 1):
                nums = nums | set((el))
                groups.add(el)

    #Checks to see if there are any groups at all so it doesn't waste time.
    if(len(groups)):
        for i, el in enumerate(list0):
            #Checks to make sure element is a string and is not one of the groups
            if((el not in groups) and isinstance(el, str)):
                for d in nums:
                    el = el.replace(d, "")
                list0[i] = el

    return list0
#-----

#
def checkGroup3(list0):
    loclist, affectGrpList = [], []
    for i in row_names:
        str_elms, indicies, count = checkOcc(list0, i)
        loclist.append((str_elms, indicies, count))
            
    for i in range(len(loclist)):
        groupList = list(checkOcc(loclist, loclist[i]))
        groupList[0] = groupList[0][0]
        groupList[1] = ''.join([str(t+1) for t in groupList[1]])
        if((groupList[0][-1] == groupList[-1]) and (groupList not in affectGrpList)):
            affectGrpList.append(groupList)

    for el in affectGrpList:
        indicies = el[0][1]
        newStr = el[1]
        for i in indicies:
            list0[i] = newStr

    return list0
#-----

#If two or more objects in a list have identical attributes, it deletes all objects with that set of attributes from the list
def removeDuplicates(allTests):
    testAttr = [t.returnAttr() for t in allTests]
    filteredTests = allTests

    #For each test, if there's another tests that has identical attributes, it filters it out from the filtered list
    for test in allTests:
        if(testAttr.count(test.returnAttr()) > 1):
            filteredTests.remove(test)
    #print(testAttr)       
    return filteredTests
#-----

#Reads CSV file
df = pd.read_csv(CSV_FILE, names = col_names , nrows = 9)
#Sets index (row names) to 1 thru 9
df.index = row_names

print(df)

#Replaces any NaN values w/'123456789' and makes every predetermined value an int. It does this by replacing NaN values w/0 and then replacing 0 w/'123456789'
df.fillna(0, inplace = True)
df = df.astype(int).replace(0, '123456789')

def main():
    n_iter = 12
    for k in range(n_iter):
        rowtests, coltests, sqrtests1, sqrtests2 = ([],)*4
        #Rows
        for i in row_names:
            row = df.loc[i].to_list()

            #Updates string to contain any possible numbers
            row = updateStr(row)
            errorChecker(row)

            #Checks if there is only one possible place a number can appear
            row = checkNum(row)
            errorChecker(row)

            #
            row = checkGroup2(row)

            #
            row = checkGroup3(row)

            #Makes any single digit strings integers
            row = updateInt(row)
            errorChecker(row)

            #Updates the dataframe
            df.loc[i] = row

            #
            row, tests = checkGroup(row, 'row', i)

            #
            if(tests):
                rowtests = rowtests + tests
        #---

        #Columns
        for i in col_names:
            col = df[i].to_list()

            #Updates string to contain any possible numbers
            col = updateStr(col)
            errorChecker(col)

            #Checks if there is only one possible place a number can appear
            col = checkNum(col)
            errorChecker(col)

            #
            col = checkGroup2(col)

            #
            col = checkGroup3(col)
            
            #Makes any single digit strings integers
            col = updateInt(col)
            errorChecker(col)

            #Updates the dataframe
            df[i] = col

            #
            col, tests = checkGroup(col, 'col', i)           
            
            if(tests):
                coltests = coltests + tests
        #---

        #3 x 3 squares
        for i in range(0,9,3):
            for j in range(0,9,3):
                list0 = df.loc[i+1][j:j+3].to_list() + df.loc[i+2][j:j+3].to_list() + df.loc[i+3][j:j+3].to_list()
                #print(list0)

                #Updates string to contain any possible numbers
                list0 = updateStr(list0)
                errorChecker(list0)

                #Checks if there is only one possible place a number can appear
                list0 = checkNum(list0)
                errorChecker(list0)
                            
                #
                list0 = checkGroup2(list0)
                
                #
                list0 = checkGroup3(list0)
                list0 = updateInt(list0)
                
                #Makes any single digit strings integers
                list0 = updateInt(list0)
                errorChecker(list0)

                #Updates the dataframe
                df.iloc[i, [j, j+1, j+2]] = list0[:3]
                df.iloc[i+1, [j, j+1, j+2]] = list0[3:6]
                df.iloc[i+2, [j, j+1, j+2]] = list0[6:]

                #
                list0, tests = checkGroup(list0, 'sqr1', (i+1) + (j/3))
                
                if(tests):
                    sqrtests1 = sqrtests1 + tests

                list2 = [list0[0],list0[3],list0[6],list0[1],list0[4],list0[7],list0[2],list0[5],list0[8]]
                list2, tests = checkGroup(list2, 'sqr2', (i+1) + (j/3))
                
                if(tests):
                    sqrtests2 = sqrtests2 + tests
        #---
                
    alltests = rowtests + coltests + sqrtests1 + sqrtests2

    #If there are duplicates of a group, it removes both instances of that group
    nonduplicates = removeDuplicates(alltests)

    for group in nonduplicates:
        #If this code doesn't work, it's because the puzzle has been solved so it will end the program.
        #try:
            #group = nonduplicates[0]
        #except:
            #print(df)
            #print("DONE")
            #exit()

        #indicies of the 2 locations in question
        indiciesX = [group.str1.idx, group.str2.idx]

        #Orientation will affect whether it's row or col and what type of 3x3 square
        if(group.orientation == 'H'):
            rowcol, sqr = 'row', 'sqr1'   
        elif(group.orientation == 'V'):
            rowcol, sqr = 'col', 'sqr2'
            
        #Gets indicies off all locations in the affected row/col and square
        rowcol_indicies = getIndicies(rowcol, group.rowcolidx)
        sqr_indicies = getIndicies(sqr, group.sqrNum)

        #Combines both the row/col and sqr indicies into a set (removes duplicates along the way)
        indicies = set(rowcol_indicies + sqr_indicies)

        #Removes the indicies of the 2 locations in question from the list
        for idx_X in indiciesX:
            indicies.remove(idx_X)

        if(group.orientation == 'H'):
            pass#print(rowcol+' '+sqr+' '+str(group.rowcolidx)+' '+str(group.sqrNum))

        for i in indicies:
            col, row = i
            df.loc[row, col] = str(df.loc[row, col]).replace(group.num, '')

#----------

dforig = df.copy()

for i in range(11):
    main()



print(df)
print(df['H'][9]/2)