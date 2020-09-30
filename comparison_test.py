import  numpy as np
from collections import Counter
class node:
    def __init__(self, node):
        self.node = node

    def __eq__(self, other_node):
        return 'Wrong' if self.node == True and not other_node.node else self.node == other_node.node

    def __repr__(self):
        return str(int(self.node))

class line:
    def __init__(self, array):
        self.array = np.array([node(i) for i in array])

    def __eq__(self, other_array):
        comparison = [p == h for p,h in zip(self.array, other_array.array)]
        return(np.array(comparison, dtype = object))

    def wrongs(self):
        pass


list1 = line([0,1,0,1,1]) # Player's Grid
list2 = line([0,1,1,0,1]) # Hidden Grid to be guessed
print(list1.array)
print(list2.array)

### comparison should be [True, True, False, (True, True), True]
comparison = list1 == list2
print(comparison, '\n')

### count should be Counter({True: x, 'Wrong': y})
count = Counter(comparison)
# print(count)
print(count.get('Wrong')) # can return None if 'Wrong' not in count

### comparison.all() should be True if all of node's condition from comparison are true
print(comparison.all())