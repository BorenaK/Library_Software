#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:04:38 2021

@author: borenak
"""

#importing libraries

import csv
import datetime


'''
Reading the csv file into a dictionary
Key is the unique number of each book 
Value contains information about the book stored as a sub dictionary with: 
Title, Author, Genre, Subgenre, Publisher as keys and the specific information as values
Using try, except, finally for error handling
'''

try:
    with open('books.csv', mode = 'r', encoding = 'utf-8') as file:      #using 'utf-8' to encode the file
        csvFile = csv.reader(file)
        #print(csvFile)
        
        rowCount = 0
        bookDictionary = {}
        
        for row in csvFile:
            #print(row)
            if rowCount == 0:
                #reads the heading
                heading = row        
                #print(heading)
                
                rowCount += 1
            else:
                #read and store the content in the dictionary
                bookDictionary[row[0]] = { 
                                          heading[1]:row[1],
                                          heading[2]:row[2],
                                          heading[3]:row[3],
                                          heading[4]:row[4],
                                          heading[5]:row[5],
                                         }
                rowCount += 1
        print(bookDictionary)
            
except:
    print('File could not be opened.')
    
finally:
    file.close()
    
    
    
    
#convert the numerical data to dates

def formatDate(refValue, dateValue):
    '''
    Function converts Microsoft epoch formatted dates 
    return: readable date as Year-Month-Day 
    '''
    #considering epoch date to be 1900-01-01
    formatRef = datetime.datetime.strptime(refValue, "%Y-%m-%d")
    newDate = (formatRef + datetime.timedelta(days=int(dateValue))).strftime("%Y-%m-%d")
    return newDate




'''
Opening and reading in the bookloans.csv file 
Excluding all rows where the unique book id is > 120 
Excluding the rows where the return date is 0
Using try, except, finally for error handling
'''
# open the file bookloans.csv
try:
    # open the file 
    with open('bookloans.csv', mode = 'r', encoding = 'utf-8') as file:       #using 'utf-8' to encode
        csvFile = csv.reader(file)
        #print(csvFile)

        #initialize the variables to store the data
        date_of_loan = []
        date_of_return = []
        memberId = []
        bookId = []

        #read the data
        for row in csvFile:
            #changing first element into '1'
            if row[0].isdigit() == False:           
                row[0] = '1'
                # excluding elements where return_date is 0
                # excluding elements where the bookId > 120
            if row[3] != 0 and int(row[0]) < 121:
            
                if row[0] != 0:                           #reading in rows 0 and 1
                    bookId += [row[0]]
                if row[1] != 0:
                    memberId = [row[1]]
                if row[2] != 0:
                #changing epoch into dates
                    date_of_loan += [formatDate('1900-01-01', row[2])]   #append the formatDate function
                else:
                    date_of_loan += ['Nan']
                if row[3] != 0:
                    date_of_return += [formatDate('1900-01-01', row[3])]
                else:
                    date_of_return += ['Nan']


        
except:
    print('File could not be opened.')
    
finally:
    file.close()

print(bookId)
print(memberId)
print(date_of_loan)
print(date_of_return)
#print(len(bookId)) 





'''
Extracts years 2019 from date_of_loan
appends to the empty list "index"
'''

index = []

#extract years 2019 and position 
for i in range(0,len(date_of_loan)):
    if int(date_of_loan[i][0:4]) == 2019:         #extract years 2019
        index.append(i)
        
#print(len(index), index)



'''
Extracts books loaned in 2019
Counts occurency for each book
'''

bookIdSelected = []

for element in index:
    bookIdSelected.append(bookId[element])    #extract books loaned in 2019
    
counts = []    
for i in range(1,121):
    count = bookIdSelected.count(str(i))    # counted books for each number
    counts.append(count)
    
#print(counts)


'''
Creates a new dictionary with the 
Key: Author name and title as tuple
Value: frequency of book loan
'''

#create new dict with name&title as key and number of times as values
#sort the keys
sortedDictionary = {}
for i in range(0, len(counts)):
    author = bookDictionary[str(i+1)]['Author']             #i starts from 0, (i+1) to start from 1 
    title = bookDictionary[str(i+1)]['Title']               #author and title
    sortedDictionary[(author, title)] = counts[i]           #author, title as key tuple - counts as value

#print(sortedDictionary)


'''
Sorts the keys of the dictionary based on their values in reverse order
Builds a new sorted dictionary 
Prints the sorted dictionary
'''

#sort the keys of sortedDictionary based on values
sortedKeys = sorted(sortedDictionary, key = sortedDictionary.get , reverse = False )
#print(sortedKeys)

#create new dictionary sDictionary
#go through sortedKeys and assign the coresponding value from sortedDictionary
sDictionary = {}
for key in sortedKeys:
    sDictionary[key] = sortedDictionary[key]              
    
print(sDictionary)


    

#bookIdSelected = bookId[index]
#print(len(index), len(bookIdSelected))
#print(bookIdSelected)



def popGenres(sDictionary):
    '''
    Creates dicitonaries for the most popular genres and subgenres based on the sorted sDictionary from year 2019
    returns: genres - the dictionary for the most popular genres
             subgenres - dictionary for the most popular subgenres
    '''
    genres = []
    subgenres = []
    
    for key, value in sDictionary.items():
        genres.append(value['Genre'])
        subgenres.append(value['SubGenre'])

    countDictionary = {}                             #genre dictionary
    for element in genres:
        if element not in countDictionary.keys():
            countDictionary[element] = 1             #create key and assign on to the value
        else:
            countDictionary[element] += 1            #adds 1 to the value if key is already there
    
    countDictionarySub = {}                          #subgenre dictionary
    for element in subgenres:
        if element not in countDictionarySub.keys(): # works as above for genres
            countDictionarySub[element] = 1
        else:
            countDictionarySub[element] += 1
    

    return countDictionary, countDictionarySub   

genres, subgenres = popGenres(bookDictionaryNew)       #call the function

print("The most popular genres:", genres)
print("The most popular subgenres:", subgenres)



def days_between(d1, d2):                                
    
    '''
    Calculates the average of the time each book is on loan
    the average late period for a loan period of 14 days
    the percentage of users returning a book late
    '''
    
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)                                #subtract days to find the difference
#days_between(date_of_return[0], date_of_loan[0])

#create a dictionary dayDifferences
dayDifferences = {}
for i in range(0, len(date_of_return)):                                      #for loop on all date of returns
    if int(date_of_loan[i][0:4]) == 2019 and int(date_of_return[i][0:4]) == 2019:     #if both are in 2019
        days = days_between(date_of_return[i], date_of_loan[i])                     #calculates the difference 
        if bookId[i] not in dayDifferences.keys():                           #starts filling out the dictionary
            dayDifferences[bookId[i]] = [days]                #creates dict with the book id as key, value the first difference
        else:
            dayDifferences[bookId[i]] += [days]               #adds the new difference
#print(dayDifferences)

    
for key, v in dayDifferences.items():        #iterates through dictionary
    print("Book id", key)                    #prints out book id
    lower = []
    upper = []                               #creates two new lists 
    for element in v:                        #fills out the lists for differences of less and more than 14 days
        if element <= 14:
            lower.append(element)
        else:
            upper.append(element)
    if len(lower) != 0:                      #to avoid zero division error
        averageLower = sum(lower)/len(lower)        #calculates the average of all elements of the list lower
        print("Average less than 14 days", round(averageLower,2))
    if len(upper) != 0:
        averageUpper = sum(upper)/len(upper)
        print("Average more than 14 days", round(averageUpper,2))
    if len(upper) != 0 and len(v) != 0:              #calculates the percentage of the book being returned late
        percentage = len(upper)/len(v) * 100
        print("Percentage of the book being returned late", round(percentage,2))  #rounded for better readability





