"""my unit-testing file"""
import unittest
import final
import graph
import functools


class MyTests(unittest.TestCase):

    def test_tokenization1(self):
        temp = None
        self.assertTrue(final.Tokenization.is_proper_enum(temp))

    def test_tokenization2(self):
        temp = final.Tokenization.word
        self.assertTrue(final.Tokenization.is_proper_enum(temp))

    def test_constructor(self):
        rw = final.RandomWriter(1, final.Tokenization.word)

    def test_graph(self):
        g = graph.Graph()
        g.add_vertex(1)
        g.add_vertex(2)
        # print(g.vertices)
        for v in g.vertices:
            if v == 1:
                temp = g[v]
                temp.add_edge(g[2], '3')
                # print(temp)
                # print(temp.get_edge('3').dest_vertex)

    def test_bytes(self):
        print("TESTING BYTES:\n")
        rw = final.RandomWriter(1, final.Tokenization.byte)
        rw.train_iterable(b"\xfe\xff\x02\xfe\x03\xfe")
        print(rw.chain.vertices)
        rw.chain.print_graph()

    def test_words(self):
        print("TESTING WORDS:\n")
        rw = final.RandomWriter(1, final.Tokenization.word)
        rw.train_iterable("a the word the")
        print(rw.chain.vertices)
        rw.chain.print_graph()

    def test_char(self):
        print("TESTING CHARACTERS:\n")
        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("abcaea")
        print(rw.chain.vertices)
        rw.chain.print_graph()

    def test_none(self):
        print("TESTING NONE:\n")
        rw = final.RandomWriter(2, final.Tokenization.none)
        rw.train_iterable((1,2,3,4,5,5,4,3,2,1))
        # print(rw.chain.vertices)
        for v in rw.chain.vertices:
            print(v)
            print(rw.prob_sums[v])
        rw.chain.print_graph()


if __name__ == "__main__":
    unittest.main()
