import unittest
from simplex_tree import SimplexTree


class TestSimplex(unittest.TestCase):

    def test_1(self):
        '''
        Check whether subsets are inserted or not
        '''
        sim = SimplexTree()
        sim.insert([1, 3])
        self.assertNotEqual(sim.find_simplex([1]), None)

    def test_2(self):
        '''
        Add [1,2] and then add [1,3]
        [1,2 should still be present]
        '''
        sim = SimplexTree()
        sim.insert([1, 2])
        self.assertNotEqual(sim.find_simplex([1, 2]), None)
        sim.insert([1, 3])
        self.assertNotEqual(sim.find_simplex([1, 3]), None)

    def test_3(self):
        '''
        Add [1,2] and then add [1,3]
        [1,2 should still be present]
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4])
        self.assertNotEqual(sim.find_simplex([1, 2]), None)
        sim.insert([1, 3])
        self.assertNotEqual(sim.find_simplex([1, 3]), None)
        self.assertNotEqual(sim.find_simplex([1, 3, 4]), None)

    def test_4(self):
        '''
        Get simplices of given dimensions 1 (Vertices)
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4])
        self.assertEqual(sim.get_simplices(dim=0), [[1], [2], [3], [4]])

    def test_5(self):
        '''
        Get simplices of given dimension 2 (Edges)
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4])
        exp = sim.get_simplices(dim=1)
        act = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        print(exp)
        print(act)
        # print(sim.get_simplices(dim=1))
        #self.assertEqual(exp, act)

    def test_6(self):
        '''
        Check filtration values
        '''
        sim = SimplexTree()

        expected = 4.0
        sim.insert([1, 2, 3, 4], expected)
        # sim.print_tree()
        actual = sim.filtration([1, 2, 3, 4])
        self.assertEqual(expected, actual)

    def test_7(self):
        '''
        Update filtration_value for existing simplex
        '''
        sim = SimplexTree()

        sim.insert([1, 2, 3, 4], 0.0)
        expected = 4.0
        sim.insert([1, 2, 3, 4], expected)
        # sim.print_tree()
        actual = sim.filtration([1, 2, 3, 4])
        # print(actual)
        # self.assertEqual(expected, actual)

    def test_8(self):
        '''
        Find boundary operator
        '''
        sim = SimplexTree()

        sim.insert([1, 2, 3, 4], 0.0)

        expected = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
        # sim.print_tree()
        actual = sim.compute_boundaries([1, 2, 3, 4])
        # print(actual)
        self.assertEqual(expected, actual)

    def test_9(self):
        '''
        Get Vertices
        '''
        sim = SimplexTree()

        sim.insert([1, 2, 3, 4], 0.0)

        expected = [[1], [2], [3], [4]]
        # sim.print_tree()
        actual = sim.get_vertices()
        # print(actual)
        self.assertEqual(expected, actual)

    def test_10(self):
        '''
        Get dimension
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = 3
        actual = sim.getdimension()

        self.assertEqual(expected, actual)

    def test_11(self):
        '''
        Get num of vertices
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = 4
        actual = sim.num_vertices()

        self.assertEqual(expected, actual)

    def test_12(self):
        '''
        num of simplices
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = 15
        actual = sim.num_simplices()

        self.assertEqual(expected, actual)

    def test_13(self):
        '''
        skeleton
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = [[1], [2], [3], [4], [1, 2], [
            1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        actual = sim.get_skeleton(1)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
