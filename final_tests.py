# -*- coding: utf-8 -*-
"""Tests for CS109 Python Final Project.

This does not test for all the requirements of the assignment! So make
sure you test it yourself.

This entire set of tests should not take more than 30 seconds to run.
My implementation takes 9s (on an i5 at 3.3Ghz). My implementation is
not particularly optimized. Just make sure you are not interating any
sequences repeatedly when you don't need to or anything like that.
(HINT: Use dicts when you need to perform lookups)

Run this script using:
  python3.5 final_tests.py
It should work if you are in the same directory as your final.py and
graph.py files. If this does not work you may want to try:
  PYTHONPATH=[directory containing final.py and graph.py] python3.5 final_tests.py

NOTE: These tests use the internet to test train_url. So those tests
will fail if you do not have internet access.

"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code works with this exact version.

from contextlib import contextmanager
import tempfile
import os
import unittest
import itertools
import sys
from pathlib import Path

import final

# You may find some of the functions or code here useful in either
# your tests or your implementation. Feel free to use it, but of
# course cite and credit your source. (This is a hint, but I'm not
# telling you which function you need.)

@contextmanager
def nonexistant_filename(suffix=""):
    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as fi:
        filename = fi.name
    os.remove(filename)
    try:
        yield str(filename)
    finally:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

@contextmanager
def filled_filename(content, suffix=""):
    with tempfile.NamedTemporaryFile(mode="w" if isinstance(content, str) else "wb", suffix=suffix, delete=False) as fi:
        fi.write(content)
        filename = fi.name
    try:
        yield str(filename)
    finally:
        os.remove(filename)

def windowed(iterable, size):
    """Convert an iterable to an iterable over a "windows" of the input.

    The windows are produced by sliding a window over the input iterable.
    """
    window = list()
    for v in iterable:
        if len(window) < size:
            window.append(v)
        else:
            window.pop(0)
            window.append(v)
        if len(window) == size:
            yield tuple(window)

def contains_sequence(iteratable, sequence, length=10000, require_length=True, times=1):
    sequence = tuple(sequence)
    count = 0
    found = 0
    for window in itertools.islice(windowed(iteratable, len(sequence)), length):
        #print(window, count, sequence)
        count += 1
        if window == sequence:
            found += 1
            if found >= times:
                return True
    #if count < length-1 and require_length:
    #    raise AssertionError("Iterable did not contain enought values for check. Ran out at {}; needed {}.".format(count, length))
    return False


class RandomWriterTests(unittest.TestCase):
    """Some simple tests for RandomWriter.

    This is not an exhaustive test suite.

    """
    DEFAULT_LENGTH = 10090

    def assertContainsSequence(self, iteratable, sequence, length=None, times=1):
        length = length or self.DEFAULT_LENGTH
        lst = list(itertools.islice(iteratable, length + len(sequence)*2))
        if not contains_sequence(lst, sequence, length, times=times):
            self.fail("The given iterable must contain the sequence: {} at least {} times "
                      "(in the first {} elements)\nSample: {}".format(list(sequence), times, length, ", ".join(repr(x) for x in lst[:100])))

    def assertNotContainsSequence(self, iteratable, sequence, length=None):
        length = length or self.DEFAULT_LENGTH
        lst = list(itertools.islice(iteratable, length + len(sequence)*2))
        if contains_sequence(lst, sequence, length):
            self.fail("The given iterable must NOT contain the sequence: {} "
                      "(in the first {} elements)\nSample: {}".format(list(sequence), length, ", ".join(repr(x) for x in lst[:100])))

    def test_numeric_sequence(self):
        rw = final.RandomWriter(2)
        rw.train_iterable((1,2,3,4,5,5,4,3,2,1))
        self.assertNotContainsSequence(rw.generate(), [5,5,3])
        self.assertNotContainsSequence(rw.generate(), [1,2,5])
        self.assertNotContainsSequence(rw.generate(), [2,4])
        self.assertContainsSequence(rw.generate(), [3,4,5,5,4,3,2], times=10)

    def test_words(self):
        rw = final.RandomWriter(1, final.Tokenization.word)
        rw.train_iterable("the given iterable must contain the sequence the")
        self.assertNotContainsSequence(rw.generate(), "the the".split(" "))
        self.assertNotContainsSequence(rw.generate(), "the iterable".split(" "))
        self.assertContainsSequence(rw.generate(), "iterable must contain".split(" "), times=10)
        self.assertContainsSequence(rw.generate(), "the sequence".split(" "), times=200)

    def test_save_load_pickle(self):
        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("abcaea")
        with nonexistant_filename() as fn:
            rw.save_pickle(fn)
            rw2 = final.RandomWriter.load_pickle(fn)
            self.assertNotContainsSequence(rw.generate(), "ac")
            self.assertNotContainsSequence(rw.generate(), "aa")
            self.assertNotContainsSequence(rw.generate(), "ce")
            self.assertContainsSequence(rw.generate(), "abc", times=100)
            self.assertContainsSequence(rw.generate(), "aeaeab", times=100)

    def test_generate_file1(self):
        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("abcaea")
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rt") as fi:
                content = fi.read()
            self.assertNotContainsSequence(content, "ac")
            self.assertNotContainsSequence(content, "aa")
            self.assertNotContainsSequence(content, "ce")
            self.assertContainsSequence(content, "abc", times=100)
            self.assertContainsSequence(content, "aeaeab", times=100)

    def test_generate_file4(self):
        rw = final.RandomWriter(1, final.Tokenization.byte)
        #                   a   b   c   a   e   a
        rw.train_iterable(b"\xfe\xff\x02\xfe\x03\xfe")
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rb") as fi:
                content = fi.read()
            self.assertNotContainsSequence(content, b"\xfe\x02")
            self.assertNotContainsSequence(content, b"\xfe\xfe")
            self.assertNotContainsSequence(content, b"\x02\x03")
            self.assertContainsSequence(content, b"\xfe\xff\x02", times=100)
            self.assertContainsSequence(content, b"\xfe\x03\xfe\x03\xfe\xff", times=100)

    def test_generate_file_size(self):
        rw = final.RandomWriter(1, final.Tokenization.character)
        rw.train_iterable("abcaea")
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rt") as fi:
                content = fi.read()
            self.assertGreaterEqual(len(content), self.DEFAULT_LENGTH)
            self.assertLessEqual(len(content), self.DEFAULT_LENGTH+2)

    def test_generate_file2(self):
        rw = final.RandomWriter(1, final.Tokenization.word)
        rw.train_iterable("a the word the")
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rt") as fi:
                content = fi.read()
            self.assertNotContainsSequence(content, "the a")
            self.assertContainsSequence(content, "the word", times=100)

    def test_generate_file3(self):
        rw = final.RandomWriter(2, final.Tokenization.none)
        rw.train_iterable((1,2,3,4,5,5,4,3,2,1))
        with nonexistant_filename() as fn:
            rw.generate_file(fn, self.DEFAULT_LENGTH)
            with open(fn, "rt") as fi:
                content = fi.read()
            self.assertNotContainsSequence(content, "5 5 3")
            self.assertNotContainsSequence(content, "1 2 5")
            self.assertContainsSequence(content, "3 4 5 5 4 3 2", times=100)


    def test_numeric_sequence_in(self):
        rw = final.RandomWriter(2)
        rw.train_iterable((1,2,3,4,5,5,5,4,3,2,1,2,4,5))
        self.assertIsInstance(next(iter(rw.generate())), int)
        self.assertContainsSequence(rw.generate(), [3,4,5,5,4,3,2], times=10)
        self.assertContainsSequence(rw.generate(), [3,4,5,5,5,5,4,3,2])
        self.assertContainsSequence(rw.generate(), [5,5,5,5,5])
        self.assertContainsSequence(rw.generate(), [3,2,1,2,4,5,5,4])
        self.assertContainsSequence(rw.generate(), [3,2,1,2,3,4,5,5,4])

    def test_numeric_sequence_notin(self):
        rw = final.RandomWriter(2)
        rw.train_iterable((1,2,3,4,5,5,5,4,3,2,1,2,4,5))
        self.assertNotContainsSequence(rw.generate(), [5,5,3])
        self.assertNotContainsSequence(rw.generate(), [1,2,5])
        self.assertNotContainsSequence(rw.generate(), [4,2])
        self.assertNotContainsSequence(rw.generate(), ["5"])

    def test_generate_count(self):
        rw = final.RandomWriter(2, final.Tokenization.character)
        rw.train_iterable("What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! "
                          "in action how like an angel! in apprehension how like a god! the beauty of the world, the paragon of animals!")
        generated = len(list(itertools.islice(rw.generate(), 10000)))
        self.assertEqual(generated, 10000)

    def test_characters(self):
        rw = final.RandomWriter(2, final.Tokenization.character)
        rw.train_iterable("What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! "
                          "in action how like an angel! in apprehension how like a god! the beauty of the world, the paragon of animals!")
        self.assertIsInstance(next(iter(rw.generate())), str)
        self.assertContainsSequence(rw.generate(), "worm")
        self.assertNotContainsSequence(rw.generate(), "mals ")

    def test_train_iterator(self):
        rw = final.RandomWriter(1)
        rw.train_iterable(iter((1,2,3,4,5,5,5,4,3,2,1,2,4,5)))
        self.assertIsInstance(next(iter(rw.generate())), int)
        self.assertContainsSequence(rw.generate(), [3,4,5,5,4,3,2], times=10)
        self.assertContainsSequence(rw.generate(), [3,4,5,5,5,5,4,3,2])
        self.assertContainsSequence(rw.generate(), [5,5,5,5,5])
        self.assertContainsSequence(rw.generate(), [3,2,1,2,4,5,5,4])
        self.assertContainsSequence(rw.generate(), [3,2,1,2,3,4,5,5,4])

    def test_characters_level3(self):
        rw = final.RandomWriter(3, final.Tokenization.character)
        rw.train_iterable("What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! "
                          "in action how like an angel! in apprehension how like a god! the beauty of the world, the paragon of animals!")
        self.assertIsInstance(next(iter(rw.generate())), str)
        self.assertNotContainsSequence(rw.generate(), "worm")
        self.assertNotContainsSequence(rw.generate(), "mals ")
        self.assertContainsSequence(rw.generate(), "n how n")

    def test_bytes_nonutf8(self):
        rw = final.RandomWriter(2, final.Tokenization.byte)
        rw.train_iterable(b"What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! "
                          b"in action how like an angel! in apprehension how like a god!\xff\xfe the beauty of the world, the paragon of animals!")
        self.assertTrue(isinstance(next(iter(rw.generate())), (int, bytes)))
        self.assertNotContainsSequence(rw.generate(), b"mals ")
        self.assertContainsSequence(rw.generate(), b"worm")
        self.assertContainsSequence(rw.generate(), b"!\xff\xfe")

    def test_bytes_nonutf8_file(self):
        rw = final.RandomWriter(1, final.Tokenization.byte)
        rw.train_url("http://www.singingwizard.org/stuff/nonutf8.txt")
        self.assertTrue(isinstance(next(iter(rw.generate())), (int, bytes)))
        self.assertContainsSequence(rw.generate(), b"\xfe\xff\xfe")
        self.assertNotContainsSequence(rw.generate(), b"\x02\xfe")

    def test_train_twice(self):
        rw = final.RandomWriter(3, final.Tokenization.character)
        rw.train_iterable("What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! ")
        rw.train_iterable("in action how like an angel! in apprehension how like a god! the beauty of the world, the paragon of animals!")
        self.assertIsInstance(next(iter(rw.generate())), str)
        self.assertNotContainsSequence(rw.generate(), "worm")
        self.assertNotContainsSequence(rw.generate(), "mals ")
        self.assertContainsSequence(rw.generate(), "n how n")

    def test_words2(self):
        rw = final.RandomWriter(2, final.Tokenization.word)
        rw.train_iterable("What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! "
                          "in action how like an angel! in apprehension how like a god! the beauty of the world, the paragon of animals!")
        self.assertIsInstance(next(iter(rw.generate())), str)
        self.assertNotContainsSequence(rw.generate(), "man angel".split(" "), length=50000)
        self.assertNotContainsSequence(rw.generate(), "infinite in reason".split(" "), length=50000)
        self.assertNotContainsSequence(rw.generate(), ("worm",))
        self.assertContainsSequence(rw.generate(), "action how like a god!".split(" "), length=50000)
        self.assertContainsSequence(rw.generate(), "infinite in faculty!".split(" "), length=50000)

    def test_multiple_generators(self):
        rw = final.RandomWriter(2, final.Tokenization.character)
        rw.train_iterable("What a piece of work is man! how noble in reason! how infinite in faculty! in form and moving how express and admirable! "
                          "in action how like an angel! in apprehension how like a god! the beauty of the world, the paragon of animals!")
        self.assertIsInstance(next(iter(rw.generate())), str)
        g1 = rw.generate()
        g2 = rw.generate()
        ss = zip(*[(next(g1), next(g2)) for _ in range(self.DEFAULT_LENGTH)])
        for s in ss:
            self.assertContainsSequence(s, "worm")
            self.assertNotContainsSequence(s, "mals ")

    def test_train_url_characters(self):
        rw = final.RandomWriter(3, final.Tokenization.character)
        rw.train_url("http://www.singingwizard.org/stuff/pg24132.txt")
        self.assertContainsSequence(rw.generate(), "ad di", length=200000)

    def test_train_url_bytes(self):
        rw = final.RandomWriter(4, final.Tokenization.byte)
        rw.train_url("http://www.singingwizard.org/stuff/pg24132.txt")
        self.assertContainsSequence(rw.generate(), b"ad di", length=300000)

    def test_train_url_word(self):
        rw = final.RandomWriter(1, final.Tokenization.word)
        rw.train_url("http://www.singingwizard.org/stuff/pg24132.txt")
        self.assertContainsSequence(rw.generate(), "she had".split(), length=100000)

    def test_train_url_utf8(self):
        rw = final.RandomWriter(5, final.Tokenization.character)
        rw.train_url("http://www.singingwizard.org/stuff/utf8test.txt")
        self.assertContainsSequence(rw.generate(), "ajtób", length=100000)

    def test_graph_module(self):
        import graph
        print("Remember to make sure your graph module is general enough to be used in other applications.")


if __name__ == "__main__":
    unittest.main()
