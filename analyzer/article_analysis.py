from sets import Set
from goose import Goose
import operator
import math

def read_stop_words_file():
	f = open('analyzer/stop_words.txt')
	file_content = f.read().replace(' ', '')
	stop_words = file_content.strip().split(',')
	return Set(stop_words)

def get_article_from_url(article_url):
	# Official code
	g = Goose()
	article = g.extract(url=article_url)	
	return (article.title, article.cleaned_text)	

	'''# Testing code
	f1 = open('title.txt');
	article_title = f1.read()
	f2 = open('article.txt');
	article_content = f2.read()
	return (article_title, article_content)'''

def split_article_into_setences(article_url): 
	'''
	split the article into a list of sentences based in the sentence periods
	'''
	(article_title, article_content) = get_article_from_url(article_url)
	sentence_list = [article_title]
	article_content = article_content.replace('\n', '')

	article_length = len(article_content)
	i=0
	curr_dot_position = 0
	while (i < article_length):
		prev_dot_position = curr_dot_position
		curr_dot_position = article_content.find('.', i)
		if (curr_dot_position >= i):
			if (curr_dot_position < article_length-1): # check if the dot found is the last dot of the article
				next_char = article_content[curr_dot_position + 1]
				if (not next_char.isdigit()): # check if the dot is really a sentence period  
					sentence_list.append(article_content[prev_dot_position+1:curr_dot_position].strip())
					i = curr_dot_position + 1
				else:
					i = curr_dot_position + 1
					curr_dot_position = prev_dot_position
			else:
				sentence_list.append(article_content[prev_dot_position+1:curr_dot_position].strip())
				i = curr_dot_position + 1
		else:
			break

	return sentence_list

def get_descriptive_words(sentence_list, stop_word_set):
	desc_word_list = [] # list of descriptive words (words that are not stop words)
	frequence_dict = {} # frequencies of descriptive words in the article
	desc_words_total = 0; # total number of descriptive words (including frequency)

	for sentence in sentence_list:
		word_list = sentence.split(' ')
		for word in word_list:
			word = word.lower().replace(',', '').replace('(', '').replace(')', '')
			if (not (word in stop_word_set)):
				if (word in Set(desc_word_list)):
					frequence_dict[word] = frequence_dict[word] + 1
				else:
					frequence_dict.setdefault(word, 1)
					desc_word_list.append(word)
				desc_words_total = desc_words_total + 1

	return (desc_word_list, frequence_dict, desc_words_total)

def get_topic_potential_words(sentence_list, stop_word_set):
	'''
	Find a list of words which are possibly the main ideas of the article
	'''
	desc_word_list, frequence_dict, desc_words_total = get_descriptive_words(sentence_list, stop_word_set)
	sorted_frequence_pairs = sorted(frequence_dict.items(), key=operator.itemgetter(1), reverse=True)
	
	expected_topic_potential_words_num = desc_words_total / 8
	topic_potential_pair_list = sorted_frequence_pairs[0:expected_topic_potential_words_num]
	topic_potential_word_list = [word for (word, frequency) in topic_potential_pair_list]

	# calculate the probability of all topic-potential words
	total_num_topic_potential_words = 0
	for (word, frequency) in topic_potential_pair_list:
		total_num_topic_potential_words = total_num_topic_potential_words + frequency
	prob_dict = {}
	for (word, frequency) in topic_potential_pair_list:
		prob_dict[word] = frequency * 1.0 / total_num_topic_potential_words

	return (topic_potential_word_list, prob_dict)

def check_if_a_sentence_qualified_for_summary(topic_potential_word_set, prob_dict, sentence, qualified_ratio):
	word_list = sentence.split(' ')
	topic_potential_word_num = 0
	total_prob = 0
	
	for word in word_list:
		word = word.lower().replace(',', '').replace('(', '').replace(')', '')
		if word in topic_potential_word_set:
			topic_potential_word_num = topic_potential_word_num + 1
			total_prob = total_prob + prob_dict[word]
	topic_potential_word_ratio = topic_potential_word_num * 1.0 / len(word_list)
	average_prob_in_title = total_prob * 1.0 / topic_potential_word_num

	if (topic_potential_word_ratio < qualified_ratio):
		return False

	average_prob_in_article = 1.0 / len(topic_potential_word_set)
	if (average_prob_in_title <= average_prob_in_article):
		return False

	return True

def check_if_title_qualified_for_summary(topic_potential_word_set, prob_dict, title):
	return check_if_a_sentence_qualified_for_summary(topic_potential_word_set, prob_dict, title, 0.33)

def pick_summary_sentences(sentence_list, stop_word_set):
	sentence_weight_dict = {}
	topic_potential_word_list, prob_dict = get_topic_potential_words(sentence_list, stop_word_set)
	topic_potential_word_set = Set(topic_potential_word_list)
	
	for sentence in sentence_list:
		sentence_weight_dict.setdefault(sentence, 0)
		word_list = sentence.split(' ')
		for word in word_list:
			word = word.lower().replace(',', '').replace('(', '').replace(')', '')
			if (word in topic_potential_word_set):
				sentence_weight_dict[sentence] = sentence_weight_dict[sentence] + prob_dict[word]
	
	sorted_sentence_weight_pairs = sorted(sentence_weight_dict.items(), key=operator.itemgetter(1), reverse=True)
	sorted_sentence_list = [sentence for (sentence, weight) in sorted_sentence_weight_pairs if sentence != sentence_list[0]]
	is_title_qualified = check_if_title_qualified_for_summary(topic_potential_word_set, prob_dict, sentence_list[0])
	chosen_sentences = []

	print is_title_qualified

	if is_title_qualified:
		chosen_sentences.append(sentence_list[0])
	
	expected_summary_sentence_num = int(math.ceil(len(sentence_list) * 1.0 / 8))
	expected_summary_sentence_num = min(expected_summary_sentence_num, 5)
	for i in range(expected_summary_sentence_num):
		chosen_sentences.append(sorted_sentence_list[i])

	return chosen_sentences

def get_summary(article_url):
	sentence_list = split_article_into_setences(article_url)
	stop_word_set = read_stop_words_file()
	return pick_summary_sentences(sentence_list, stop_word_set)

if __name__ == '__main__':
	article_url = 'http://oliveremberton.com/2014/the-problem-isnt-that-life-is-unfair-its-your-broken-idea-of-fairness/'
	print get_summary(article_url)