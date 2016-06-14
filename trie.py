import string, re

class Trie:
  '''
  Build a prefix tree to make autocomplete suggestions
  '''
  def __init__(self, low=False):
    lower = {chr(i):{} for i in range(97, 97+26)}
    upper = {chr(i):{} for i in range(65, 65+26)}
    self.children = dict(lower.items() + upper.items())
    self.children[" "] = {}
    self.low = low
    # print self.children

  '''
  Add word to the trie recursively
  '''
  def add_word(self, word, root=None):
    if word == '':
      if root != self.children and root is not None:
        root['_'] = {}
      return
    if self.low:
      word = word.lower()
    if word[0] not in self.children:
        return
    if not root:
      root = self.children
    parent = root[word[0]]
    if len(word) > 1:
      if word[1] not in parent:
        parent[word[1]] = {}
    self.add_word(word[1:], root[word[0]])

  '''
  Check if the trie contains a word, and whether it is valid
  '''
  def is_valid(self, word, root=None):
    if word == '':
      if root is not None:
        return '_' in root
      else:
        return True
    if not root:
      root = self.children
    if self.low:
      word = word.lower()
    if word[0] in root:
      return self.find_word(word[1:], root[word[0]])
    else:
      return False

  '''
  Display all words starting with the prefix word
  '''
  def show_matches(self, word, root=None):
    if word == '':
      return ['']
    if root is None:
      root = self.children
    orig_word = word
    if self.low:
      word = word.lower()
    while word:
      if word[0] in root:
        root = root[word[0]]
        word = word[1:]
      else:
        return ['']
    # print 'root =',root
    return self.build_words(root, orig_word, [])

  '''
  Build all valid words starting from current root dict
  '''
  def build_words(self, root, word, acc):
    # print 'word =',word,'root =',root
    if root == {}:
      return ['']
    for c in root:
      if '_' in root[c]:
        acc.append(word + c)
      self.build_words(root[c], word+c, acc)
    return acc

  '''
  Build trie from words in a file
  '''
  def add_words_from_file(self, filename):
    with open(filename) as f:
      delims = '#$%&\\ \n()*+,-./:;<=>?@[\\]^_`{|}~"'
      text = f.read()
      text = re.split('['+delims+']', text)
      text = [word for word in text if word != '']
      # print len(text)
      for w in text:
        self.add_word(w)

  '''
  Build trie from phrases in a file
  '''
  def add_phrases_from_file(self, filename):
    with open(filename) as f:
      text = f.readlines()
      text = [p.rstrip() for p in text]
      # print text
      for p in text:
        self.add_word(p)
      # print self.children

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Usage: python trie.py 'word_to_be_autocompleted'"
    print "Example: python trie.py que"
    print "Returns: ['queer', 'queen', 'quench']"
    exit()
  t = Trie()
  t.add_phrases_from_file('designers.txt')
  print t.show_matches(sys.argv[1])



