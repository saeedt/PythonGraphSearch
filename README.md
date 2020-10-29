# Python Graph Search Algorithms
Several graph search algorithms based on Dijkstra's algorithm are implemented in Python. I implemented a searchable graph in JSON format which is stored in a [pandas](https://pandas.pydata.org) DataFrame to improve the performance.
The graph files are stored in graph folder. Any data from [OpenStreetMap](https://www.openstreetmap.org) can be used to build the graph.

## Data Converter
`dataConverter.py` is a python script that reads a CSV file and converts it to JSON for the other modules to use. You can download the data for your region of interest from [OpenStreetMap](https://www.openstreetmap.org) project. I used [osm2pgrouting](https://github.com/pgRouting/osm2pgrouting) to import it to a spatially enabled [PostgreSQL](https://www.postgresql.org/) database. Then, the table 'ways_vertices_pgr' where the edges are stored can be converted to CSV. `source, target, x1, y1, x2, y2, dist` are the required columns in the CSV file.

## Dijkstra's shortest path algorithm
`Dijkstra.py` finds the shortest distance between two nodes in the graph identified by their node IDs.

## Multi-Threaded Dijkstra's (MTD) algorithm
The median problem is a popular problem in network location introduced by Hakimi (1964). MTD algorithm finds the median (i.e. node with the minimum total weighted distance to a set of demand points) of a weighted graph. MTD algorithm proposed by Ghanbartehrani and Porter (2019) in the paper titled [An efficient algorithm for solving the median problem on real road networks](https://www.tandfonline.com/doi/abs/10.1080/0305215X.2019.1631305) is the most efficient optimal solution method for this [NP-Hard](https://en.wikipedia.org/wiki/NP-hardness) problem.
MTD is a scalable algorithm tested on real road networks with up to [28 million nodes](https://digitalcommons.georgiasouthern.edu/pmhr_2016/12/). The 28-milion node experiment was performed on a solver implemented in Java and executed on [server JRE](https://www.oracle.com/java/technologies/javase-server-jre8-downloads.html), so do not expect such performance on the Python implementation provided here in `MTDalgorithm.py`.
I am currently working on a high performance [Julia](https://julialang.org/) implementation of the MTD algorithm based on a similar graph representation.

## Clustering heuristics for solving the P-Median problem
`pMedian.py` is a clustering heuristic based on [Klincewicz (1991)](https://www.sciencedirect.com/science/article/abs/pii/037722179190090I) heuristic for p-hub median problem. The clustering algorithm is used in [(Ghanbartehrani & Porter, 2018)](https://digitalcommons.georgiasouthern.edu/pmhr_2018/6/) to solve a p-median problem with over 3,000 demand points and 150 facilities, on a road network with over 28 million nodes.

## The sample graph
`TestData.csv` and `graph.json` files in `graph` folder are the real road network for the city of Rockford, Illinois retrieved from [OpenStreetMap](https://www.openstreetmap.org) project. The graph consists of 19,836 nodes and 27,970 edges.

## Coming soon: visualization
I tried [geoplot](https://residentmario.github.io/geoplot/index.html) and [geopandas](https://geopandas.org/) to visualize the demand points and facility locations on map. I spent hours just to get everything installed (had to install anaconda, reset my environment, and used some advice from [this](https://github.com/ResidentMario/geoplot/issues/38) thread to resolve conflicts) just to see how disappointing the plots look compared to what [LeafLet](https://leafletjs.com/) generates with just a few lines of code and a 650 KB library.
I will add an interactive data visualization module in JavaScript/LeafLet soon.
