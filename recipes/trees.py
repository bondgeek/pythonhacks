class Tree(object):
    @staticmethod
    def node_gen(obj, keys):
        node = TreeNode(keys)
        k = keys[0]
        for rec in obj:
            node = node(k, rec[0], rec[1])
            yield node
    
    def __init__(self, obj_list, keys):
        self.tree = obj_list
        self.keys = keys
        
        self.root = Tree.node_gen(self.tree, keys)
 
class TreeNode(object):
    key = None
    value = None
    next_level = None
    def __init__(self, keys):
        self._keys = keys
    
    def __call__(self, key, value, next_level):
        self.key = key
        self.value = value
        self.next_level = next_level
        return self
    
    def __str__(self):
        nl_len = (len(self.next_level) 
                  if hasattr(self.next_level, "__len__") else None)
        
        return ("%s: %s %d" % (self.key, self.value, nl_len))
    
    def down(self):
        if self._keys[1:]:
            return Tree.node_gen(self.next_level, self._keys[1:])
        else:
            if hasattr(self.next_level, "__iter__"):
                return self.next_level
            else:
                return [self.next_level]

