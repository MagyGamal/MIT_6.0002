# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:49:56 2019

@author: Magy Gamal
"""

def sum_digits(n):
    """ Given a number, this function gets the sum of its digits."""
    #base case
    if n==0:
        return 0
    #returns last digit then calls the function again with the number after removing that last digit then sums
    else:
        return n%10+sum_digits(int(n/10))
print("output=",sum_digits(687))
print("supposed output=21")
print("output=",sum_digits(12))
print("supposed output=3")

def ispalendrome(n):
    """A number is said to be a palindrome if it’s the same when reversing all its digits.
Given an integer, the function returns true if the given number is a palindrome, else false."""
    n=str(n)
    #base case
    if len(n)<=1:
        return True
    # if the first and last element are the same then call the function without those first and last and do the same 
    else:
        return n[0]==n[-1] and ispalendrome(n[1:-1])
print("output=",ispalendrome(1451))
print("supposed output=False")
print("output=",ispalendrome(12321))
print("supposed output=True")

def bubble_sort(list,step):
    """Bubble Sort is the simplest sorting algorithm that works by repeatedly swapping the adjacent
elements if they are in the wrong order."""
    #base case
    if step==1:
        return list
    else:
        for i in range(len(list)-1):
            if list[i]>list[i+1]:
                temp=list[i]
                list[i]=list[i+1]
                list[i+1]=temp
        return(bubble_sort(list,step-1))
print("output=",bubble_sort([4,3,2,1],len([4,3,2,1])))
print("supposed output=[1,2,3,4]")

#exercise 2.1
import math
def binaryones(n):
    """Let n be some positive integer. Consider the problem of
determining the number of bits set to 1 in the binary representation of n
(i.e., n expressed in base 2)."""
    #base case1
    if n==0 :
        return 0
    #base case2
    elif math.log(n,2)==1:
        return 1
    else:
        return 1+binaryones(n-2**(int(math.log(n,2))))
print("output of decimal to binary ones")
for n in range(0,16):
    print(binaryones(n))
 
#exercise 2.2:
def prefix(l,n):
    """Consider the function that adds the first n positive
integers. Define a more general function that it is also applicable
to all nonnegative integers. In other words, modify the function
considering that it can also receive ! = 0 as an input argument"""
    #base case
    if n==0:
        return 0
    else:
        return l[0]+prefix(l[1:],n-1)
print(prefix([1,-1,10,17,7],3))

#exercise 2.4
def digits(n):
    """Consider the problem of printing the digits of some
nonnegative integer n on the console vertically, in “normal” order, where
the most significant digit must appear on the first line, the second most
significant digit on the second line, and so on."""
    #base case
    if len(str(n))<=1:
        return print(n)
    else:
        digits(int(n/10))
        return print(n%10)
print("output of vertical digits")
print("output",digits(2341))

#exercise 2.5   
def maximum(list):
    """Define a general diagram when using a divide and
conquer approach for the problem of calculating the largest value in a list
\ of n elements"""
    #base case
    if len(list)<=1:
        return list[0]
    else:
        middle=len(list)//2
        m1=maximum(list[0:middle])
        m2=maximum(list[middle:len(list)])
        return max(m1,m2) 
print("output",maximum([5,-1,3,2,4,7,2]))
print("supposed output=7")



    
