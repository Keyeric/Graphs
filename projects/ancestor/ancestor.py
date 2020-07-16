class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def earliest_ancestor(ancestors, starting_node):
    q = Queue() # empty queue
    current_node = starting_node # copy to fuck up/"munge"
    relationships = {}
    for node in ancestors: # node(parent, child)
        if node[1] not in relationships:
            relationships[node[1]] = set() # put it in relationships
        relationships[node[1]].add(node[0])# assign parents to nodes


    if starting_node in relationships: # if starting node(child) is a child
        q.enqueue(relationships[current_node]) #add child to line of ancestor inspection
    else:
        return - 1 # starting node is not a child, abort

    while True:
        relations = q.dequeue()
        current_node = min(relations)
        if current_node not in relationships: #no parent?
            return current_node #you've reached the end!
        else:
            q.enqueue(relationships[current_node]) #else keep going
