from node import Node


class SimplexTree:
    def __init__(self):
        self.head = None
        print("Created Simplex Tree")

    def __get_simplex_name(self, simplex_prefix, simplex_name):
        '''
        Internal method to generate the simplex name

        Arguments:-
        simplex_prefix : Parent simplex name (For e.g. [1,2])
        simplex_name : Simplex name (For e.g. [3])
        returns the appended complete name of the simplex (For e.g. [1,2,3])
        '''
        _simplex_prefix = simplex_prefix.copy()
        _simplex_prefix.append(simplex_name)
        return _simplex_prefix

    def insert_sibling(self, node, siblings, parent_simplex_name):
        '''
        Iterative Method to insert the sibling in horizontal direction. 
        This method also calls the insert_child() method to insert the
        children of the siblings.

        Arguments:-
        node : Node to which the siblings will be added
        siblings : Array of siblings
        parent_simplex_name : Name of the parent Simplex name
        '''
        if len(siblings) == 0 or siblings is None:
            return
        print("Inserting siblings", siblings)
        temp = node

        while(temp.next is not None):
            temp = temp.next
        for i in range(len(siblings)):
            node_name = siblings[i]
            simplex_name = self.__get_simplex_name(
                parent_simplex_name, node_name)
            print("Inserting : ", node_name, "Parent Simplex name :",
                  parent_simplex_name, "Simplex Name :", simplex_name)
            new_node = self.__find(simplex_name)
            if new_node is None:
                new_node = Node(node_name, simplex_name)
                self.insert_child(new_node, simplex_name, siblings[i+1:])
                temp.next = new_node
                temp = new_node
            else:
                print("Simplex :{} already exists".format(simplex_name))
                self.insert_child(new_node, simplex_name, siblings[i+1:])

    def insert_child(self, parent, simplex_prefix, children):
        '''
        Recursive method to insert the children also calls the insert_siblings()
        method.

        Arguments:-
        parent : parent node
        simplex_prefix : Complete name of the parent simplex. (For e.g.[1,2,3]-> [1,2])
        children : Simplex to add in the given parent (For eg. [1,2,3])

        '''
        if len(children) == 0 or children is None:
            return
        print("Inserting children", children)
        node_name = children[0]
        simplex_name = self.__get_simplex_name(simplex_prefix, node_name)
        node = self.__find(simplex_name)
        node_exist = node is not None
        if not node_exist:
            node = Node(node_name, simplex_name, 0.0)
        self.insert_child(node, simplex_name, children[1:])
        self.insert_sibling(node, children[1:], simplex_prefix)

        # Node Children might not be enpty
        # Find the last node (TODO : Need to add appropriately to maintain order)
        #last_child_node = parent.child
        if not node_exist:
            if parent.child is None:
                parent.child = node
            else:
                last_child_node = parent.child
                while (last_child_node.next is not None):
                    last_child_node = last_child_node.next
                last_child_node.next = node

        # Node Children might not be enpty
        # Find the last node (TODO : Need to add appropriately to maintain order)
        # last_child_node = parent.child
        # if last_child_node is not None:
        #   while (last_child_node.next is not None):
        #     last_child_node = last_child_node.next

        #   last_child_node.next = node
        # else:
        #   last_child_node = node

    def insert(self, _simplex, filtration=0.0):
        '''
        Insert Method (API) to insert the simplex.

        Arguments:
        _simplex : Input Simplex array eg. [1,2,3]
        filteration : Filteration value for the simplex
        '''
        simplex = _simplex
        simplex.sort()
        if self.__find(simplex) is not None:
            print("Simplex:", simplex, "is already present")
            return
        if self.head is None:
            # Create a root node
            node = Node("x", filtration)
            self.head = node
            self.insert_child(self.head, [], simplex)
        else:
            node = self.head.child
            self.insert_sibling(node, simplex, [])

    def find_simplex(self, simplex):
        '''
        Method to find the given simplex

        Arguments:
        simplex : Input Simplex array eg. [1,2,3]
        '''
        __simplex = self.__find(simplex)
        if __simplex is not None:
            print("Simplex {} is presnt in the simplex tree".format(
                __simplex.simplex_name))
        else:
            print("Simplex {} is NOT presnt in the simplex tree".format(simplex))
        return __simplex

    def __find(self, simplex):
        '''
        Internal Method to find the given simplex

        Arguments:
        simplex : Input Simplex array eg. [1,2,3]
        '''
        if self.head is None:
            return None
        found = False
        temp = self.head.child
        found_simplex = None
        for i in simplex:
            while(temp is not None):
                if temp.name == i:
                    found_simplex = temp
                    temp = temp.child
                    break

                temp = temp.next

        if found_simplex is not None and found_simplex.simplex_name == simplex:
            return found_simplex
        return None

    def delete(self):
        pass

    def filteration(self, node):
        pass

    def print_siblings(self, node, prefix=""):
        '''
        Iterative method to print the simplices

        Arguments:
        node : Input Simplex array (For eg. [1,2,3])
        prefix : Parent Simplex name (For eg. [1,2]) (Deprecated)
        '''

        if node is None:
            return
        temp = node
        while(temp is not None):
            self.print_child(temp, "")
            temp = temp.next

    def print_child(self, node, prefix=""):
        '''
        Recursive method to print the children of a node
        '''
        if node is None:
            return
        prefix = prefix + str(node.name)+","
        print("(Child) :Simplex:(", prefix, ")", node.simplex_name)
        self.print_siblings(node.child)
        # self.print_child(node.child,prefix)

    def print_tree(self, node=None):
        node = self.head
        self.print_siblings(node.child)
