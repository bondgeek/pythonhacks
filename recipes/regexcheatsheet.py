import re
 
def regexp():
    s = '<html><head><title>Title</title>'
 
    # with pre compiled pattern
    pattern = re.compile('title')
    match = pattern.search(s)
 
    #check for existence
    print match
    # >> <_sre.SRE_Match object at 0x011E0E58>
 
    #loop through all matches
    match = pattern.findall(s)
    print match
    # >> ['title', 'title']
 
    #grouping matches
    s = '<html><head><title>Title</title>'
    pattern = re.compile('(head).*(title)')
    match = pattern.search(s)
    print match.group(0)
    # >>head><title>Title</title
    print match.group(1)
    # >>head
 
    #replace
    pattern = re.compile('title')
    print pattern.sub("ersetzt",s)
    # >> <html><head><ersetzt>Title</ersetzt>
 
    #split
    pattern = re.compile('title')
    print pattern.split(s)
    # >> ['<html><head><', '>Title</', '>']
 
    #replace alle lines in file by "eineZeile"
    f = open('test.txt','r')
    l= ['eineZeile' for l in f.readlines()]
    f.close()
    print l
    f=open("test.txt", "w")
    f.writelines(l)
    f.close()
 
regexp()

