"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list2 = list(list1)  
    if len(list2) <= 1:  
        return  list2  
    dummy_a = 0  
    dummy_b = 1      
      
    while dummy_a < len(list2) and dummy_b < len(list2):  
        if list2[dummy_a] != list2[dummy_b]:  
            list2[dummy_a+1] = list2[dummy_b]  
            dummy_a += 1  
            dummy_b += 1  
        else:  
            dummy_b += 1  
    return list2[0:dummy_a+1]

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    dummy_a = 0  
    dummy_b = 0  
    new_list = [];  
    while dummy_a < len(list1) and dummy_b < len(list2):  
        if list1[dummy_a]==list2[dummy_b]:  
            new_list.append(list1[dummy_a])  
            dummy_a += 1;  
            dummy_b += 1;  
        elif list1[dummy_a]<list2[dummy_b]:  
            dummy_a += 1  
        else:  
            dummy_b += 1  
    return new_list 
   

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    new_list = []  
    dummy_a = 0  
    dummy_b = 0 
    new_list = [];  
    while dummy_a < len(list1) and dummy_b < len(list2):  
        if list1[dummy_a] <= list2[dummy_b]:  
            new_list.append(list1[dummy_a])  
            dummy_a += 1  
        else:  
            new_list.append(list2[dummy_b])  
            dummy_b += 1  
    while dummy_a < len(list1):  
        new_list.append(list1[dummy_a])  
        dummy_a += 1  
    while dummy_b < len(list2):  
        new_list.append(list2[dummy_b])  
        dummy_b += 1          
    return new_list
    
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    sorted_list = []  
    if len(list1) <= 1:  
        return list1  
    mid = (len(list1)-1)//2   
    list2 = merge_sort(list1[:mid+1])   
    #mid = (len(list1)-1)//2 and here is   
    #merge_sort(list1[:mid]) then there is an infinite loop,   
    #imagine the case where list1=[3,4], list1[:0] and   
    #list1[0:]. It will start an infinite loop.  
    list_new = merge_sort(list1[mid+1:])  
    sorted_list = merge(list2,list_new)      
    return sorted_list  
    

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:  
        return [""]
    starting_letter = word[0:1]  
    result_rem = gen_all_strings(word[1:])  
    result_rem_copy = list(result_rem)  
    for dummy_i in result_rem_copy:  
        for index in range(len(dummy_i)): 
            new_word = dummy_i[:index] + starting_letter + dummy_i[index:]  
            result_rem.append(new_word)  
        result_rem.append(dummy_i + starting_letter)  
    return result_rem 


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    string_result = []  
    url = codeskulptor.file2url(filename)  
    netfile = urllib2.urlopen(url)  
    for line in netfile.readlines():  
        string_result.append(line[:-1])  
    return string_result
def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

#Uncomment when you are ready to try the game
run()

    
    
