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
        The container should be a dict that maps the specific state of the
        Markov chain to the specific instantiation of the Vertex that
        encapsulates that state

        TODO: Make sure to incorporate the empty graph case.
        """
        # Our container of all the vertices in this Graph
        self._vertices = {}

    @property
    def vertices(self):
        """Getter for a graph that returns an immutable container of the
        vertices in said graph
        """
        return frozenset(self._vertices.keys())

    def add_vertex(self, state):
        """Method to add another Vertex to this Graph. Simply store a newly
        instantiated Vertex in our container
        """
        # TODO: make sure that the state can be any value?
        # Create a new Vertex and add the (k, v) pair of mapping state to
        # actual Vertex to our Graph
        self._vertices[state] = Vertex(state)

    def __contains__(self, state):
        """Method overriding. Make sure that we can quickly check to see if
        a given state is contained in the graph
        """
        return state in self._vertices.keys()

    def __getitem__(self, state):
        """Contains method for our Graph class. Make sure that we can quickly
        access any given state in our graph
        """
        # attempt to hash the given state to return its corresponding Vertex
        try:
            return self._vertices[state]
        except ValueError:
            raise KeyError(f"State {repr(state)} is not in the Graph")

    def compute_probabilities(self):
        """Method to traverse our graph entirely and compute the
        probabilities of each of the paths
        """
        raise NotImplementedError()


"""My implementation of a Vertex that will be used as containers to store
'states' in our Graph Class.

Models a network of nodes where the nodes (vertices) are connected by edges
"""


class Vertex:
    def __init__(self, state):
        """Our constructor for our Vertex class.

        Vertices should contain the current state of the Markov chain in which
        we are in as well of a storage container of all the outgoing edges that
        are directed from this Vertex to another Vertex
        """
        # Our current state of history in regards to
        self._state = state
        # Our container for possible next states which is encapsulated by
        # dictionary mappings of tokens to Edges
        self._outgoing_edges = {}
        # TODO: may need to add another dict for fast lookups that maps Edge
        #  objects to probabilities

    @property
    def state(self):
        """Getter for Vertex that returns the current state (differentiates
        vertices from one another).
        """
        return self._state

    @property
    def outgoing_edges(self):
        """Getter for Vertex that returns an immutable dictionary of all the
        outgoing edges from this Vertex
        """
        return frozenset(self._outgoing_edges.items())

    def add_edge(self, dest, token):
        """Method to add a connection from the current node to the
        destination node that should already be instantiated.
        """
        # Null check on the destination vertex
        if dest:
            self._outgoing_edges[token] = Edge(dest, token, 0)
        else:
            raise ValueError("Error: dest vertex hasn't been instantiated")


"""My implementation of an Edge that will be used to connect Vertices in a
Graph Class.

Models connections between vertices with directed edges.
"""


class Edge:
    def __init__(self, vertex, token, probability=0):
        """Our constructor for an edge.

        Edges have a vertex attribute in which it is the vertex to which the
        edge is directed. They also have token attributes which simulate our
        choices of paths for the Markov chain graph. Lastly they have the
        probability attribute to simulate our statistically random choices.
        """
        # Instance attributes
        self._vertex = vertex
        self._token = token
        self._probability = probability

    @property
    def vertex(self):
        """Getter that returns the vertex to which this Edge is directed"""
        return self._vertex

    @property
    def token(self):
        """Getter that returns the token to which this Edge signifies"""
        return self._token

    @property
    def probability(self):
        """Getter that returns the probability in which this Edge will be
        chosen in a path algorithm"""
        return self._probability

    @probability.setter
    def probability(self, probability):
        """Setter for our probability attribute.

        In the traversal algorithm of our Graph, this will only be set once.
        """
        # Make sure that the probability has not already been set
        if self._probability == 0:
            self._probability = probability
        else:
            raise RuntimeError("Error: This Edge already has set probability")
