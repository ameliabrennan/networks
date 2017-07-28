# Sarah July 2017
# Script for comparing text documents (SINGLE COMPARISON ONLY)
# Outputs summary files of most common words, and their frequencies, in each file
# Outputs summary of the Jaccard index and shared words
# i.e. the number of common words divided by the number of union unique words
# 0 for no common words, 1 for all the same words
# Could be modified for fancier text analysis, e.g. cosine
# Depends on nltk being downloaded

import os
import nltk
from nltk.corpus import stopwords
tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

def words_freq_dist(input_string):
    words_blob = ''.join(input_string)
    words_for_analysis = nltk.word_tokenize(words_blob)
    ignored = ignored_words()
    words_for_analysis = [w.lower() for w in words_for_analysis if w.lower() not in ignored]
    words_dist = nltk.FreqDist(words_for_analysis)
    return(words_dist)

def ignored_words():
    stops = set(stopwords.words('english'))
    html_filler = set(['div', 'href=', 'ul', 'class=', '/div', 'href=', '/a', 'li', '/li', '/td', '/span', 'grunticon-arw-right-red-20', '--', 'target=', '#', 'button-label', 'title=', '/footer', '/', 'mb-md-md-xs', 'type='])
    punctuation = set(['.', ',', '?', "''", ':', '``', ')', "'s", '(', '...', '%', '-', '!', "'", u'>', u';', u'&'])
    return stops | punctuation | html_filler

def read_file_to_string(input_file_name):
  print("\nReading file: %s" %input_file_name)
  input_file = open(input_file_name, "r")
  input_string = ""
  line_count = 0
  for line in input_file:
    try:
      input_string += line
      #.encode('UTF-8')
      line_count += 1
    except:
      print("\tNote! Line %s skipped due to error with text encoding" %(str(line_count)))
    continue
  
  print(input_string)
  return(input_string)

def return_root_file_name(file_name):
  base_file_name = os.path.basename(file_name)
  root_file_name = os.path.splitext(base_file_name)[0]
  return(root_file_name)

def return_file_extension(file_name):
  base_file_name = os.path.basename(file_name)
  file_extension = os.path.splitext(base_file_name)[1]
  return(file_extension)

def return_output_file_name(input_file_name):
  output_file_name = os.path.dirname(input_file_name) + '/' + return_root_file_name(input_file_name) 
  output_file_name += '_WORDFREQUENCY.csv'
  return(output_file_name)

def write_words_freq_to_file(words_freq_dist, output_file_name, limit_write_words=600):
  print("\nWriting %s most common words to file: %s" %(limit_write_words, output_file_name))
  output_file = open(output_file_name, "w")
  output_file.write("WORD, COUNT")
  output_file.write("\n")
  for current_word, count in words_freq_dist.most_common(limit_write_words):
    output_file.write(current_word)
    output_file.write(",")
    output_file.write(str(count))
    output_file.write("\n")

def preview_words_freq(words_freq_dist, limit_display_words=20):
  dict_count = len(words_freq_dist)
  print("Found %s distinct words" %dict_count)
  print("\nPreview of %s most common words:" %limit_display_words)
  print(words_freq_dist.most_common(limit_display_words))

def words_freq_shared_count(left, right):
  shared_words = 0
  for k, v in left.items():
    if k in right:
      shared_words += 1
  return(shared_words)


def words_freq_missing_from_second_list(left, right):
  missing_words = [""]
  for k, v in left.items():
    if k not in right:
      missing_words.append(k)
  return(missing_words)

def jaccard_text_file_comparison(input_file_name_1, input_file_name_2):
  
  input_string_1 = read_file_to_string(input_file_name_1)
  input_string_2 = read_file_to_string(input_file_name_2)

  result = jaccard_text_comparison(input_string_1, input_string_2)

def jaccard_text_comparison(input_string_1, input_string_2):
  
  words_freq_dist_1 = words_freq_dist(input_string_1)
  words_freq_dist_2 = words_freq_dist(input_string_2)

  word_count_1 = len(words_freq_dist_1)
  word_count_2 = len(words_freq_dist_2)
  
  input_string_union = input_string_1 + input_string_2
  words_freq_dist_union = words_freq_dist(input_string_union)

  union_word_count = len(words_freq_dist_union)

  shared_word_count = words_freq_shared_count(words_freq_dist_1, words_freq_dist_2)

  jaccard_index = float(shared_word_count)/float(union_word_count)

  print("\n\t**** Result ****")
  print("\tUnique words 1: %s" %(str(word_count_1)))
  print("\tUnique words 2: %s" %(str(word_count_2)))
  print("\n\tUnique words in UNION of two string: %s" %(str(union_word_count)))
  print("\n\tShared word count: %s" %(str(shared_word_count)))
  print("\tJaccard index: %s" %(str(jaccard_index)))

##### MAIN

input_directory = "H:/Sarah_GOS2016_BurningGlass/Stage_6_WordComparison/"
file_name_1 = input_directory + "BH069_BurningGlass.txt"
print(file_name_1)
file_name_2 = input_directory + "BH069_ProgramDescription.txt"
print(file_name_2)

result = jaccard_text_file_comparison(file_name_1, file_name_2)

#result = jaccard_text_file_comparison(file_name_1, file_name_2)
