from node import Node
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random


class SimplexTree:
    def __init__(self):
        self.head = None
        print("Created Simplex Tree")

    def __get_random_filtration(self):
        filt = [1.0, 2.0, 3.0, 4.0]
        return random.choice(filt)

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

    def __insert_sibling(self, node, siblings, parent_simplex_name, filtration):
        '''
        Iterative Method to insert the sibling in horizontal direction.
        This method also calls the __insert_child() method to insert the
        children of the siblings.

        Arguments:-
        node : Node to which the siblings will be added
        siblings : Array of siblings
        parent_simplex_name : Name of the parent Simplex name
        '''
        if len(siblings) == 0 or siblings is None:
            return
        # print("Inserting siblings", siblings)
        temp = node  # [1]

        for i in range(len(siblings)):  # [2,3] | [3] | []
            node_name = siblings[i]  # 2 | 3
            while(temp.next is not None and temp.next.name < node_name):
                temp = temp.next  # temp -> last node of the linked list

            simplex_name = self.__get_simplex_name(
                parent_simplex_name, node_name)  # parent_simplex_name = [] , 2 => [2] | [],3 => [3]
            new_node = self.__find(simplex_name)  # [2] | [3] # [2,3,4]
            if new_node is None:
                if len(simplex_name) == 2:
                    new_node = Node(node_name, simplex_name,
                                    self.__get_random_filtration())
                elif len(simplex_name) == 1:
                    new_node = Node(node_name, simplex_name, 0.0)

                else:
                    new_node = Node(node_name, simplex_name, filtration)

                self.__insert_child(new_node, simplex_name,
                                    siblings[i+1:], filtration)
                new_node.next = temp.next
                temp.next = new_node  # [1].next = [2] | [2].next = [3]
                temp = new_node  # temp [2] | temp [3]
            else:
                self.__insert_child(new_node, simplex_name,
                                    siblings[i+1:], filtration)  # new_node: [2] simplex_name: [2] siblings [3]

    def __insert_child(self, parent, simplex_prefix, children, filtration):
        '''
        Recursive method to insert the children also calls the __insert_siblings()
        method.

        Arguments:-
        parent : parent node
        simplex_prefix : Complete name of the parent simplex. (For e.g.[1,2,3]-> [1,2])
        children : Simplex to add in the given parent (For eg. [1,2,3])

        '''
        if len(children) == 0 or children is None:
            return
        # print("Inserting children", children) # [1,2,3] | [2,3] | [3]
        node_name = children[0]  # [1] | [2] | [3]
        simplex_name = self.__get_simplex_name(
            simplex_prefix, node_name)  # [] , 1 => [1] | [1] , 2 => [1, 2] | [1,2], 3 => [1 ,2 , 3]
        node = self.__find(simplex_name)  # [1] | [1, 2] | [1 ,2 ,3]
        node_exist = node is not None
        if not node_exist:
            if len(simplex_name) == 2:
                node = Node(node_name, simplex_name,
                            self.__get_random_filtration())
            elif len(simplex_name) == 1:
                node = Node(node_name, simplex_name, 0.0)
            else:
                node = Node(node_name, simplex_name, filtration)
            # node [1] | [1, 2] | [1,2,3]
        self.__insert_child(node, simplex_name,
                            children[1:], filtration)  # [2, 3] | [3] | []
        self.__insert_sibling(
            node, children[1:], simplex_prefix, filtration)  # node [1] simplex_prefix [] , children [2,3]

        # Node Children might not be enpty
        # Find the last node (TODO : Need to add appropriately to maintain order)
        # last_child_node = parent.child
        if not node_exist:
            if parent.child is None:
                parent.child = node
            else:
                last_child_node = parent.child
                while (last_child_node.next is not None):
                    last_child_node = last_child_node.next
                last_child_node.next = node

    def __findsubsets(self, simplex, length):
        return list(itertools.combinations(simplex, length))

    def compute_boundaries(self, simplex, return_list=False):
        '''
        Compute the Boundary operator

        Arguments:
        simplex : Simplex for which we need to find the boundary operator
        '''
        found_simplex = self.__find(simplex)
        if found_simplex:
            if return_list:
                return [list(t) for t in self.__findsubsets(simplex, len(simplex)-1)]
            return self.__findsubsets(simplex, len(simplex)-1)
        return None

    def get_max_child_filtration(self, simplex):
        sub_simplices = self.compute_boundaries(simplex, True)
        max_filt = max(
            [self.__find(ss).filtration_value for ss in sub_simplices])
        return max_filt

    def balance_filtrations(self):
        i = 2
        simplices = self.__get_simplices(self.head, i, [])

        while(len(simplices) > 0):
            for _ss in simplices:
                _f = self.get_max_child_filtration(_ss)
                self.__find(_ss).filtration_value = _f
            i = i+1
            simplices = self.__get_simplices(self.head, i, [])

    def update_filtration(self, _simplex, filtration):
        self.__update_filtration(_simplex, filtration)
        self.balance_filtrations()

    def __update_filtration(self, _simplex, filtration):
        simplex = _simplex
        simplex.sort()
        found_simplex = self.__find(simplex)
        if found_simplex is not None:

            sub_simplices = self.compute_boundaries(simplex, True)

            if sub_simplices is not None:
                if len(self.__find(sub_simplices[0]).simplex_name) > 1:
                    max_filt = max(
                        [self.__find(ss).filtration_value for ss in sub_simplices])
                    max_simplices = [
                        ss for ss in sub_simplices if self.__find(ss).simplex_name[len(simplex)-2] == simplex[len(simplex)-1]]
                    for _ss in max_simplices:
                        self.update_filtration(_ss, filtration)
                    if max_filt > filtration:
                        other_simplices = [
                            ss for ss in sub_simplices if self.__find(ss).filtration_value == max_filt]
                        for _ss in other_simplices:
                            self.update_filtration(_ss, filtration)

            found_simplex.filtration_value = filtration

    def insert(self, _simplex, filtration=0.0):
        '''
        Insert Method (API) to insert the simplex.

        Arguments:
        _simplex : Input Simplex array eg. [1,2,3]
        filteration : Filteration value for the simplex
        '''
        simplex = _simplex
        simplex.sort()
        found_simplex = self.__find(simplex)
        if found_simplex is not None:
            return
        if self.head is None:
            # Create a root node
            node = Node("x", 0.0)
            self.head = node
            self.__insert_child(self.head, [], simplex, filtration)
        else:
            node = self.head.child
            self.__insert_sibling(node, simplex, [], filtration)
        self.balance_filtrations()

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
        temp = self.head.child  # [1]
        found_simplex = None
        for i in simplex:  # 1 | 2
            while(temp is not None):  # horizontal search
                if temp.name == i:  # 1 == 1
                    found_simplex = temp
                    temp = temp.child
                    break

                temp = temp.next

        if found_simplex is not None and found_simplex.simplex_name == simplex:
            return found_simplex
        return None

    def __get_simplices(self, node, dim=0, output=[]):
        if node is None:
            # No simplices available for the given dimension
            return []
        if dim == -1:
            temp = node
            while temp is not None:
                output.append(temp.simplex_name)
                temp = temp.next
            return output
        temp_next = node
        while (temp_next is not None):
            output.extend(self.__get_simplices(temp_next.child, dim-1, []))
            temp_next = temp_next.next
        return output

    def get_vertices(self):
        '''
        Get Vertices i.e Simplices of 0 dimensions
        '''
        outputs = self.__get_simplices(self.head, 0, [])
        return outputs

    def get_simplices(self, dim=0):
        '''
        Get Simplex by Dimensions
        '''
        if self.head is None:
            return
        outputs = self.__get_simplices(self.head, dim)
        return outputs

    def __get_coordinates(self, vertices):
        '''
        Internal method used to generate the random coordinates for the vertices
        of the simplicial complex

        Arguments:
        vertices : list of vertices
        '''
        max_x = 0
        max_y = 0
        max_z = 0
        coordinates = []
        for _ in vertices:
            _x = random.random()
            max_x = max(max_x, _x)
            _y = random.random()
            max_y = max(max_y, _y)
            _z = random.random()
            max_z = max(max_z, _z)
            coordinates.append((_x, _y, _z))

        # vertices
        # return coordinates
        return [(-0.75, 0.25, 0),  # 1
                (-0.25, 0, 0),  # 2
                (-0.5, 0.5, -0.5),  # 3
                (-0.125, 1, 0),  # 4
                (-0.125, 0.125, -0.75),  # 5
                (0.5, 0.5, 0),  # 6
                (1, 0, 0),  # 7
                (1, 0.75, 0),  # 8
                (0, 0, 0),  # 9
                (0.5, 0.75, 0)  # 10
                ]

    def draw_simplex3D(self, max_dim=None):
        '''
        Method to draw the simplicial complex using the simplex tree

        Arguments:
        max_dim : Max dimension upto which we should print the simplicial complex

        '''
        vertices = self.__get_simplices(self.head, 0)
        coordinates = self.__get_coordinates(vertices)

        x2, y2, z2 = zip(*coordinates)

        fig = plt.figure(figsize=(4, 4))

        ax = fig.gca(projection='3d')

        ax.set_xlabel('X')
        ax.set_xlim3d(-0.75, 1.5)
        ax.set_ylabel('Y')
        ax.set_ylim3d(-0.75, 1.5)
        ax.set_zlabel('Z')
        ax.set_zlim3d(-0.75, 1.5)
        ax.axis('off')
        ax.scatter(x2, y2, z2)

        dim = min(self.getdimension(), 3)

        if max_dim is not None:
            dim = min(self.getdimension(), min(3, max_dim))

        plt.title("Simplicial Complex Upto Dim: {}".format(dim))

        config = {0: {'edgecolors': 'r',
                      'facecolor': [0.0, 0.0, 1],
                      'linewidths': 1,
                      'alpha': 0.3
                      },
                  1: {'edgecolors': 'black',
                      'facecolor': [0.0, 0.0, 1],
                      'linewidths': 1,
                      'alpha': 1.0
                      },
                  2: {'edgecolors': 'black',
                      'facecolor': [0.56, 0.875, 0.79],
                      'linewidths': 1,
                      'alpha': 0.3
                      },
                  3: {'edgecolors': 'black',
                      'facecolor': [0.56, 1, 0.79],
                      'linewidths': 1,
                      'alpha': 1.0
                      }, }

        for _d in range(0, dim+1):
            _simplices = self.__get_simplices(self.head, _d)
            poly3d_edges = [[coordinates[vert_id-1] for vert_id in face]
                            for face in _simplices]
            edge_collection = Poly3DCollection(poly3d_edges, **config[_d])
            ax.add_collection3d(edge_collection)

        plt.show()

    def draw_simplex(self, max_dim):
        self.draw_simplex3D(max_dim)

    def delete(self):
        pass

    def filtration(self, _simplex):
        simplex = _simplex
        simplex.sort()
        found_simplex = self.__find(simplex)
        if found_simplex is None:
            return
        return found_simplex.filtration_value

    def getdimension(self):
        '''
        dimension of simplicial complex= max_dimension of any simplex
        Arguments:
        '''
        vertices = self.get_vertices()
        dim = -1
        for i in range(len(vertices)+1):
            simplices = self.__get_simplices(self.head, i, [])
            if simplices:
                dim = dim+1
            else:
                return dim

    def num_vertices(self):
        vertices = self.get_vertices()
        if vertices:
            return len(vertices)
        return 0

    def num_simplices(self):
        '''
        returns the number of simplices in simplicial complex
        '''
        count = 0
        vertices = self.get_vertices()
        if vertices:
            count = count+len(vertices)
            for i in range(1, len(vertices)):
                simplices = self.__get_simplices(self.head, i, [])
                if simplices:
                    count = count+len(simplices)
                else:
                    break
        return count

    def get_skeleton(self, dim):
        vertices = self.get_vertices()
        if vertices:
            if(dim == 0):
                return vertices
            for i in range(1, dim+1):
                simplices = self.__get_simplices(self.head, i, [])
                if simplices:
                    vertices = vertices+simplices
                else:
                    # return vertices
                    break
            return vertices

    def __print_siblings(self, node, prefix=""):
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
            self.__print_child(temp, "")
            temp = temp.next

    def __print_child(self, node, prefix=""):
        '''
        Recursive method to print the children of a node
        '''
        if node is None:
            return
        prefix = prefix + str(node.name)+","
        print("Simplex: {} Filtration value : {}".format(
            node.simplex_name, node.filtration_value))
        self.__print_siblings(node.child)

    def print_tree(self, node=None):
        node = self.head
        self.__print_siblings(node.child)

    def link(self, x):
        a = self.head
        ans = []
        a = a.child
        while(a != None):
            if(a.name == x):
                c = a.child
                while(c != None):
                    ans.append(c.name)
                    c = c.next
                break
            else:
                c = a.child
                while(c != None):
                    if(c.name == x):
                        ans.append(a.name)
                        break
                    c = c.next
            a = a.next
        final_list = []
        for i in range(len(ans)):
            lis = list(map(list, itertools.combinations(ans, i+1)))
            for j in lis:
                if(self.__find(j) != None):
                    final_list.append(j)
        return final_list

    def delete(self, list_simplex):
        a = self.head
        self.del_rec(a, list_simplex)

    def del_rec(self, a, list_simplex):
        if(a == None):
            return
        if(len(list_simplex) == 1):
            if(a.child != None):
                if (a.child.name == list_simplex[0]):
                    a.child = a.child.next
                else:
                    self.del_rec(a.next, list_simplex)
            if(a.next != None):
                if (a.next.name == list_simplex[0]):
                    a.next = a.next.next
                else:
                    self.del_rec(a.child, list_simplex)
        else:
            if(a.child != None):
                if (a.child.name == list_simplex[0]):
                    self.del_child_only(a.child, list_simplex[1:])
                else:
                    self.del_rec(a.child, list_simplex)
            if(a.next != None):
                if (a.next.name == list_simplex[0]):
                    self.del_child_only(a.next, list_simplex[1:])
                else:
                    self.del_rec(a.next, list_simplex)

    def del_child_only(self, a, list_simplex):
        if(a == None):
            return
        if(len(list_simplex) == 1):
            if(a.child.name == list_simplex[0]):
                a.child = a.child.next
            else:
                self.del_rec(a.child, list_simplex)
        else:
            if(a.child.name == list_simplex[0]):
                self.del_child_only(a.child, list_simplex[1:])
            else:
                self.del_rec(a.child, list_simplex)

    def coface(self, simplex):
        if self.head is None:
            return None
        lst = list()
        vertices = self.num_vertices()
        simplices = list()
        for i in range(vertices):
            sim = self.__get_simplices(self.head, i, [])
            simplices = simplices+sim

        for i in range(len(simplices)):
            if(set(simplex).intersection(set(simplices[i])) == set(simplex)):
                lst.append(simplices[i])
        # lst=lst.remove(simplex)
        return lst

    def star(self, vertex):
        if len(vertex) == 1:
            star_vertex = self.coface(vertex)
            return star_vertex

        return
    # def lower_star(self, vertex):
    #     star_v = self.star(vertex)
    #     lst=list()
    #     for i in range(len(star_v)):
    #         if (vertex.filtration_value >= star_v[i].filtration_value):
    #             lst.append(star_v[i])
    #     return lst
