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

        sim.insert([1, 2, 3, 4])
        expected = 4.0
        sim.update_filtration([1, 2, 3, 4], expected)
        actual = sim.filtration([2, 3, 4])
        self.assertEqual(expected, actual)

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
        Get Vertices
        '''
        sim = SimplexTree()

        sim.insert([1, 2, 3, 4], 0.0)

        # sim.print_tree()
        sim.delete([2, 4])
        actual = sim.find_simplex([2, 4])
        actual1 = sim.find_simplex([3, 4])
        actual2 = sim.find_simplex([2, 3, 4])
        actual3 = sim.find_simplex([1, 2, 3, 4])
        expected = None
        print(actual)
        self.assertEqual(expected, actual)
        self.assertNotEqual(expected, actual1)
        self.assertEqual(expected, actual2)
        self.assertEqual(expected, actual3)

    def test_11(self):
        '''
        Get Vertices
        '''
        sim = SimplexTree()

        sim.insert([1, 2, 3, 4], 0.0)

        # sim.print_tree()
        sim.delete([1, 2, 4])
        actual = sim.find_simplex([2, 4])
        actual1 = sim.find_simplex([3, 4])
        actual2 = sim.find_simplex([1, 2, 4])
        actual3 = sim.find_simplex([1, 2, 3, 4])
        expected = None
        # print(actual)
        self.assertNotEqual(expected, actual)
        self.assertNotEqual(expected, actual1)
        self.assertEqual(expected, actual2)
        self.assertEqual(expected, actual3)

    def test_12(self):
        '''
        Get Vertices
        '''
        sim = SimplexTree()

        sim.insert([1, 2, 3, 4], 0.0)
        sim.insert([5, 6, 7], 0.0)

        # sim.print_tree()
        ans = sim.link(7)
        expected = [[5], [6], [5, 6]]
        # print(actual)
        self.assertEqual(expected, ans)

    def test_13(self):
        '''
        Get dimension
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = 3
        actual = sim.getdimension()
        print(actual)

        self.assertEqual(expected, actual)

    def test_14(self):
        '''
        Get num of vertices
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = 4
        actual = sim.num_vertices()
        print(actual)

        self.assertEqual(expected, actual)

    def test_15(self):
        '''
        num of simplices
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = 15
        actual = sim.num_simplices()
        print(actual)

        self.assertEqual(expected, actual)

    def test_16(self):
        '''
        skeleton
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = [[1], [2], [3], [4], [1, 2], [
            1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
        actual = sim.get_skeleton(1)
        print(actual)

        self.assertEqual(expected, actual)

    def test_17(self):
        '''
        coface
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = [[1, 2], [1, 2, 3], [1, 2, 4], [1, 2, 3, 4]]
        actual = sim.coface([1, 2])
        print(actual)

        self.assertEqual(expected, actual)

    def test_18(self):
        '''
        star
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3, 4], 0.0)
        expected = [[1], [1, 2], [1, 3], [1, 4], [
            1, 2, 3], [1, 2, 4], [1, 3, 4], [1, 2, 3, 4]]
        actual = sim.coface([1])
        print(actual)

        self.assertEqual(expected, actual)

    def test_19(self):
        '''
        filtration
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3])
        #sim.insert([3, 4], 2.0)

        sim.update_filtration([1, 2, 3], 4.0)
        actual = sim.filtration([3, 2])
        #sim.update_filtration([1, 2, 3])
        self.assertEqual(4.0, actual)

    def test_20(self):
        '''
        filtration
        '''
        sim = SimplexTree()
        sim.insert([1, 2, 3])
        #sim.insert([3, 4], 2.0)

        sim.print_tree()

        sim.update_filtration([1, 2], 6.0)

        #sim.update_filtration([1, 2, 3])
        sim.print_tree()

    # def test_16(self):
    #     '''
    #     lower star
    #     '''
    #     sim = SimplexTree()
    #     sim.insert([1, 2, 3, 4], 0.0)
    #     expected = [[1],[1, 2],[1,3],[1,4],[1,2,3],[1,2,4],[1,3,4],[1,2,3,4]]
    #     actual = sim.coface([1])
    #     print(actual)

    #     self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
