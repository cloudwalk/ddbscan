Discrete DBSCAN
===============

This is a version of `DBSCAN`_ clustering algorithm optimized for discrete, bounded data, reason why we call it Discrete DBSCAN (DDBSCAN). The base for the current implementation is from `this source`_. The algorithm code is in file ``ddbscan/ddbscan.py`` and can easily be read. The main algorithm itself is in method ``compute()``, and can be understood following the links above or reading papers describing it.

Another feature of this implementation is that it is designed towards online learning. As a result, when we add points to our DDBSCAN object, we must pass one point each time to method ``add_point``. See :ref:`usage_section` below.

Optimization for discrete and bounded data
------------------------------------------

Our main optimization to the vanilla algorithm described in the links above is based on the fact that for discrete and bounded data, we expect
to see many times the same point occurring, so we can keep track of how many times the point ocurred and optimize our algorithm to use that
information.

To speed up insertions of new points and computation of clusters, each DDBSCAN object keeps, for each point, the index of its neighbours and
the neighbourhood size (the sum of the counts of the neighbours points). So, when we insert a new point, we see if it is an already existing pair
and just increment its counter and the neighbourhood size of its neighbours. We recompute a KDTree with the points in case a new pair is
inserted, updating the point data for its neighbours.

Parameters
----------

A DBSCAN model has two parameters:

-  ``min_pts``: minimum amount of neighbours of a point to create a cluster.
-  ``eps`` : radius to look for neighbours.

By tunning the two parameters we are, in fact, setting the anomaly (outlier) detection sensitiveness. A greater value for ``min_pts`` implies that to recognize a new pattern as a cluster, instead of an anomaly, we must see a larger amount of points with that pattern. A greater value for ``eps`` implies bigger clusters can form easier, so that points in less dense areas can be recognized as clusters members given this large ``eps``. Given the importance of tunning this parameters, we have a method to set them, called ``set_params()``, which updates the internal state of the model accordingly.

Install
-------

To just install the package the easist way is to use pip:

.. code-block:: console

    $ pip install ddbscan

Another option is to clone this repo and run

.. code-block:: console

    $ python setup.py install

To run the tests:

.. code-block:: console

    $ python setup.py test


.. _usage_section:
Usage
-----

A typical example would be as following:

.. code-block:: python

    import ddbscan

    # Create a DDBSCAN model with eps = 4 and min_pts = 5
    scan = ddbscan.DDBSCAN(2, 5)    

    # Add points to model
    data = [[1,  2], [2,  2], [1,  3], [2, 3], [3, 3], [8, 9],
            [7,  6], [9,  7], [6, 9], [6, 8], [5, 5], [7, 8]]

    for point in data:
        scan.add_point(point=point, count=1, desc="")

    # Compute clusters
    scan.compute()

    print 'Clusters found and its members points index:'
    core_number = 0
    for core, reachable in scan.clusters:
        print '=== Core %d ===' % core_number
        print 'Core points index: %s' % list(core)
        print 'Reachable points index: %s' % list(reachable)
        core_number += 1

    print '\nCluster assigned to each point:'
    for i in xrange(len(scan.points)):
        print '=== Point: %s ===' % scan.points[i]
        print 'Cluster: %2d' % scan.points_data[i].cluster,
        # If a point cluster is -1, it's an anomaly
        if scan.points_data[i].cluster == -1:
            print '\t <== Anomaly found!'
        else:
            print


License
-------

::

    The MIT License (MIT)

    Copyright (c) 2014 CloudWalk, Inc.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


.. _DBSCAN: http://en.wikipedia.org/wiki/DBSCAN
.. _this source: http://cjauvin.blogspot.com.br/2014/06/dbscan-blues.html