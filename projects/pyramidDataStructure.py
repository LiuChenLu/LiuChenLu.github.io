#!/usr/bin/env python
from math import floor,ceil,sqrt
from array import array

#################################################################################
#functions in this file:
#delete-max:
#   Operation that takes a pyramid stored in an array A of size n, removes 
#   the largest element from the pyramid and returns it.
#insert:
#   Operation that takes a pyramid stored in an array A of size n and an 
#   element x, and inserts the new element into the pyramid
#contain:
#   Given an array A of size n and an number x, determine whether x is an 
#   element of A.

#################################################################################
#mathmatical functions. given a position in A, the fuction does what the title of
#the function suggests
def getLevel (pos):
    return floor(0.5*(sqrt(8*pos+1)-1))

def getLeftChild(pos,t=1):
    """
    Gets the t-th left child of the vertex at position pos.
    The first left child is just the left child of the vertex.
    The second left child is the left child of the left child 
    of the vertex.
    Etc.
    """
    i=getLevel(pos)
    return int(pos+0.5*(i+t)*(i+t+1)-0.5*i*(i+1))

def getRightChild(pos,t=1):
    i=getLevel(pos)
    return int(pos+0.5*(i+t)*(i+t+1)-0.5*i*(i+1)+t)

def getLeftParent(pos,t=1):
    i=getLevel(pos)
    if (pos==1) or i==0:
    #if there is no left parent, return -1
        return -1
    return int(pos+0.5*(i-t)*(i+1-t)-0.5*(i+1)*i-t)

def getRightParent(pos,t=1):
    i=getLevel(pos)
    if i==pos-0.5*(i+1)*(i):
    #if there is no right parent, return -1
        return -1
    return int(pos+0.5*(i-t)*(i+1-t)-0.5*(i+1)*i)

#################################################################################
#PART C
#################################################################################
#RUNTIME ANALYSIS:
#   Each iteration of the while loop is O(1) time because it only does 
#   arithmatics and array indexing.
#   Starting at the root-node, flipDown travels down the pyramid, switching the
#   current and the larger of its children if the child is larger than current
#   node, stopping if the current node is larger than any of its children.
#   flipDown must stop when the loop reaches the bottom most layer of the pyramid.
#   Let n be the total number of nodes in the pyramid
#   Let l be the number of layers
#       we know by part b that 1/2(l-1)l+1<=n<=1/2(l-1)l, 
#       so 1/2(sqrt(8n-7)+1)<=l and 1/2(1+sqrt(-7+8n))>=l
#   Therefore, l is in Theta(sqrt(n)).
#   Since the loop iterates at most l times traveling down the pyramid,
#   it runs in O(sqrt(n)) time
def flipDown (A):
    """
    flipDown takes a node and replaces it with the larger
    of its two children, if that child is larger than the node.
    flipDown then recursively adjust the larger child's children
    so that the pyramid regains its order
    """
    v=0
    while True:
        #left child's location
        lcLoc=getLeftChild(v)
        #right child's location
        rcLoc=getRightChild(v)

        #If a vertex has child/ren, the left justified nature of the 
        #bottom-most row guarantees that it will have a left child.
        #suppose this node has no children, then we're done
        if len(A)<=lcLoc :
            return

        #find the child that has the largest key
        if rcLoc>=len(A):
            maxchild=lcLoc
        elif A[rcLoc] > A[lcLoc]:
            maxchild=rcLoc
        else:
            maxchild=lcLoc
        
        #if the key value at max child is greater than A[v], then we need to swap
        if A[maxchild] > A[v]:
            #swap node at v and its left child
            tmp=A[maxchild]
            A[maxchild]=A[v]
            A[v]=tmp
            v=maxchild
            continue
        else:
            return

#RUNTIME ANALYSIS:
#   this function has the same runtime as flipDown
def deleteMax (A):
    """
    deleteMax takes a pyramid stored in an array A of size n, removes 
    the largest element from the pyramid and returns it.
    """
    ret=A[0]
    if len(A)==1:
        #if the length of the array is 1, then return an empty array
        A=array('i')
    else:
        #remove the last element of A and put it in A[0]
        #this function takes constant time
        A[0]=A.pop()
        #A is modified inplace by flipDown
        flipDown(A)
    return ret

#################################################################################
# PART D
#################################################################################
#RUNTIME ANALYSIS:
#   Each iteration of the while loop is O(1) time because it only does 
#   arithmatics and array indexing.
#   Starting at the bottom most layer, flipUp goes up the pyramid.
#   flipUp must stop the loop when v reaches the root node of the pyramid.
#   Let n be the total number of nodes in the pyramid
#   Let l be the number of layers
#       we know by part b that 1/2(l-1)l+1<=n<=1/2(l-1)l+l,
#       so 1/2(sqrt(8n-7)+1)<=l and 1/2(1+sqrt(-7+8n))>=l
#   Therefore, l is in Theta(sqrt(n))
#   Since the loop iterates at most l times traveling up the pyramid,
#   it runs in O(sqrt(n)) time
def flipUp(A):
    """
    flipUp takes a node and replaces it with the smaller
    of its two parents, if that parent is smaller than the node.
    flipUp then recursively adjust the smaller parent's parents
    so that the pyramid regains its order.
    """
    v=len(A)-1
    while True:
        #left parent's location
        lpLoc=getLeftParent(v)
        #right parent's location
        rpLoc=getRightParent(v)
        #if the node does not have a left or right parent, then the get parent
        #function will return -1, which is an invalid index

        #suppose this node has no parents, then we're done
        if 0>lpLoc and 0>rpLoc:
            return
        
        #find the parent that has the smallest key
        if 0<=lpLoc and 0>rpLoc:
            minparent=lpLoc
        elif 0<=rpLoc and 0>lpLoc:
            minparent=rpLoc
        elif A[rpLoc] > A[lpLoc]:
            minparent=lpLoc
        else:
            minparent=rpLoc
        
        #if that parent has a smaller value than the current node, then swap
        if A[minparent] < A[v]:
            tmp=A[v]
            A[v]=A[minparent]
            A[minparent]=tmp
            v=minparent
            continue
        else:
            return

#append has linear runtime, but most of the time it has O(1) append
#the rest of this algorithm has runtime sqrt(n) by analysis in flipUp
def insert(A,val):
    """
    Operation that takes a pyramid stored in an array A of size n and an 
    element x, and inserts the new element into the pyramid
    """
    A.append(val)
    flipUp(A)

#################################################################################
# PART E
#################################################################################
#RUNTIME:
#   Binary search eliminates aproximately half of the possible answers at each 
#   iteration, so the number of remaining possible elements is at most
#   (ceil(m/2))^k for k iterations and at least (floor(m/2))^k, where m is the
#   number of elements we're searching over -> k is in Theta(log m).
#   Since binary search has runtime log(m), this also has runtime Theta(log(m))
#
#   binarySearchDownRightChild conducts a binary search in all the right children
#   (the vertex's right child, that vertex's right child, that vertex's right
#   vertex, etc). Since any vertex's number of right children is limited by the
#   height of the pyramid.
#   Let l be the number of layers
#       we know by part b that 1/2(l-1)l+1<=n<=1/2(l-1)l+l, 
#       so 1/2(sqrt(8n-7)+1)<=l and 1/2(1+sqrt(-7+8n))>=l
#       So we know that l is in Theta(sqrt(n))
#   So the runtime of this function is log(sqrt(n))=1/2(log(n)).
#   Therefore, the runtime of this function is in Theta(log(n))
def binarySearchDownRightChild(A,x,pos):
    """
    Runs binary search down a path of right children
    """
    originalLevel=getLevel(pos)
    currentLevel=getLevel(pos)
    finalLevel=getLevel(len(A)-1)
    if getRightChild(pos,t=finalLevel-currentLevel)>=len(A):
        finalLevel = finalLevel - 1
    while True:
        mid = floor((finalLevel-currentLevel)/2)
        nxt = getRightChild(pos,t=(currentLevel-originalLevel+mid))
        if A[nxt] == x:
            return True
        elif A[nxt] > x :
            currentLevel = currentLevel+mid+1
        elif A[nxt] < x :
            finalLevel = currentLevel+mid-1
        if currentLevel > finalLevel:
            return False

#RUNTIME:
#   Starting at the root node, contain calls binarySearchDownRightChild until it
#   either reaches the leftmost node on the bottom-most layer or it finds the 
#   element x
#   If the element x is not found, then contain will iterate through all the left
#   child of the root node. Since the pyramid has height at most l in Theta(sqrt(n))
#   we know that the whileloop will run Theta(sqrt(n)) times before stopping
#   Each iteration of the whileloop takes Theta(log(n)) time by analysis of 
#   binarySearchDownRightChild.
#   Therefore, contain runs in Theta(sqrt(n) log(n))
def contain(A,x):
    """
    Given an pyramid A in the form of an array of size n and an number x, 
    determine whether x is an element of A.
    """
    pos = 0
    while True:
        #if we've searched through the entire array or if the element we're
        #looking for is larger than anything underneath it, we're done
        if pos >= len(A) or x > A[pos] :
            return False
        #if we've found the element, we are also done.
        elif x==A[pos] :
            return True
        #otherwise, do a binary search down the tree's right children
        else:
            ret = binarySearchDownRightChild(A,x,pos)
            if ret == True :
                return True
            else :
                pos = getLeftChild (pos)
                continue

#################################################################################
#testing
if __name__=="__main__":
    print deleteMax(array('i',[1])) #prints []
    print deleteMax(array('i',[10,8,9])) #prints [9,8]
    print deleteMax(array('i',[79,68,46,67,35,30,15,34,22])) 
    #prints [68, 67, 46, 34, 35, 30, 15, 22]
    print deleteMax(array('i',[100,99,98,97,97,1]))
    #prints [99, 97, 98, 1, 97]
    A=array('i',[100,99,98,97,97,1])
    insert (A,101)
    print A
    A=array('i',[100,99,98,97])
    insert (A,101)
    print A
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),68)
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),79)
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),22) 
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),35) 
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),34) 
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),35) 
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),46) 
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),67) 
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),30) 
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),15) 
#
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),36)
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),100)
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),1)
    #print contain(array('i',[79,68,46,67,35,30,15,34,22]),31)
#
    #print contain(array('i',[]),3)
    #print contain(array('i',[1]),1)
    #print contain(array('i',[1]),3)
    ##print contain(array('i',[1]),0)
