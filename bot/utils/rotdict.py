class Node:
    def __init__(self,key,val,next,prev):
        self.key=key
        self.val=val
        self.next=next
        self.prev=prev
    def __str__(self):
        return f"{repr(self.prev)} <- ({repr(self.key)}:{repr(self.val)}) -> {repr(self.next)}"
    def __repr__(self):
        return f"{repr(self.val)}"

class RotDict:
    def __init__(self):
        self.data = {}
        self.state = None
    def __setitem__(self, key, val):
        if key in self.data:
          self.data[key].val = val  
        elif self.state == None:
            node = Node(key,val,None,None)
            node.next=node
            node.prev=node
            self.state=node
            self.data[key]=node
        else:
            node = Node(key,val,self.state,self.state.prev)
            node.prev.next=node
            node.next.prev=node
            self.data[key]=node
    def __getitem__(self,key):
        return self.data[key].val
    def __len__(self):
        return len(self.data)
    def __delitem__(self, key):
        node = self.data[key]
        if node is self.state:
            self.state = node.next
        node.next.prev, node.prev.next = node.prev, node.next
        del self.data[key]
        if len(self.data)==0:
            self.state=None
    def __contains__(self,key):
        return key in self.data
    def __iter__(self):
        return self.keys()
    def items(self):
        node = self.state
        if node == None:
            return
        yield node.key, node.val
        node=node.next
        while node is not self.state:
            yield node.key, node.val
            node=node.next
    def keys(self):
        node = self.state
        if node == None:
            return
        yield node.key
        node=node.next
        while node is not self.state:
            yield node.key
            node=node.next
    def values(self):
        node = self.state
        if node == None:
            return
        yield node.val
        node=node.next
        while node is not self.state:
            yield node.val
            node=node.next
    def __repr__(self):
        return repr(self.data)
    def __str__(self):
        return "{"+"".join(f"\n\t{k}: {v}" for k,v in self.items())+"\n}"
    @property
    def key(self):
        return self.state.key
    @property
    def val(self):
        return self.state.val
    @val.setter
    def val(self,val):
        self.state.val = val
    def next(self):
        self.state = self.state.next
        return self
    def prev(self):
        self.state = self.state.prev
        return self
    def rot(self,direction):
        return self.next() if direction else self.prev()
        
    def apply(self,fun,start=0,end=None):
        if end is None:
            end = len(self)-1
        if start is None:
            start = -len(self)+1
        if 0 <= start <= end or 0 >= start >= end:
            a = start
            b = end
        elif 0 <= end <= start or 0 >= end >= start:
            a = end
            b = start
        else:
            self.apply(fun,1 if end>0 else -1,end)
            self.apply(fun,start,0)
            return
        old = self.state
        direction = a > 0 or b > 0
        a = abs(a)
        for i in range(abs(b)+1):
            if i >= a:
                fun(self.val)
            self.rot(direction)
        self.state=old
            
    def jump(self,key):
        self.state = self.data[key]
        return self
    def __del__(self):
        while self.state:
            node = self.state
            self.state = self.state.next
            node.next = None
            node.prev = None
