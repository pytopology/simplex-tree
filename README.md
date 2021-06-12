## Simplex tree
This library contains the implementation of **Simplex Tree** data structure which is used to store the simplicial complex. The implementation is completely based on the research paper "The Simplex Tree: An Efficient Data Structure for General Simplicial Complexes" by Jean-Daniel Boissonnat, Clément Maria (https://hal.inria.fr/file/index/docid/707901/filename/RR-7993.pdf)

![image](https://user-images.githubusercontent.com/7954909/121715814-f0799000-cafc-11eb-8c73-4a8615b13db7.png)


## About Project
This project is a part of coursework [E0 207 : Computational Topology : Theory and Applications](https://www.csa.iisc.ac.in/~vijayn/courses/CTTA/index.html) offered at CSA, Indian Institute of Science.

### Installation
```
pip install pytopology
```

### Example Usage
```
from pytopology import SimplexTree

simp = SimplexTree()
simp.insert([1,2,3],4.)
simp.printTree()
```
**Output**
```
Simplex: [1] Filtration value : 2.0
Simplex: [1, 2] Filtration value : 3.0
Simplex: [1, 2, 3] Filtration value : 4.0
Simplex: [1, 3] Filtration value : 4.0
Simplex: [2] Filtration value : 3.0
Simplex: [2, 3] Filtration value : 4.0
Simplex: [3] Filtration value : 4.0
```

### Visualizing the Simplex 
```
from pytopology import SimplexTree

simp = SimplexTree()
sim.insert([1, 2, 3])
sim.insert([2, 3, 4, 5])
sim.insert([6, 7, 9])
sim.insert([7, 8])
sim.insert([10])
simp.draw_simplex3D()
```
![image](https://github.com/pytopology/simplex-tree/blob/main/dim3.gif)
![image](https://github.com/pytopology/simplex-tree/blob/main/dim2.gif)
![image](https://github.com/pytopology/simplex-tree/blob/main/dim1.gif)
![image](https://github.com/pytopology/simplex-tree/blob/main/dim0.gif)

## Operations on Simplicial Complex
- Insert
- Find (Query)
- Boundary
- Print
- Filtration (with recursive propagation)
- Visualization 
- Get Dimension
- NumVertices, NumSimplices, Skeleton
- CoFace, Star, Link 

## Contributors
- Ashish Kankal ([@ashishkankal](https://github.com/ashishkankal))
- Karan Gupta([@karan25gupta](https://github.com/karan25gupta))
- Vivek A([@vivek1kerala7](https://github.com/vivek1kerala7))
