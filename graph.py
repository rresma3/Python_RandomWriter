"""Create a module called 'graph' (make sure the file name is exactly
'graph.py') that contains class(es) and code that are used to represent and
manipulate the Markov chain graph. It should implement the Markov chain as an
abstract concept and not have any code specific to this usage. Also it should
use objects to represent the graph structure, instead of encoding relationships
as some opaque set of tables.

The API of the module is up to you, but it should be an API which I could use
to implement a different Markov-chain-related system without changing it. So
try to make the API generic and not specific to this application. I will be
grading the generality of the graph module.

NOTE: Do not optimized your graph representation. Just represent it in
the simplest way you can. That's how I implemented mine and it runs the
whole test suite in 9 seconds which is plenty fast enough for our
application and actually much faster than most implementations people
turn in."""


class Graph:
    def __init__(self):
        """Our constructor for the Graph class.

        Each graph should store a container of all the nodes in the graph.
        The container should be a dict that maps the specific data of a
        vertex to the specific instantiation of the Vertex that
        encapsulates that state

        """
        # Our container of all the vertices in this Graph, this dictionary
        # should map data to the vertices that encapsulate the data
        self._vertices = {}

    @property
    def vertices(self):
        """Getter for a graph that returns an immutable container of the
        vertices in said graph
        """
        return frozenset(self._vertices.keys())

    def add_vertex(self, data):
        """Method to add another Vertex to this Graph. Simply store a newly
        instantiated Vertex in our container
        """
        if data is None:
            raise TypeError("Error: data must be non-null")
        else:
            # Create a new Vertex and add the (k, v) pair of mapping data to
            # actual Vertex to our Graph
            self._vertices[data] = Vertex(data)

    def size(self):
        """Size method for our graph class. Allows us to quickly see the
        number of vertices in this graph"""
        return len(self._vertices)

    def __contains__(self, data):
        """Contains method overriding. Make sure that we can quickly check to
        see if a given data piece is contained in the graph
        """
        return data in self._vertices.keys()

    def __getitem__(self, data):
        """Get method overriding. Make sure that we can quickly
        access any given Vertex in our graph
        """
        # attempt to hash the given data to return its corresponding Vertex
        try:
            return self._vertices[data]
        except ValueError:
            raise KeyError(f"State {repr(data)} is not in the Graph")

    def print_graph(self):
        """Method to traverse our graph entirely and output all the vertices
        and edges for those vertices
        """
        for v in self.vertices:
            vert_obj = self._vertices[v]
            print(f"vertex: {v}")
            print(f"\t(data: {v}, v_object: {vert_obj})")
            print("\tcorresponding edges: ")
            for edge in vert_obj.outgoing_edges:
                edge_obj = vert_obj.get_edge(edge)
                print(f"\t\tedge: {edge}")
                print(f"\t\t\t(token: {edge}, e_object: {edge_obj})")
                print(f"\t\t\tweight: {edge_obj.weight}, dest: "
                      f"{edge_obj.dest_vertex}")


"""My implementation of a Vertex that will be used as containers to store
'states' in our Graph Class.

Models a network of nodes where the nodes (vertices) are connected by edges
"""


class Vertex:
    def __init__(self, data):
        """Our constructor for our Vertex class.

        Vertices should contain data as well of a storage container of all the
        outgoing edges that are directed from this Vertex to another Vertex
        """
        # Our current state of history in regards to
        self._data = data
        # Our container for edges that leave this vertex which is
        # encapsulated by dictionary mappings of tokens to Edges
        self._outgoing_edges = {}

    @property
    def data(self):
        """Getter for Vertex that returns the current state (differentiates
        vertices from one another).
        """
        return self._data

    @property
    def outgoing_edges(self):
        """Getter for Vertex that returns an immutable dictionary of all the
        outgoing edges from this Vertex
        """
        return frozenset(self._outgoing_edges.keys())

    def has_edge(self, edge_token):
        """Contains method. Make sure that we can quickly check to
        see if a given edge exists in our outgoing vertex
        """
        return edge_token in self._outgoing_edges.keys()

    def get_edge(self, edge_token):
        """Get method overriding. Make sure that we can quickly
        access any given Vertex in our graph
        """
        # attempt to hash the given data to return its corresponding Vertex
        try:
            return self._outgoing_edges[edge_token]
        except ValueError:
            raise KeyError(f"State {repr(edge_token)} is not an Edge")

    def add_edge(self, dest, token):
        """Method to add a connection from the current node to the
        destination node that should already be instantiated.
        """
        # Null check on the destination vertex
        if dest:
            self._outgoing_edges[token] = Edge(dest, token, 1)
        else:
            raise ValueError("Error: dest vertex hasn't been instantiated")


"""My implementation of an Edge that will be used to connect Vertices in a
Graph Class.

Models connections between vertices with directed edges.
"""


class Edge:
    def __init__(self, dest_vertex, token, weight=0):
        """Our constructor for an edge.

        Edges have a vertex attribute in which it is the vertex to which the
        edge is directed. They also have token attributes which simulate our
        choices of paths for the Markov chain graph. Lastly they have the
        probability attribute to simulate our statistically random choices.
        """
        # Instance attributes
        self._dest_vertex = dest_vertex
        self._token = token
        self._weight = weight

    @property
    def dest_vertex(self):
        """Getter that returns the vertex to which this Edge is directed"""
        return self._dest_vertex

    @property
    def token(self):
        """Getter that returns the token to which this Edge signifies"""
        return self._token

    @property
    def weight(self):
        """Getter that returns the probability in which this Edge will be
        chosen in a path algorithm"""
        return self._weight

    def incr_weight(self, amount):
        """Incrementer for our probability attribute.

        In the traversal algorithm of our Graph, this will be a counter
        """
        self._weight += amount
