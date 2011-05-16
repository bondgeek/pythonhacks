import numpy as np
import matplotlib.pyplot as plt

Words =  ["car", "bike", "cars", "his", "tires", "she", "ive", "her", "#k", "are"]

Document = {
"auto1": [5, 0, 0, 0, 0, 1, 0, 2, 1, 0],
"auto2": [0, 0, 3, 0, 3, 0, 1, 0, 0, 1],
"auto3": [2, 0, 0, 0, 0, 0, 1, 0, 0, 0],
"auto4": [1, 0, 1, 0, 2, 0, 0, 0, 0, 1],
"auto5": [5, 0, 2, 0, 0, 4, 2, 2, 3, 7],
"moto1": [0, 3, 0, 1, 0, 0, 0, 0, 0, 0],
"moto2": [0, 0, 0, 6, 0, 0, 0, 0, 0, 1],
"moto3": [0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
"moto4": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
"moto5": [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
 }
 
kk = sorted(Document)  

def doc_sum(k):
    '''number of words in doc'''

    return sum(Document.get(k, []))
    
def doc_length(k):
    '''Euclidean distance from origin metric'''
    vect = Document.get(k, [])

    return np.sqrt(sum([v*v for v in vect]))
    
def doc_to_doc(k1, k2, normtype=None):
    
    v1 = map(float, Document.get(k1, []))
    v2 = map(float, Document.get(k2, [])) 
    
    if normtype:
        n1 = float(normtype(k1))
        v1 = [x/n1 for x in v1]
        
        n2 = float(normtype(k2))
        v2 = [x/n2 for x in v2]
        
    vect = zip(v1,v2) if len(v1) == len(v2) else ([],[])
    
    return np.sqrt(sum([(x1-x2)*(x1-x2) for x1, x2 in vect]))
    
def metrix(ntype=None):
    m = []
    for k in kk:
        dvect = []
        print("\n%-5s" % k),
        for k2 in kk:
            d = doc_to_doc(k, k2, ntype)
            dvect.append(d)
            print("%-4.2f" % d),
        m.append(dvect)
    return m
    
fig = plt.figure(1, hspace=2.)
norms = (None, doc_sum, doc_length)
nplt = 311
for n in norms:
    print("\n")
    
    mtx = metrix(n)
    ax = fig.add_subplot(nplt)
    nplt += 1
    ax.imshow(mtx, 
               extent=[1, len(kk), 1, len(kk)], 
               interpolation='nearest', 
               cmap='gray')
    #ax.yticks(range(0,10), sorted(Document))
    ax.set_yticklabels(sorted(Document))
    ax.set_xticklabels(sorted(Document), rotation='vertical')
    
    doc_title = n.func_name if n else "none"
    ax.set_title("norm: %s" % doc_title)
    
    plt.show()