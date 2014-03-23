#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import time

class Node:
    nodes = {}
    words = []

    def __init__(self):
        self.nodes = {}
        self.words = []

    def __repr__(self):
        """Mainly for debug/prints - the string representation of this class
        prints the node's words,
        and child node keys (numbers, as a one-character string)
        """
        return 'words: %s, keys: %s' % (self.words, self.nodes.keys())

    def insert_word(self, letter_to_number_mapping, letters_remaining, final_word):
        """From this node, insert a word
        Called recursively for each letter in the word, returning the top-level node
        Always passing the letter_to_number mapping in is a bit ugly, but hey it works =)

        Also, may be a better way than always passing round the 'final_word'
        (which is pushed onto the final node's .words[]) ...
        """

        # If the word contains non-letter characters, skip
        if not re.match('^[A-Z]+$', final_word):
            return self

        if letters_remaining:
            current_letter = letters_remaining[0]
            current_number = letter_to_number_mapping[current_letter]
            letters_remaining = letters_remaining[1:]
            if not self.nodes.get(current_number):
                self.nodes[current_number] = Node()
            self.nodes[current_number] = self.nodes[current_number].insert_word(letter_to_number_mapping, letters_remaining, final_word)
        else:
            self.words.append(final_word)
        return self

    def possible_words(self, numbers_remaining, root_node=None, have_used_a_number_as_word=False):
        """Given a string of numbers (numbers_remaining)
        return an array of possible words
        (or combination of words separated by hyphens)

        root_node is always the top-level root of the whole tree,
        to allow searching for further possible words from the top.
        Bit ugly to pass it around all the time, but hey it works

        have_allowed_a_number effects the 'can skip one number' rule

        """
        print 'possible_words, rem=%s, im=%s, huanaw¡=%s' % (numbers_remaining, self, have_used_a_number_as_word)

        # First time, we'll becalled with no root node specified; i am the root
        if not root_node:
            root_node = self

        # If we're at the end of the list of numbers, return my words (if any)
        if not numbers_remaining:
            return self.words

        # Numbers remain, and this node has words
        # Check for combos with further words
        # If such exist, combine this node's words those with those further words
        # (separated by hyphens)
        combined_words = []
        if self.words:
            further_possible_words = root_node.possible_words(numbers_remaining=numbers_remaining, root_node=root_node)

            # The rule is:
            # "If no further words are possible, it's ok to treat one number as a word"
            # But only once
            if not further_possible_words and not have_used_a_number_as_word:
                # Get further_possible, skipping the current number
                further_possible_words = root_node.possible_words(
                    numbers_remaining=numbers_remaining[1:],
                    root_node=root_node,
                    have_used_a_number_as_word=True)
                # Munge the current number on to the end of all of this node's words
                self.words = [word + '-' + numbers_remaining[0] for word in self.words]

            # Combine all words on this node, with all further possible words,
            for word in self.words:
                for further_possible_word in further_possible_words:
                    combined_words.append('-'.join([word, further_possible_word]))

        # From this node, with the remaining numbers, check child nodes for longer words
        next_number = numbers_remaining[0]
        numbers_remaining = numbers_remaining[1:]
        try:
            longer_words = self.nodes[next_number].possible_words(numbers_remaining, root_node=root_node, have_used_a_number_as_word=have_used_a_number_as_word)
        except KeyError, e:
            # There's no node form here with the next number
            longer_words = []
        return combined_words + longer_words

if __name__ == '__main__':
    # Build the letter-to-number mapping
    number_to_letter_mapping = {
        '0': '0',
        '1': '1',
        '2': '2ABC',
        '3': '3DEF',
        '4': '4GHI',
        '5': '5JKL',
        '6': '6MNO',
        '7': '7PQRS',
        '8': '8TUV',
        '9': '9WXZY',
    }
    letter_to_number_mapping = {}
    for n in number_to_letter_mapping:
        for letter in number_to_letter_mapping[n]:
            letter_to_number_mapping[letter] = n

    # Load the dict
    dictfile = '/usr/share/dict/words'
    dictfile =  'dict_words'
    #dictfile =  'words'
    words = open(dictfile, 'r')
    root_node = Node()
    i=0
    start_time = time.time()
    for word in words:
        i+=1
        word = word.strip().upper()
        root_node = root_node.insert_word(letter_to_number_mapping, letters_remaining=word, final_word=word)
    end_time = time.time()
    #print 'loaded %s words in %s sec' % (i, int(end_time-start_time))

    for line in sys.stdin:
        number = line.strip()
        number = re.sub('[^0-9]', '', number)
        words = root_node.possible_words(number)
        for word in words:
            print word


    # All below is testing util stuff
    def w2n(word):
        """Util to convert a word to numbers
        """
        word = re.sub('[^A-Z0-9]', '', word)
        return ''.join([letter_to_number_mapping[x] for x in word])
    #print 'final: %s' % root_node.possible_words(w2n('cross3word'))
    #print 'final: %s' % root_node.possible_words(w2n('cross3words'))
    #print 'final: %s' % root_node.possible_words(w2n('catbat'))
    #print 'final: %s' % root_node.possible_words(w2n('bat'))

    def generate_some_phone_numbers():
        import random
        for i in xrange(100):
            print random.randint(10000000,19999999)
    #generate_some_phone_numbers()
