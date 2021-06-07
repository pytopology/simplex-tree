class Node:
    def __init__(self, name, simplex_name=[], filtration_value=0):
        self.name = name
        self.simplex_name = simplex_name
        self.filtration_value = filtration_value
        self.next = None   # Pointer to sibling
        self.parent = None  # Pointer to parent
        self.child = None  # Pointer to child
