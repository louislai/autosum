from sets import Set
from goose import Goose
import operator



def read_stop_words_file():
	f = open('analyzer/stop_words.txt')
	file_content = f.read().replace(' ', '')
	stop_words = file_content.strip().split(',')
	return Set(stop_words)

def read_conclusion_transition_word_file():
	f = open('conclusion_transition_word.txt')
	file_content = f.read()
	transition_word_list = file_content.split(',')
	return transition_word_list

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
	check_if_a_sentence_qualified_for_summary(topic_potential_word_set, prob_dict, title, 0.33)

def check_if_sentence_contains_conclusion_transition_word(sentence):
	transition_word_list = read_conclusion_transition_word_file()
	for word in transition_word_list:
		if sentence.lower().find(word) >= 0:
			return True

	return False

def get_topic_potential_sentences(topic_potential_word_set, prob_dict, sentence_list):
	'''
	get a list of sentences which contains conclusion_transition_word
	'''
	important_sentence_list = []
	for sentence in sentence_list:
		if check_if_sentence_contains_conclusion_transition_word(sentence):
			important_sentence_list.append(sentence)

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
	chosen_pairs = sorted_sentence_weight_pairs[0:4]
	chosen_sentences = [chosen_sentence for (chosen_sentence, weight) in chosen_pairs]

	is_title_qualified = check_if_title_qualified_for_summary(topic_potential_word_set, prob_dict, sentence_list[0])


	return chosen_sentences
	# return get_topic_potential_sentences(topic_potential_word_set, prob_dict, sentence_list)

def get_summary(article_url):
	sentence_list = split_article_into_setences(article_url)
	stop_word_set = read_stop_words_file()
	return pick_summary_sentences(sentence_list, stop_word_set)

if __name__ == '__main__':
	article_url = 'http://www.straitstimes.com/news/sport/tennis/story/tennis-sister-act-spurs-serena-williams-open-last-16-20150124'
	sentence_list = split_article_into_setences(article_url)
	stop_word_set = read_stop_words_file()
	# print pick_summary_sentences(sentence_list, stop_word_set)
	print get_summary(article_url)

stop_words= "a, able, about, above, according, accordingly, across, actually, after, afterwards, again, against, all, allow, allows, almost, alone, along, already, also, although, always, am, among, amongst, an, and, another, any, anybody, anyhow, anyone, anything, anyway, anyways, anywhere, apart, appear, appreciate, appropriate, are, around, as, aside, ask, asking, associated, at, available, away, awfully, be, became, because, become, becomes, becoming, been, before, beforehand, behind, being, believe, below, beside, besides, best, better, between, beyond, both, brief, but, by, came, can, cannot, cant, cause, causes, certain, certainly, changes, clearly, co, com, come, comes, concerning, consequently, consider, considering, contain, containing, contains, corresponding, could, course, currently, definitely, described, despite, did, different, do, does, doing, done, down, downwards, during, each, edu, eg, eight, either, else, elsewhere, enough, entirely, especially, et, etc, even, ever, every, everybody, everyone, everything, everywhere, ex, exactly, example, except, far, few, fifth, first, five, followed, following, follows, for, former, formerly, forth, four, from, further, furthermore, get, gets, getting, given, gives, go, goes, going, gone, got, gotten, greetings, had, happens, hardly, has, have, having, he, hello, help, hence, her, here, hereafter, hereby, herein, hereupon, hers, herself, hi, him, himself, his, hither, hopefully, how, howbeit, however, ie, if, ignored, immediate, in, inasmuch, inc, indeed, indicate, indicated, indicates, inner, insofar, instead, into, inward, is, it, its, itself, just, keep, keeps, kept, know, knows, known, last, lately, later, latter, latterly, least, less, lest, let, like, liked, likely, little, look, looking, looks, ltd, mainly, many, may, maybe, me, mean, meanwhile, merely, might, more, moreover, most, mostly, much, must, my, myself, name, namely, nd, near, nearly, necessary, need, needs, neither, never, nevertheless, new, next, nine, no, nobody, non, none, noone, nor, normally, not, nothing, novel, now, nowhere, obviously, of, off, often, oh, ok, okay, old, on, once, one, ones, only, onto, or, other, others, otherwise, ought, our, ours, ourselves, out, outside, over, overall, own, particular, particularly, per, perhaps, placed, please, plus, possible, presumably, probably, provides, que, quite, qv, rather, rd, re, really, reasonably, regarding, regardless, regards, relatively, respectively, right, said, same, saw, say, saying, says, second, secondly, see, seeing, seem, seemed, seeming, seems, seen, self, selves, sensible, sent, serious, seriously, seven, several, shall, she, should, since, six, so, some, somebody, somehow, someone, something, sometime, sometimes, somewhat, somewhere, soon, sorry, specified, specify, specifying, still, sub, such, sup, sure, take, taken, tell, tends, th, than, thank, thanks, thanx, that, thats, the, their, theirs, them, themselves, then, thence, there, thereafter, thereby, therefore, therein, theres, thereupon, these, they, think, third, this, thorough, thoroughly, those, though, three, through, throughout, thru, thus, to, together, too, took, toward, towards, tried, tries, truly, try, trying, twice, two, un, under, unfortunately, unless, unlikely, until, unto, up, upon, us, use, used, useful, uses, using, usually, value, various, very, via, viz, vs, want, wants, was, way, we, welcome, well, went, were, what, whatever, when, whence, whenever, where, whereafter, whereas, whereby, wherein, whereupon, wherever, whether, which, while, whither, who, whoever, whole, whom, whose, why, will, willing, wish, with, within, without, wonder, would, would, yes, yet, you, your, yours, yourself, yourselves, zero"
