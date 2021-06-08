class Node:
    def __init__(self, name, simplex_name=[], filtration_value=0):
        self.name = name  # [4]
        self.simplex_name = simplex_name  # [1,2,3,4]
        self.filtration_value = filtration_value
        self.next = None   # Pointer to sibling
        self.parent = None  # Pointer to parent
        self.child = None  # Pointer to child
