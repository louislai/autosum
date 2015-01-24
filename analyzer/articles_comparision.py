import article_analysis
from sets import Set
import operator
import math

def get_descriptive_words_and_frequencies(article_url, stop_word_set):
	sentence_list = article_analysis.split_article_into_setences(article_url)
	desc_word_list, frequence_dict, desc_words_total = article_analysis.get_descriptive_words(sentence_list, stop_word_set)
	return (desc_word_list, frequence_dict, desc_words_total)

def calculate_closeness_of_articles(first_url, second_url):
	stop_word_set = article_analysis.read_stop_words_file()
	first_desc_word_list, first_freq_dict, first_desc_word_total = get_descriptive_words_and_frequencies(first_url, stop_word_set)
	second_desc_word_list, second_freq_dict, second_desc_word_total = get_descriptive_words_and_frequencies(second_url, stop_word_set)

	common_desc_word_list = [] # list of words that appear in both first descriptive word list and second descriptive word list 
	first_desc_word_set = Set(first_desc_word_list)
	second_desc_word_set = Set(second_desc_word_list)
	common_word_num_in_first = 0
	common_word_num_in_second = 0
	common_word_dict = {}
	for word in first_desc_word_list:
		if word in second_desc_word_set:
			common_desc_word_list.append(word)
			common_word_dict[word] = first_freq_dict[word] + second_freq_dict[word]
			common_word_num_in_first = common_word_num_in_first + first_freq_dict[word]
			common_word_num_in_second = common_word_num_in_second + second_freq_dict[word]

	sorted_common_word_freq_pairs = sorted(common_word_dict.items(), key=operator.itemgetter(1), reverse=True)
	sorted_common_words = [word for (word, freq) in sorted_common_word_freq_pairs]

	closeness_ratio = max(common_word_num_in_first * 1.0 / first_desc_word_total, common_word_num_in_second * 1.0 / second_desc_word_total);
	closeness_percentage = round(closeness_ratio * 100, 1)

	expected_common_topic_word_num = min(math.ceil(len(first_desc_word_list) / 60.0), math.ceil(len(second_desc_word_list) / 60.0))
	expected_common_topic_word_num = int(min(expected_common_topic_word_num, len(sorted_common_words), 5))

	return closeness_percentage, sorted_common_words[:expected_common_topic_word_num]


if __name__ == '__main__':
	first_url = 'http://oliveremberton.com/2014/the-problem-isnt-that-life-is-unfair-its-your-broken-idea-of-fairness/'
	second_url = 'http://oliveremberton.com/2014/how-to-make-resolutions-that-actually-work/'
	print calculate_closeness_of_articles(first_url, second_url)