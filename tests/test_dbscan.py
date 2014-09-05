from nose.tools import assert_equals

import ddbscan

def test_add_new_points():
    scan = ddbscan.DDBSCAN(5, 10)

    # Add one point to ddbscan
    scan.add_point(point=[2,3], count=5, desc="First point.")

    # Test list size
    assert_equals(len(scan.points), 1)
    assert_equals(len(scan.points_data), 1)

    # Test first point data
    assert_equals(scan.points[0], [2,3])
    assert_equals(scan.points_data[0].desc, "First point.")
    assert_equals(scan.points_data[0].count, 5)
    assert_equals(scan.points_data[0].neighbourhood, [0])
    assert_equals(scan.points_data[0].size_neighbourhood, 5)

    # Add another point with a distance great than eps
    # Distance = Sqrt((4-2)^2 + (8-3)^2) ~=  5.38
    scan.add_point([4, 8], 9, "Second point.")

    # Test list size
    assert_equals(len(scan.points), 2)
    assert_equals(len(scan.points_data), 2)

    # First point data must be unchanged
    assert_equals(scan.points[0], [2,3])
    assert_equals(scan.points_data[0].desc, "First point.")
    assert_equals(scan.points_data[0].count, 5)
    assert_equals(scan.points_data[0].neighbourhood, [0])
    assert_equals(scan.points_data[0].size_neighbourhood, 5)

    # Test second point data
    assert_equals(scan.points[1], [4,8])
    assert_equals(scan.points_data[1].desc, "Second point.")
    assert_equals(scan.points_data[1].count, 9)
    assert_equals(scan.points_data[1].neighbourhood, [1])
    assert_equals(scan.points_data[1].size_neighbourhood, 9)

    # Add third point within eps of second one
    # Distance = Sqrt((5-4)^2 + (11-8)^2) ~=  3.16
    scan.add_point([5, 11], 2, "Third point.")
    assert_equals(len(scan.points), 3)
    assert_equals(len(scan.points_data), 3)

    # First point data must be unchanged
    assert_equals(scan.points[0], [2,3])
    assert_equals(scan.points_data[0].desc, "First point.")
    assert_equals(scan.points_data[0].count, 5)
    assert_equals(scan.points_data[0].neighbourhood, [0])
    assert_equals(scan.points_data[0].size_neighbourhood, 5)

    # Second point neighbourhood data must be changed
    assert_equals(scan.points[1], [4,8])
    assert_equals(scan.points_data[1].desc, "Second point.")
    assert_equals(scan.points_data[1].count, 9)
    assert_equals(scan.points_data[1].neighbourhood, [1,2]) # 1 is neighbour of 2
    assert_equals(scan.points_data[1].size_neighbourhood, 9 + 2)

    # Test third point data
    assert_equals(scan.points[2], [5,11])
    assert_equals(scan.points_data[2].desc, "Third point.")
    assert_equals(scan.points_data[2].count, 2)
    assert_equals(scan.points_data[2].neighbourhood, [1,2])
    assert_equals(scan.points_data[2].size_neighbourhood, 2 + 9)

def test_add_n_dimensional_point():
    scan = ddbscan.DDBSCAN(5, 10)

    # Add 3-D point to ddbscan
    scan.add_point(point=[2,3,5], count=2, desc="First point.")

    # Test points matrix dimension
    assert_equals(len(scan.points), 1)
    assert_equals(len(scan.points[0]), 3)
   
    # Test points_data list size
    assert_equals(len(scan.points_data), 1)

    # Add more points
    scan.add_point(point=[1,2,3], count=1, desc="Second point.")


def test_add_existing_point():
    scan = ddbscan.DDBSCAN(5, 10)

    # Add one point to ddbscan
    scan.add_point([2, 3], 5, "First point.")

    # Test list size
    assert_equals(len(scan.points), 1)
    assert_equals(len(scan.points_data), 1)

    # Test first point data
    assert_equals(scan.points[0], [2,3])
    assert_equals(scan.points_data[0].desc, "First point.")
    assert_equals(scan.points_data[0].neighbourhood, [0])
    assert_equals(scan.points_data[0].count, 5)
    assert_equals(scan.points_data[0].size_neighbourhood, 5)

    # Add same point to ddbscan, but with count = 8
    scan.add_point([2, 3], 8, "Changed point.")

    # List size must be unchanged
    assert_equals(len(scan.points), 1)
    assert_equals(len(scan.points_data), 1)

    # Must've change desc, count and size_neighbourhoodnos
    assert_equals(scan.points[0], [2,3])
    assert_equals(scan.points_data[0].desc, "Changed point.")
    assert_equals(scan.points_data[0].neighbourhood, [0])
    assert_equals(scan.points_data[0].count, 5 + 8)
    assert_equals(scan.points_data[0].size_neighbourhood, 5 + 8)

def test_set_params_simple():
    # Test parameters setting
    scan = ddbscan.DDBSCAN(5, 10)
    assert_equals(scan.eps, 5)
    assert_equals(scan.min_pts, 10)

    scan.set_params(2, 15)
    assert_equals(scan.eps, 2)
    assert_equals(scan.min_pts, 15)

def test_set_params_advanced():
    scan = ddbscan.DDBSCAN(5, 10)

    # Add three points
    scan.add_point(point=[2, 3], count=5, desc="First point.")
    scan.add_point([4, 8], 9, "Second point.")
    scan.add_point([5, 11], 2, "Third point.")

    # With eps=5, we know the neighbourhood and its size
    assert_equals(scan.points_data[0].size_neighbourhood, 5)
    assert_equals(scan.points_data[1].neighbourhood, [1,2]) # 1 is neighbour of 2
    assert_equals(scan.points_data[1].size_neighbourhood, 9 + 2)
    assert_equals(scan.points_data[2].neighbourhood, [1,2])
    assert_equals(scan.points_data[2].size_neighbourhood, 2 + 9)

    # Set eps to small value, so that no one has neighbours
    scan.set_params(2, 15)

    assert_equals(scan.points_data[0].neighbourhood, [0])
    assert_equals(scan.points_data[0].size_neighbourhood, 5)
    assert_equals(scan.points_data[1].neighbourhood, [1])
    assert_equals(scan.points_data[1].size_neighbourhood, 9)
    assert_equals(scan.points_data[2].neighbourhood, [2])
    assert_equals(scan.points_data[2].size_neighbourhood, 2)

    # Set eps to initial, to see if the values remains correct
    scan.set_params(5, 10)

    assert_equals(scan.points_data[0].size_neighbourhood, 5)
    assert_equals(scan.points_data[1].neighbourhood, [1,2]) # 1 is neighbour of 2
    assert_equals(scan.points_data[1].size_neighbourhood, 9 + 2)
    assert_equals(scan.points_data[2].neighbourhood, [1,2])
    assert_equals(scan.points_data[2].size_neighbourhood, 2 + 9)

    # Set eps to large value, so that everyone is neighbour of anyone
    scan.set_params(12, 12)

    assert_equals(scan.points_data[0].neighbourhood, [0, 1, 2])
    assert_equals(scan.points_data[0].size_neighbourhood, 16)
    assert_equals(scan.points_data[1].neighbourhood, [0, 1, 2])
    assert_equals(scan.points_data[1].size_neighbourhood, 16)
    assert_equals(scan.points_data[2].neighbourhood, [0, 1, 2])
    assert_equals(scan.points_data[2].size_neighbourhood, 16)

    # Set eps to initial, to see if the values remains correct
    scan.set_params(5, 10)

    assert_equals(scan.points_data[0].size_neighbourhood, 5)
    assert_equals(scan.points_data[1].neighbourhood, [1,2]) # 1 is neighbour of 2
    assert_equals(scan.points_data[1].size_neighbourhood, 9 + 2)
    assert_equals(scan.points_data[2].neighbourhood, [1,2])
    assert_equals(scan.points_data[2].size_neighbourhood, 2 + 9)

    # Add far away point
    scan.add_point(point=[18, 15], count=7, desc="Far away point.")

    # See if it affects the other points data
    scan.set_params(12, 12)

    assert_equals(scan.points_data[0].neighbourhood, [0, 1, 2])
    assert_equals(scan.points_data[0].size_neighbourhood, 16)
    assert_equals(scan.points_data[1].neighbourhood, [0, 1, 2])
    assert_equals(scan.points_data[1].size_neighbourhood, 16)
    assert_equals(scan.points_data[2].neighbourhood, [0, 1, 2])
    assert_equals(scan.points_data[2].size_neighbourhood, 16)

    scan.set_params(5, 10)

    assert_equals(scan.points_data[0].size_neighbourhood, 5)
    assert_equals(scan.points_data[1].neighbourhood, [1,2]) # 1 is neighbour of 2
    assert_equals(scan.points_data[1].size_neighbourhood, 9 + 2)
    assert_equals(scan.points_data[2].neighbourhood, [1,2])
    assert_equals(scan.points_data[2].size_neighbourhood, 2 + 9)

def test_compute_clusters():

    # Random generated data
    data = [[ 92, 109], [146, 245], [295,  42], [ 19, 116], [221, 273], [ 12, 122],
            [187,  72], [ 92,  79], [278, 282], [  6, 240], [295,  23], [184, 257],
            [116, 151], [263,   3], [217,  24], [ 87,  12], [170, 143], [148,  91],
            [205, 176], [ 17,  68], [122, 278], [272, 171], [ 33, 169], [ 95, 191],
            [158,  83], [288,  92], [206,  26], [ 94, 193], [ 83, 194], [273, 187],
            [240,  78], [ 55, 152], [ 78, 183], [215,  77], [ 41, 103], [225, 239],
            [ 94,  13], [170, 123], [187,   0], [237, 212], [ 36,   5], [ 69, 141],
            [ 97, 126], [210, 264], [ 12, 151], [151, 225], [ 75,  73], [224, 134],
            [  3, 150], [297, 236], [104,  19], [142,  45], [ 80, 175], [170,  76],
            [176, 281], [153, 223], [147, 181], [ 27,   6], [ 18,  89], [110, 122],
            [131, 170], [299, 275], [257, 134], [ 79, 166], [ 28, 262], [275,  77],
            [231,  14], [174,  65], [170,  43], [292, 228], [ 53,  29], [ 33, 288],
            [ 39, 104], [137,  21], [115, 174], [ 79, 217], [ 77, 195], [ 98, 115],
            [190,  53], [  8, 211], [227,  30], [119, 291], [139, 279], [ 53,  65],
            [120,  35], [112, 269], [188, 152], [ 91,  32], [204,   9], [ 12,  30],
            [125, 137], [167,  79], [135,  62], [ 60, 207], [ 26, 283], [ 48, 265],
            [189, 247], [162, 139], [246, 113], [125, 118]]

    # Expected output is based on sklearn DBSCAN implementation
    # Example:
    #
    # from sklearn.cluster import DBSCAN
    # import numpy
    #
    # scan = DBSCAN(eps=40, min_samples=5)
    # predictions = scan.fit_predict(data)
    # count_outliers = 0
    # for p in predictions:
    #     if p == -1:
    #         count_outliers = count_outliers + 1
    # count_clusters = max(predictions) + 1

    # Test with parameters eps=40 and min_pts=5
    scan = ddbscan.DDBSCAN(40, 5)

    for p in data:
        scan.add_point(p, 1, "Desc")

    scan.compute()

    count_outliers = 0
    for p in scan.points_data:
        if p.cluster == -1:
            count_outliers = count_outliers + p.count
    
    count_clusters = len(scan.clusters)

    assert_equals(count_outliers, 16)
    assert_equals(count_clusters, 3)

    # Test with parameters eps=30 and min_pts=2
    scan = ddbscan.DDBSCAN(30, 2)

    for p in data:
        scan.add_point(p, 1, "Desc")

    scan.compute()

    count_outliers = 0
    for p in scan.points_data:
        if p.cluster == -1:
            count_outliers = count_outliers + p.count
    
    count_clusters = len(scan.clusters)

    assert_equals(count_outliers, 2)
    assert_equals(count_clusters, 16)

    # Test with parameters eps=80 and min_pts=10
    scan = ddbscan.DDBSCAN(80, 10)

    for p in data:
        scan.add_point(p, 1, "Desc")

    scan.compute()

    count_outliers = 0
    for p in scan.points_data:
        if p.cluster == -1:
            count_outliers = count_outliers + p.count
    
    count_clusters = len(scan.clusters)

    assert_equals(count_outliers, 1)
    assert_equals(count_clusters, 1)

    # Test with parameters eps=10 and min_pts=5
    scan = ddbscan.DDBSCAN(10, 5)

    for p in data:
        scan.add_point(p, 1, "Desc")

    scan.compute()

    count_outliers = 0
    for p in scan.points_data:
        if p.cluster == -1:
            count_outliers = count_outliers + p.count
    
    count_clusters = len(scan.clusters)

    assert_equals(count_outliers, 100)
    assert_equals(count_clusters, 0)

def test_compute_clusters_repeated_points():

    data = [[ 3,  2], [ 3,  2], [ 6,  9], [ 0,  9], [ 2,  4], [ 9,  0], [ 0,  1],
            [ 4,  7], [ 4, 10], [ 7,  3], [ 6, 10], [ 6,  6], [ 6,  1], [ 2,  7],
            [ 1,  0], [ 3,  7], [ 3,  5], [ 4,  7], [ 4, 10], [ 1,  6], [ 5,  5],
            [ 1,  6], [ 9,  2], [ 6,  7], [ 4,  4], [ 0,  3], [ 7,  5], [ 7,  4],
            [ 3,  4], [ 3,  9], [10,  3], [ 5,  5], [ 0,  0], [ 6,  8], [ 9,  6],
            [ 9,  8], [ 1,  5], [ 4,  0], [ 7,  8], [ 3,  5], [ 8,  4], [ 5, 10],
            [10,  7], [ 2,  2], [ 3,  6], [ 8,  2], [ 2,  8], [ 8,  3], [ 2,  3],
            [ 1,  2], [ 8,  3], [ 8, 10], [ 5,  9], [10,  6], [ 5,  5], [ 4,  4],
            [ 9,  1], [ 5,  8], [ 2, 10], [ 5,  0], [ 4,  2], [ 1,  6], [ 9,  3],
            [ 3,  6], [10,  2], [ 5,  1], [10,  6], [ 5,  0], [ 9,  3], [ 4,  7],
            [ 4,  5], [ 6,  2], [ 4,  4], [10,  7], [ 5,  3], [ 6,  1], [ 5,  7],
            [ 8,  6], [ 3,  0], [ 2,  9], [ 5,  4], [ 3,  3], [ 1,  6], [ 7,  4],
            [ 2,  7], [10,  5], [ 5,  2], [ 3,  0], [ 6,  8], [ 6,  6], [ 1,  1],
            [ 4,  4], [ 5,  6], [ 4,  1], [ 9,  6], [ 7,  6], [ 2,  7], [ 6,  9],
            [ 8, 10], [ 2,  0], [ 9,  5], [ 0,  7], [ 1,  3], [10,  7], [ 7,  2],
            [ 3,  1], [10,  0], [ 6, 10], [ 2,  5], [ 5,  8], [ 6,  5], [ 9,  2],
            [10,  5], [ 4,  0], [ 5, 10], [ 9,  1], [ 5,  5], [ 0,  5], [ 3,  5],
            [10, 10], [ 8,  2], [ 8,  0], [ 5,  6], [ 4,  9], [ 5,  2], [ 9,  7],
            [ 7,  9], [ 2,  7], [10, 10], [ 1,  3], [ 7,  6], [ 2,  5], [ 5,  8],
            [ 6,  7], [ 5,  6], [ 8,  6], [ 4,  4], [ 6,  8], [ 0,  4], [ 7,  1],
            [ 1,  6], [10,  6], [ 0,  7], [ 7,  0], [ 1,  8], [ 5,  5], [ 0,  3],
            [ 9,  3], [ 6,  5], [ 0,  5], [ 8,  6], [10,  6], [ 6,  1], [ 1,  4],
            [ 3,  8], [ 4, 10], [ 5,  2], [ 2,  6], [ 0,  1], [ 1,  6], [ 9,  3],
            [ 8, 10], [ 6, 10], [ 6,  8], [10,  4], [10,  1], [ 8,  9], [ 1, 10],
            [ 6,  7], [ 5,  9], [ 0,  3], [ 0,  8], [ 7,  4], [ 8,  7], [ 7,  9],
            [ 1,  0], [ 6,  3], [ 7, 10], [ 8,  9], [ 1,  9], [10, 10], [10, 10],
            [ 2,  1], [ 1,  3], [10,  0], [ 6,  5], [ 6,  1], [ 1,  0], [ 9,  8],
            [ 6,  2], [ 6,  3], [ 7,  1], [10,  8], [ 1,  1], [ 3,  1], [ 6,  2],
            [ 1,  0], [ 4,  2], [ 6,  8], [ 1,  3]]

    # Test with parameters eps=5 and min_pts=5
    scan = ddbscan.DDBSCAN(5, 5)

    for p in data:
        scan.add_point(p, 1, "Desc")

    scan.compute()

    count_outliers = 0
    for p in scan.points_data:
        if p.cluster == -1:
            count_outliers = count_outliers + p.count
    
    count_clusters = len(scan.clusters)

    assert_equals(count_outliers, 0)
    assert_equals(count_clusters, 1)

    # Test with parameters eps=3 and min_pts=50
    scan = ddbscan.DDBSCAN(3 , 50)

    for p in data:
        scan.add_point(p, 1, "Desc")

    scan.compute()

    count_outliers = 0
    for p in scan.points_data:
        if p.cluster == -1:
            count_outliers = count_outliers + p.count
    
    count_clusters = len(scan.clusters)

    assert_equals(count_outliers, 31)
    assert_equals(count_clusters, 1)
