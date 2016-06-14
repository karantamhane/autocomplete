from flask import Flask, render_template, request, redirect, url_for, make_response
from trie import Trie
app = Flask(__name__)

'''
Build a Trie using the appropriate data
'''
# t = Trie()
# t.add_words_from_file("stories.txt")

# t = Trie(low=True)
# t.add_words_from_file("chamber_of_secrets.txt")

t = Trie()
t.add_phrases_from_file("designers.txt")
t.add_phrases_from_file("dresses.txt")

'''
Get user input and request suggestions for autocomplete
'''
@app.route('/', methods=['GET', 'POST'])
def index():
  word = request.args.get('word')
  if word:
    wordlist = t.show_matches(word)
    # print wordlist
    if wordlist == [''] or wordlist == []:
      wordlist = ['No matches found']
    return make_response(render_template('index.html', word=word, wordlist=wordlist))
  else:
    return render_template('index.html')

if __name__ == '__main__':
  app.run('localhost', 5000)