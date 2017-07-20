import os
import nltk
from nltk.corpus import stopwords
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

def words_freq_dist(input_string):
    #print("input_string: ", input_string)
    words_blob = ''.join(input_string)
    words_for_analysis = nltk.word_tokenize(words_blob)
    ignored = ignored_words()
    words_for_analysis = [w.lower() for w in words_for_analysis if w.lower() not in ignored]
    # print("words_for_analysis", words_for_analysis)
    words_dist = nltk.FreqDist(words_for_analysis)
    return(words_dist)

def ignored_words():
    stops = set(stopwords.words('english'))
    html_filler = set(['div', 'href=', 'ul', 'class=', '/div', 'href=', '/a', 'li', '/li', '/td', '/span', 'grunticon-arw-right-red-20', '--', 'target=', '#', 'button-label', 'title=', '/footer', '/', 'mb-md-md-xs', 'type='])
    punctuation = set(['.', ',', '?', "''", ':', '``', ')', "'s", '(', '...', '%', '-', '!', "'", u'>', u';', u'&'])
    return stops | punctuation | html_filler

def return_root_file_name(file_name):
  base_file_name = os.path.basename(file_name)
  root_file_name = os.path.splitext(base_file_name)[0]
  return(root_file_name)


#####MAIN

# Read in file
input_file_name = "input_text.txt"
print("\Input file: %s" %input_file_name)
input_file = open(input_file_name, "r")
input_string = ""
input_line_count = 0
for line in input_file:
    input_string += line
    input_line_count += 1

# call word distribution functions, print preview of results
words_freq_dist = words_freq_dist(input_string)
print("\nPreview of most common words:")
print(words_freq_dist.most_common(10))

# write to file with same name, new extension

#output_file_name = os.path.dirname(input_file_name) + '/' + 
output_file_name = return_root_file_name(input_file_name) + '.csv'
print("\nNow writing word counts to file: %s" %output_file_name)

output_file = open(output_file_name, "w")
output_file.write("WORD, COUNT")
output_file.write("\n")
for sample, count in words_freq_dist.most_common(100):
 # print(sample)
 # print(str(count))
  output_file.write(sample)
  output_file.write(",")
  output_file.write(str(count))
  output_file.write("\n")
