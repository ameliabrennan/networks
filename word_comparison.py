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
    html_filler = set(['div', 'class=', '/div'])
    punctuation = set(['.', ',', '?', "''", ':', '``', ')', "'s", '(', '...', '%', '-', '!', "'", u'>', u';', u'&'])
    return stops | punctuation | html_filler

my_file = open("input_text.txt", "r")
my_string = ""
for line in my_file:
    my_string += line
print(my_string)
words_list = my_string

#words_list = "Upon successful completion of the program, you will have gained broad knowledge and skills for paraprofessional work and/or further learning within the fashion and textiles industry. This program will give you a broad theoretical and technical knowledge of specific areas such as product development, supply chain, marketing, CAD/IT, fashion materials, fashion branding, fashion visual merchandising and merchandise planning."
#words_list += "The RMIT Associate Degree Fashion and Textiles Merchandising is designed to develop a work-ready fashion merchandiser who will have broad knowledge and skills for paraprofessional work and/or further learning.  You will develop the requisite skills and graduate capabilities to succeed in the rapidly evolving fashion and textiles industry. This program has a strong emphasis on teamwork within a business environment contextualised for merchandising. You will be prepared for employment through the development of interrelationships and direct contact with industry."
words_freq_dist = words_freq_dist(words_list)
#print(words_freq_dist)
print(words_freq_dist.most_common(30))
print("\nHERE ARE THE MOST COMMON WORDS")

output_file = open("word_counts.csv", "w")
output_file.write("WORD, COUNT")
output_file.write("\n")
for sample, count in words_freq_dist.most_common(15):
  print(sample)
  print(str(count))
  output_file.write(sample)
  output_file.write(",")
  output_file.write(str(count))
  output_file.write("\n")
