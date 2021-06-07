import unittest
from simplex_tree import SimplexTree


class TestStringMethods(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
