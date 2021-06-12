

from simplex_tree import SimplexTree

sim = SimplexTree()

sim.insert([1], 2.0)
sim.insert([3], 4.0)
sim.insert([2], 3.)

sim.insert([1, 2], 3.)
sim.insert([1, 3], 4.)
sim.insert([2, 3], 4.)

sim.insert([1, 2, 3], 4.)
# sim.insert([2, 3, 4, 5])
# sim.insert([6, 7, 9])
# sim.insert([7, 8])
# sim.insert([10])


sim.print_tree()

#sim.insert([4, 5])

# sim.get_simplices(1)

# sim.draw_simplex3D(0)
