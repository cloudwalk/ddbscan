from  scipy.spatial import cKDTree
import numpy as np

# In Python 3.* xrange become default range
try:
    xrange
except NameError:
    xrange = range

class PointData:
    """ 
    Struct for a data point. 
    Fields: 
    - count: number of points with that coordinates  
    - cluster: label of cluster. -1 is noise.
    - core: True if it's core point, False it it's reachable (or noise)
    - size_neighbourhood: number of points in the neighbourhood
    - neighbourhood: list of indices of points within eps
    - desc: latest description
    """
    
    def __init__(self, count, desc):
        self.count = count
        self.cluster = -1 #noise
        self.core = False
        self.neighbourhood = []
        self.size_neighbourhood = count # It contains itself
        self.desc = desc
        
class DDBSCAN:
    """ Class to create a DDBSCAN model using data discreteness to speed things up.
    
    Attributes:
        - eps: radius to look for neighbours
        - min_pts: minumum of neighbours to be core point
        - points: matrix m x n of points, when n is the point dimension
        - points_data: list of DataPoints
        - clusters: list of clusters with members indices
        - last_index: index of last data point
        - tree: kd-tree used to retrieve neighbourhood for points
    """
    
    def __init__(self, eps, min_pts):
        self.eps = eps
        self.min_pts = min_pts
        self.points_data = []
        self.points = []
        self.clusters = []
        self.last_index = 0 
        self.tree = None
        
    def add_point(self, point, count, desc):
        """ Add a new point (passed as a n-dimensional list [x, y, z, ...]) to model updating it's neighbours.
            It's description will be set to desc. 
        """
        self.last_index = self.points.index(point) if point in self.points else -1
        if self.last_index != -1: # If point already seem
            self.points_data[self.last_index].count = self.points_data[self.last_index].count + count
            self.points_data[self.last_index].desc = desc
            for neighbour_index in self.points_data[self.last_index].neighbourhood:
                self.points_data[neighbour_index].size_neighbourhood = \
                    self.points_data[neighbour_index].size_neighbourhood + count
        else:
            # Add point to list and update last_index
            self.last_index = len(self.points)
            self.points.append(point)
            
            # Create PointData
            self.points_data.append(PointData(count, desc))
            
            # Recreate tree
            self.tree = cKDTree(self.points)
            
            # Update neighbourhood list
            self.points_data[self.last_index].neighbourhood = self.tree.query_ball_point(point, self.eps)
            
            # Calculate size of neighbourhood and add this to their neighbourhood
            for neighbour_index in self.points_data[self.last_index].neighbourhood:
                if neighbour_index != self.last_index: # Update others in neighbourhood
                    self.points_data[self.last_index].size_neighbourhood = \
                        self.points_data[self.last_index].size_neighbourhood + self.points_data[neighbour_index].count
                    self.points_data[neighbour_index].neighbourhood.append(self.last_index)
                    self.points_data[neighbour_index].size_neighbourhood = self.points_data[neighbour_index].size_neighbourhood + count
    
    def set_params(self, eps, min_pts):
        """ Set params and update structures. """
        self.eps = eps
        self.min_pts = min_pts
        
        # Update data
        for i in xrange(len(self.points)):
            self.points_data[i].cluster = -1
            self.points_data[i].neighbourhood = self.tree.query_ball_point(self.points[i], self.eps)
            self.points_data[i].size_neighbourhood = 0
        
        # Update size -f neighbourhood
        for i in xrange(len(self.points)):
            for neighbour_index in self.points_data[i].neighbourhood:
                self.points_data[i].size_neighbourhood = \
                        self.points_data[i].size_neighbourhood + self.points_data[neighbour_index].count

    def compute(self):
        """ Compute clusters. """
        self.clusters = []
        num_cluster = -1
        visited = set()
        for i in xrange(len(self.points)):
            if i in visited:
                continue
            visited.add(i)
            num_neighbours = self.points_data[i].size_neighbourhood
            if num_neighbours >= self.min_pts:
                self.clusters.append(({i}, set())) # core
                num_cluster = num_cluster + 1
                self.points_data[i].cluster = num_cluster
                to_merge_in_cluster = set(self.points_data[i].neighbourhood)
                while to_merge_in_cluster:
                    j = to_merge_in_cluster.pop()
                    if j not in visited:
                        visited.add(j)
                        self.points_data[j].cluster = num_cluster
                        num_neighbours = self.points_data[j].size_neighbourhood
                        if num_neighbours >= self.min_pts:
                            to_merge_in_cluster |= set(self.points_data[j].neighbourhood)
                    if not any([j in c for c in self.clusters]):
                        self.points_data[j].cluster = num_cluster
                        num_neighbours = self.points_data[j].size_neighbourhood
                        if num_neighbours >= self.min_pts:
                            self.points_data[j].core = True
                            self.clusters[-1][0].add(j) # core
                        else:
                            self.points_data[j].core = False
                            self.clusters[-1][1].add(j) # reachable