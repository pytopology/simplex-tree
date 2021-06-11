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
simp.insert([1,2,3,4])
simp.printTree()
```

### Visualizing the Simplex 
```
from pytopology import SimplexTree

simp = SimplexTree()
simp.insert([1,2,3,4])
simp.draw_simplex3D()
```
## Operations on Simplicial Complex
- Insert
- Find
- Boundary
- Print
- Get Filtration
- Visualization 
- Insert modifications (sorted order)
- Get Dimension
- NumVertices, NumSimplices, Skeleton

## WIP
- Visualization (Generate random points properly)
- Update filtration (recursively)
## Pending 
- Delete (***)
- CoFace, Star(Lower star , Upper star), Closure, Link (Lower Link, Upper Link)
- Persistance, Betti numbers (Optional)

## Contributors
Ashish Kankal 

Karan Gupta

Vivek A
