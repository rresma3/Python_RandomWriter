"""Final project: Random Writer that can save its model.

NOTE: This is a long file, however I strongly recommend you read the
whole thing BEFORE starting on the project.

In this project you will write a "random writer": a program that
builds a statistical model of some data and then outputs a stream of
data that is similar to the original but randomly generated. Here is
how we will do it: [The idea for this assignment is from an assignment
that Dr Calvin Lin uses for CS314H. He was nice enough to let me use
his text to explain it.]

Imagine taking a book, such as Tom Sawyer, and determining the
probability with which each character occurs. You'd probably find that
spaces are the most common character, followed by the character "e",
etc. Given these probabilities, which we will call a Level 0 analysis,
you could randomly produce text that, while not resembling English,
would have the property that the characters would likely occur in the
same proportions as they do in Tom Sawyer. For example, here's what
you might produce:

  rla bsht eS ststofo hhfosdsdewno oe wee h .mr ae irii ela iad o r te
  ut mnyto onmalysnce, ifu en c fDwn oee

Now imagine doing a slightly more sophisticated analysis, a Level 1
analysis, that determines the probability with which each character
follows every other character. You would probably discover that "h"
follows "t" more frequently than "x" does, and you would probably
discover that a space follows a period more frequently than a comma
does.  With this new analysis, you could use the probabilities from
Tom Sawyer to randomly pick an initial character and then repeatedly
choose the next character based on the previous character and the
probabilities provided by the analysis. Your new text might look like
the following, which looks a bit more like English than the previous
example:

  "Shand tucthiney m?" le ollds mind Theybooue He, he s whit Pereg
  lenigabo Jodind alllld ashanthe ainofevids tre lin-p asto oun
  theanthadomoere

We can generalize these ideas to a Level k analysis that determines
the probability with which each character follows every possible
sequence of k characters. For example, a Level 5 analysis of Tom
Sawyer would show that "r" follows "Sawye" more frequently than any
other character. After a Level k analysis, you'd be able to produce
random text by always choosing the next character based on the
previous k characters -- which we will call the state -- and based on
the probabilities produced by your analysis.

For relatively small values of k (5-7), the randomly generated text
begins to take on many of the characteristics of the source text.
While it still will not produce legal English, you will be able to
tell that it was derived from Tom Sawyer instead of Harry Potter. As
the value of k increases, the text looks increasingly like English.
Here are some more examples:

Level 2:
  "Yess been." for gothin, Tome oso; ing, in to weliss of an'te cle -
  armit.  Paper a comeasione, and smomenty, fropech hinticer, sid, a
  was Tom, be such tied. He sis tred a youck to themen

Level 4:
  en themself, Mr. Welshman, but him awoke, the balmy shore.  I'll
  give him that he couple overy because in the slated snuffindeed
  structure's kind was rath.  She said that the wound the door a fever
  eyes that WITH him.

Level 6:
  people had eaten, leaving. Come - didn't stand it better judgment;
  His hands and bury it again, tramped herself! She'd never would
  be. He found her spite of anything the one was a prime feature
  sunset, and hit upon that of the forever.

Level 8:
  look-a-here - I told you before, Joe.  I've heard a pin drop.  The
  stillness was complete, how-ever, this is awful crime, beyond the
  village was sufficient.  He would be a good enough to get that
  night, Tom and Becky.

Level 10:
  you understanding that they don't come around in the cave should get
  the word "beauteous" was over-fondled, and that together" and
  decided that he might as we used to do - it's nobby fun. I'll learn
  you."

We can also generalize this idea to use words in place of characters
as the "tokens" of the model. In fact we can generalize this process
to work over any sequence of values of any type. The states are then
short sequences of values.

Formally, the model we are building here is called a Markov Chain. A
Markov chain is a directed graph where every node is a state and every
outgoing edge from a node is a possible token to find while in that
state. The edges have probabilities that define how likely it is to
follow that edge. The probability of all the edges leaving a node
should sum to 1.

With this graph we can generate output by picking a random starting
node and then picking an outgoing edge based on the probabilities,
outputting it's associated token, and repeating the process based on
the node at the other end of the edge.

More concretely you can think of being in a state represented by a
string "th". We would then look at the probability that each other
letter would follow "th". "e" is likely to be very common; "x" not so
much. If we generate the "e", we are in state "he" and we check
probabilities based on that state.

Feel free to discuss the Markov chain with one another or look it
up. However you should not discuss how to implement it or copy an
existing implementation.

NOTE: This module can be used in various modes (level, tokenization,
etc). However, you should NOT need to reimplement large blocks of code
for each case. Instead, think about what actually changes from mode to
mode and use conditionals around only those part. You may even want to
write some utility methods which perform some abstract operations in
the appropriate way for the current mode. In the end, just remember
how much I hate duplicated or messy code as you handle all the cases.

"""

"""You will be turning in this assignment as a ZIP file, since you
will need to turn in 2 different modules (final.py and graph.py).
"""

"""TODO: Create a Tokenization enum with values: word, character,
byte, none (name them exactly this; do not capitalize). Use the
enumeration support in the standard library. The tokenization modes
have the following meanings:

word: Interpret the input as UTF-8 and split the input at any
  white-space characters and use the strings between the white-space
  as tokens. So "a b" would be ["a", "b"] as would "a\n b".

character: Interpret the input as UTF-8 and use the characters as
  tokens.

byte: Read the input as raw bytes and use individual bytes as the
  tokens.

none: Do not tokenize. The input must be an iterable.

"""

"""TODO: Create a module called 'graph' (make sure the file name is exactly
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
turn in.

"""

"""In implementing the algorithms required for this project you should
not focus too much on performance however you should make sure your
code can train on a large data set in a reasonable time. For instance,
a 6MB input file on level 4 should not take more than 10 seconds.
Similarly you should be able to generate output quickly; 5,000 tokens
per second or better. These should be easy to meet without any
optimization if you use the correct data structures (e.g., dicts when
you need fast lookup by a key).

You can get some test input from http://www.gutenberg.org/. You may
want to use the complete works of Shakespeare:
http://www.gutenberg.org/cache/epub/100/pg100.txt

"""
from enum import Enum, auto
import graph


class Tokenization(Enum):
    word = auto()
    character = auto()
    byte = auto()
    none = None

    @classmethod
    def is_proper_enum(cls, item):
        """Class Method that tests whether or not item is a proper
        enumeration
        """
        return item is cls.word or item is cls.character or item is \
            cls.byte or item is cls.none or item is cls.none.value


class RandomWriter(object):
    """A Markov chain based random data generator.
    """

    def __init__(self, level, tokenization=None):
        """Initialize a random writer.

        Args:
          level: The context length or "level" of model to build.
          tokenization: A value from Tokenization. This specifies how
            the data should be tokenized.

        The value given for tokenization will affect what types of
        data are supported.

        """
        # Error Check for proper input to the constructor
        if level < 0:
            raise ValueError(f"Error: level {repr(level)} must be positive")
        if not Tokenization.is_proper_enum(tokenization):
            raise ValueError(f"Error: tokenization {repr(tokenization)} must "
                             f"be of acceptable type")
        # instance attributes
        self._level = level
        self._tokenization = tokenization
        # initialize our Markov Chain
        self.chain = graph.Graph()
        # initialize our probability sum container to hold the total sum of
        # all outgoing edge weights for our chain vertices
        self.prob_sums = {}

    @property
    def level(self):
        """Getter that returns the given RandomWriter's level attribute.
        """
        return self._level

    @property
    def tokenization(self):
        """Getter that returns the given RandomWriter's tokenization
        attribute.
        """
        return self._tokenization

    def add_chain(self, data):
        """Function to add a new state to our Markov Chain, uses our Graph's
        API to do so.

        NOTE: state should be a tuple containing k-level amount of tokens,
        make sure to unpack correctly
        """
        # add a new vertex to our graph rep. of the chain
        self.chain.add_vertex(data)
        # add new entry for dictionary of (vertex, total_outgoing_edges) pairs
        self.prob_sums[data] = 0

    def has_conn(self, source, dest):
        """Function to test whether or not two chains in the Markov Chain
        already have a connection
        """
        return self.chain[source].has_edge(dest[-1])

    def get_conn(self, source, dest):
        """Function to return the edge that connects two chains in the Markov
        Chain
        """
        return self.chain[source].get_edge(dest[-1])

    def _incr_prob_sum(self, state):
        """Function to increment the number of outward connection of edges
        for a given state.
        """
        self.prob_sums[state] += 1

    def add_conn(self, source, dest, token):
        """Function to build an edge from the source state to the destination
        state with token specified.
        """
        # add an edge from source's vert obj to dest's vert obj
        self.chain[source].add_edge(self.chain[dest], token)
        # add 1 to the number of outgoing edges from the source destination
        self._incr_prob_sum(source)

    def generate(self):
        """Generate tokens using the model.

        Yield random tokens using the model. The generator should
        continue generating output indefinitely. This means we will cycle
        over multiple vertices

        It is possible for generation to get to a state that does not
        have any outgoing edges. You should handle this by selecting a
        new starting node at random and continuing.

        """
        # TODO: GENERATOR OBJ FOR ONCE WE HAVE OUR GRAPH
        raise NotImplementedError

    def generate_file(self, filename, amount):
        """Write a file using the model.

        Args:
          filename: The name of the file to write output to.
          amount: The number of tokens to write.

        For character or byte tokens this should just output the
        tokens one after another. For any other type of token a space
        should be added between tokens. Use str to convert values to
        strings for printing.

        Do not duplicate any code from generate.

        Make sure to open the file in the appropriate mode.
        """
        # TODO: OUTPUT GENERATOR YIELDED RANDOMIZED TOKENS TO FILE
        raise NotImplementedError

    def save_pickle(self, filename_or_file_object):
        """Write this model out as a Python pickle.

        Args:
          filename_or_file_object: A filename or file object to write
            to. You need to support both.

        If the argument is a file object you can assume it is opened
        in binary mode.

        """
        raise NotImplementedError

    @classmethod
    def load_pickle(cls, filename_or_file_object):
        """Load a Python pickle and make sure it is in fact a model.

        Args:
          filename_or_file_object: A filename or file object to load
            from. You need to support both.
        Return:
          A new instance of RandomWriter which contains the loaded
          data.

        If the argument is a file object you can assume it is opened
        in binary mode.

        """
        raise NotImplementedError

    def train_url(self, url):
        """Compute the probabilities based on the data downloaded from url.

        Args:
          url: The URL to download. Support any URL supported by
            urllib.

        This method is only supported if the tokenization mode is not
        none.

        Do not duplicate any code from train_iterable.

        """
        raise NotImplementedError

    def _gen_tokenized_data(self, data, size):
        """Helper function to generate tokens of proper length based on the
        level specified by this RandomWriter.

        The windows are produced by sliding a window over the input data
        which should be an iterable.

        if tokenization is character/word then data is a string which is
        iterable
        else if tokenization is byte then data is a bytestream

        NOTE: code taken from Arthur Peters' windowed() function in
        final_tests.py, Thanks Mr. Peters!

        TODO: handle k = 0 level case
        """
        # empty window to add elements to
        window = list()
        # iterate over the elements in the iterable
        for elem in data:
            # check if the size of the window is in the proper window
            if len(window) < size:
                # if so then add the next word/char/byte/token to the window
                window.append(elem)
            else:
                # otherwise, pop front and add to back, sliding the window down
                # by one unit
                window.pop(0)
                window.append(elem)
            # if the window has reached specified size, yield the proper state
            if len(window) == size:
                # tokenize by string
                if self.tokenization is Tokenization.character or \
                        self.tokenization is Tokenization.word:
                    yield "".join(window)
                # tokenize by byte
                elif self.tokenization is Tokenization.byte:
                    yield b"".join(window)
                # simply yield another iterable
                else:
                    yield tuple(window)

    def _data_type_check(self, data):
        """Helper function to make sure that the data is in the correct form
        for this RandomWriter's Tokenization

        If the tokenization mode is none, data must be an iterable. If
        the tokenization mode is character or word, then data must be
        a string. Finally, if the tokenization mode is byte, then data
        must be a bytes. If the type is wrong raise TypeError.
        """
        # if in character or word tokenization, data must be a str
        if self.tokenization is Tokenization.character or self.tokenization \
                is Tokenization.word:
            return isinstance(data, str)
        # if in byte tokenization, data must by raw bytes
        elif self.tokenization is Tokenization.byte:
            return isinstance(data, bytes)
        # if in none tokenization, data must be an iterable
        elif self.tokenization is Tokenization.none or self.tokenization is \
                Tokenization.none.value:
            return hasattr(data, '__iter__')
        # something went wrong with the constructor
        else:
            raise TypeError("Error: this RandomWriter does not have a proper "
                            "tokenization")

    def _build_markov_chain(self, states):
        """Helper function to help build the Markov Chain graph and compute
        the probabilities based on a generator of states w k-level lengths
        """
        # iterate through our states two at a time, creating our graph and
        # using the Markov chain algorithm to construct our probabilities
        try:
            # pop the first state from the generator and add it to the
            # initially empty chain
            old_state = next(states)
            self.add_chain(old_state)
        except StopIteration:
            raise RuntimeError("empty generator! empty input string or we "
                               "messed up the conversion of iterables")
        # iterate through the rest of the states
        for new_state in states:
            # does the next state already exists in the Markov Chain
            if new_state in self.chain:
                # does the old state already have a connection to the new state
                if self.has_conn(old_state, new_state):
                    # increment the counter of occurrences for edge's token
                    self.get_conn(old_state, new_state).incr_weight(1)
                else:
                    # create a new connection between old and new states
                    self.add_conn(old_state, new_state, new_state[-1])
            # the next state is brand new and we need a new connection
            else:
                # build a new chain to add the the Markov chain
                self.add_chain(new_state)
                # add a connection from the old chain to the new chain
                self.add_conn(old_state, new_state, new_state[-1])
            # iterate to the next state
            old_state = new_state

    def train_iterable(self, data):
        """Compute the probabilities based on the data given.

        Try to avoid storing all that data at one time, but if it is way
        simpler to store it don't worry about it. For most input types
        you will not need to store it.
        """
        # type check on the input data
        if not self._data_type_check(data):
            raise TypeError(f"Error: data is not in correct form for this "
                            f"RW's mode -> {self.tokenization}")

        # if we are in word tokenization then split data along white spaces
        if self.tokenization is Tokenization.word:
            states = self._gen_tokenized_data(data.split(), self.level)
        # if we are in byte tokenization then split data by byte
        elif self.tokenization is Tokenization.byte:
            states = self._gen_tokenized_data((data[i:i+1] for i in range(
                len(data))), self.level)
        # otherwise, iterate over data normally to create new gen of states
        else:
            states = self._gen_tokenized_data(data, self.level)
        # build our Markov Chain based on the generator we've constructed from
        # the input data
        self._build_markov_chain(states)


"""Modules you will want to look at:
* enum
* pickle
* requests

You may use the requests if you like even though it is not in the
standard library. I will make sure it is installed on the testing
machine.

"""
