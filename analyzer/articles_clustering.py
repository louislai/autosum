import articles_comparison
import article_analysis
import clusters_new
import operator
from sets import Set

def cluster_articles(url_list):
	stop_word_set = article_analysis.read_stop_words_file()
	data_list = []
	combined_desc_word_dict = {}
	for url in url_list:
		data = articles_comparison.get_descriptive_words_and_frequencies(url, stop_word_set)
		data_list.append(data)
		desc_word_list, frequence_dict, desc_words_total = data
		for word in desc_word_list:
			combined_desc_word_dict.setdefault(word, 0)
			combined_desc_word_dict[word] = combined_desc_word_dict[word] + frequence_dict[word]

	sorted_combined_desc_word_freq_pairs = sorted(combined_desc_word_dict.items(), key=operator.itemgetter(1), reverse=True)
	expected_common_word_num = min(len(sorted_combined_desc_word_freq_pairs), 10)
	expected_word_freq_pairs = sorted_combined_desc_word_freq_pairs[:expected_common_word_num]
	expected_common_desc_word_list = [word for (word, freq) in expected_word_freq_pairs]

	article_name_list = []
	common_freq_list = []
	for idx, data in enumerate(data_list):
		article_name_list.append('Article ' + str(idx))
		common_freq_list.append([])
		desc_word_list, frequence_dict, desc_words_total = data
		desc_word_set = Set(desc_word_list)
		for word in expected_common_desc_word_list:
			if word in desc_word_list:
				common_freq_list[idx].append(frequence_dict[word])
			else:
				common_freq_list[idx].append(0)

	clust = clusters_new.hcluster(common_freq_list)
	clusters_new.drawdendrogram(clust,article_name_list,jpeg="clust.jpg")

	return 'clust.jpg'

if __name__ == '__main__':
	url_list = []
	url_list.append('http://oliveremberton.com/2014/the-problem-isnt-that-life-is-unfair-its-your-broken-idea-of-fairness/')
	url_list.append('http://oliveremberton.com/2014/how-to-make-resolutions-that-actually-work/')
	url_list.append('http://oliveremberton.com/2014/how-to-find-your-passion/')
	url_list.append('http://oliveremberton.com/2014/if-you-want-to-follow-your-dreams-you-have-to-say-no-to-all-the-alternatives/')
	print cluster_articles(url_list)