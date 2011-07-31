import xml.dom.minidom as xml

def read_xml(fname):
    "returns a dom object for the xml file"
    f = open(fname)
    fdata = f.read().replace("\n", "").replace("\r", "")
    
    f.close()
    return xml.parseString(fdata)

def get_xmltext(node):
    "return text"
    rc = ""
    
    for n in node.childNodes:
        if n.nodeType == n.TEXT_NODE:
            rc = "".join((rc, n.data))

    return rc
