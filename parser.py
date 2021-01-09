import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S P S
NP -> N | Det NP | Adj NP | PP NP | NP PP | NP Conj NP
PP -> P NP | P
VP -> V | V NP | Adv VP | VP Adv | VP Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence.lower())

    for word in words.copy():
        if not word.isalnum() or word.isdigit():
            words.remove(word)

    return words

def npElement(tree):
    if len(tree) > 1:
        element_tree = []
        for subtree in tree:
            if (subtree.label() == "NP" or subtree.label() == "N") and len(subtree) == 1:
                element_tree.append(subtree)
            elif len(subtree) > 1:
                element_tree.extend(npElement(subtree))
        return element_tree

    if tree.label() == "NP" and len(tree) == 1:
        return tree
    else:
        return None

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    nounPhrases = []

    for subtree in tree:
        element = npElement(subtree)
        if element is not None:
            for item in element:
                if item.label() == "N":
                    nounPhrases.append(item)
                elif item.label() == "NP":
                    for item2 in item:
                        nounPhrases.append(item2)

    return nounPhrases

if __name__ == "__main__":
    main()
