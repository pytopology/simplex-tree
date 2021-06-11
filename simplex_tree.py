from node import Node
import itertools
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random


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
            # print("Inserting : ", node_name, "Parent Simplex name :",
            #       parent_simplex_name, "Simplex Name :", simplex_name)
            new_node = self.__find(simplex_name)  # [2] | [3]
            if new_node is None:
                new_node = Node(node_name, simplex_name, filtration)
                self.__insert_child(new_node, simplex_name,
                                    siblings[i+1:], filtration)
                new_node.next = temp.next
                temp.next = new_node  # [1].next = [2] | [2].next = [3]
                temp = new_node  # temp [2] | temp [3]
            else:
                # print("Simplex :{} already exists".format(simplex_name))
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
            # node [1] | [1, 2] | [1,2,3]
            node = Node(node_name, simplex_name, filtration)
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

    def compute_boundaries(self, simplex):
        '''
        Compute the Boundary operator

        Arguments:
        simplex : Simplex for which we need to find the boundary operator
        '''
        found_simplex = self.__find(simplex)
        if found_simplex:
            return self.__findsubsets(simplex, len(simplex)-1)
        return None

    def update_filtration(self, _simplex, filtration):
        simplex = _simplex
        simplex.sort()
        found_simplex = self.__find(simplex)
        if found_simplex is not None:
            # print("Simplex:", found_simplex, "is already present")
            # TODO : Add new function to update the filtration value
            if found_simplex.filtration_value != 0.0:
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
            # print("Simplex:", found_simplex, "is already present")
            return
        if self.head is None:
            # Create a root node
            node = Node("x", 0.0)
            self.head = node
            self.__insert_child(self.head, [], simplex, filtration)
        else:
            node = self.head.child
            self.__insert_sibling(node, simplex, [], filtration)

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
            temp = node  # [1]
            while temp is not None:
                # print(temp.simplex_name)
                # output : [[1]] | [[1] , [2]] | [[1], [2], [3]]
                output.append(temp.simplex_name)
                temp = temp.next
            return output
        temp_next = node  # head
        while (temp_next is not None):
            # print("searching children of {}".format(temp_next.simplex_name))
            # [[1], [2], [3]] # append [[[1],[2],[3]]]
            output.extend(self.__get_simplices(temp_next.child, dim-1, []))
            # print(output)
            temp_next = temp_next.next
        # print(output)
        return output

    def get_vertices(self):
        '''
        Get Vertices i.e Simplices of 0 dimensions
        '''
        outputs = self.__get_simplices(self.head, 0, [])
        print("Vertices :", outputs)
        return outputs

    def get_simplices(self, dim=0):
        '''
        Get Simplex by Dimensions
        '''
        if self.head is None:
            return
        outputs = self.__get_simplices(self.head, dim)
        print("outputs :", outputs)
        return outputs

    def __get_tuple(self, simplices, dim):
        '''
        Internal Method used to convert the list of simplices array 
        into a tuple. For e.g [[1,2,3]] => [(1,2,3)]

        Arguments:
        simplices : list of simplices which needs to be converted into tuple
        dim : Dimension of the input simplex

        '''
        output = []
        for e in filter(lambda x: len(x) == dim, simplices):
            output.append(tuple(e))
        return output

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
        return [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0.75, 0.75, 0.75), (0.5, 1.0, 0.707)]

    def draw_simplex3D(self, max_dim=None):
        '''
        Method to draw the simplicial complex using the simplex tree

        Arguments:
        max_dim : Max dimension upto which we should print the simplicial complex

        '''
        vertices = self.__get_simplices(self.head, 0)
        coordinates = self.__get_coordinates(vertices)

        x2, y2, z2 = zip(*coordinates)
        plt.clf()
        fig = plt.figure()

        ax = fig.gca(projection='3d')

        ax.set_xlabel('X')
        ax.set_xlim3d(0, 1.5)
        ax.set_ylabel('Y')
        ax.set_ylim3d(0, 1.5)
        ax.set_zlabel('Z')
        ax.set_zlim3d(0, 1.5)
        plt.title("Simplicial Complex")
        ax.axis('off')
        ax.scatter(x2, y2, z2)

        dim = min(self.getdimension(), 3)

        if max_dim is not None:
            dim = min(self.getdimension(), min(3, max_dim))

        config = {0: {'edgecolors': 'r',
                      'facecolor': [0.0, 0.0, 1],
                      'linewidths': 1,
                      'alpha': 0.3
                      },
                  1: {'edgecolors': 'r',
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
                      'facecolor': [0.56, 0.875, 0.79],
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

    def draw_simplex(self):
        '''
        Legacy method to draw the simplicial complex (Supports only 2D)
        '''
        print("Method is deprecated. Please use draw_simplex3D(dim=0)")
        return
        vertices = self.__get_simplices(self.head, 0)
        edges = self.__get_tuple(self.__get_simplices(self.head, 1), 2)
        triangles = self.__get_tuple(self.__get_simplices(self.head, 2), 3)
        print(edges)
        plt.figure(figsize=(8, 8))
        plt.title("Simplex Tree")
        ax = plt.subplot(111)
        ax = plt.gca(projection='3d')
        ax.set_xlim([-1.1, 1.1])
        ax.set_ylim([-1.1, 1.1])
        ax.set_zlim([-1.1, 1.1])
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.axis('off')
        G = nx.Graph()
        G.add_edges_from(edges)
        # Creating a dictionary for the position of the nodes
        pos = nx.spring_layout(G)
        for x, y in edges:
            (x0, y0) = pos[x]
            (x1, y1) = pos[y]
            line = plt.Line2D([x0, x1], [y0, y1],
                              color='black', zorder=1, lw=0.7)
            ax.add_line(line)

        for x, y, z in triangles:
            (x0, y0) = pos[x]
            (x1, y1) = pos[y]
            (x2, y2) = pos[z]
            tri = plt.Polygon([[x0, y0], [x1, y1], [x2, y2]],
                              edgecolor='black', facecolor=plt.cm.Blues(0.6),
                              zorder=2, alpha=0.4, lw=0.5)
            ax.add_patch(tri)
        for i in vertices:
            (x, y) = pos[i[0]]
            circ = plt.Circle([x, y], radius=0.02, zorder=3, lw=0.5,
                              edgecolor='Black', facecolor=u'#ff7f0e')
            ax.add_patch(circ)

        plt.plot()
        plt.show()

    def delete(self, simplex):
        # mini=min(simplex.name)
        # length=len(simplex.name)
        # count=0
        # temp=head.child
        # while(temp.name[0]<=mini):
        #     if(temp.name[0]==mini):
        #         count=count+1
            
       
            

        pass

    def filtration(self, simplex):
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
        print("Simplex: {} Filtration value :{}".format(
            node.simplex_name, node.filtration_value))
        self.__print_siblings(node.child)

    def print_tree(self, node=None):
        node = self.head
        self.__print_siblings(node.child)

    def coface(self, simplex):
        if self.head is None:
            return None
        # temp=simplex
        # lst=list()
        # while(temp != None):
        #     temp1=temp.child
        #     temp2=temp1
        #     while(temp2!=None):
        #         lst.append(temp2.simplex_name)
        #         temp2=temp2.sibling
        lst=list()
        vertices = self.num_vertices()
        simplices=list()
        for i in range(vertices):
            sim = self.__get_simplices(self.head,i,[])
            simplices=simplices+sim

        
        for i in range (len(simplices)):
            if(set(simplex).intersection(set(simplices[i])) == set(simplex)):
                lst.append(simplices[i])
        # lst=lst.remove(simplex)
        return lst

    def star(self, vertex):
        if len(vertex)==1:
            star_vertex=self.coface(vertex)
            return star_vertex
            
        return 
    # def lower_star(self, vertex):
    #     star_v = self.star(vertex)
    #     lst=list()
    #     for i in range(len(star_v)):
    #         if (vertex.filtration_value >= star_v[i].filtration_value):
    #             lst.append(star_v[i])
    #     return lst
