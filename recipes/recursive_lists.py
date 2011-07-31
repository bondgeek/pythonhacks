#!/urs/bin/env python
'''
recipe for printing a nested list recursively,
keeps track of the layer
adapted from:
http://www.freenetpages.co.uk/hp/alan.gauld/tutrecur.htm

'''

nestedlist = [[13,6], [4, [7,8]], 5, [8,[9,[10,'a']]]]


def print_list(L):
    '''basic version'''
    # if its empty do nothing
    if not L: 
        return
        # if it's a list call printList on 1st element
    
    if type(L[0]) == type([]):
        print_list(L[0])
    else: #no list so just print 
        print L[0] 
    
    # now process the rest of L 
    
    print_list(L[1:])


def print_list(L):
    '''basic version'''
    # if its empty do nothing
    if not L: 
        return
        # if it's a list call printList on 1st element
    
    if type(L[0]) == type([]):
        print_list(L[0])
    else: #no list so just print 
        print L[0] 
    
    # now process the rest of L 
    
    print_list(L[1:])
