#switches
print "switch example 1"
cases = {
'a': 
    lambda: 'one',
'b':
    lambda: 'two',
'default':
    lambda: 'three'
}

switch = lambda c: cases.get(c, cases['default'])()

var = ['b','xxx']
for v in var:
    out = switch(v)
    print("Switch on %s = %s"%(v,out))


print """\nswitch example 2
        default included in switch"""

op = raw_input("Enter operation for 2 'op' 3: ")

if op in "+-*/":
    print("2 %s 3 = " % op)
else:
    print("'%s' is an unkown operation." % op)

cases = {
     '+': lambda : 2 + 3,
     '-': lambda : 2 - 3,
     '*': lambda : 2 * 3,
     '/': lambda : 2. / 3.
     }

switch2 = cases.get(op, lambda : 0)()

print(switch2)


print "\nswitch example 3"
name = raw_input("What is your name? ")
op = raw_input("enter 'l' or 'p'")

cases = {
    'l': len,
    'p': lambda txt: txt.upper()
    }

def default(obj): 
    print("Invalid entry, %s" % obj)

switch3 = cases.get(op, default)
out = switch3(name)

print(out)
