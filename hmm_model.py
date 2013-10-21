import sys
import re
import pickle
from sets import Set
# create test set

def main():
    corpus = ''
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python ' + sys.argv[0] + ' filename.pos\n')
        sys.exit(1)
    for index in range(1, len(sys.argv)):
        f = open(sys.argv[index])
        for line in f:
            corpus = corpus + line + " "
        f.close()
    
    print "Calculating HMM probabilities...."
    corpus = corpus.split(' ')
    observations = get_tagged_list(corpus)
    
    total_tag_list = observations[0]
    vocabulary = observations[2]

    # get transition probabilities
    transition_counts = get_transition_counts(total_tag_list)
    transition_probs = get_transition_probs(transition_counts)
    tag_list = transition_counts.keys()

    # get emission probabilities
    tagged_observations = observations[1]
    emission_counts = get_emission_counts(tagged_observations)
    emission_probs = get_emission_probs(emission_counts)
    
    to_pickle = [transition_probs, emission_probs, tag_list, vocabulary]
    pickle.dump(to_pickle, open('model.dat', 'w'))
    print "Saving to model.dat"

def get_tagged_list(text):
    total_tag_list = []
    tagged_tokens_list = []
    vocabulary = Set([])
    for token in text:
        token = re.sub(r"\n", "", token)
        if token.startswith('='):
            token = 'q_zero/q_zero'
        if token == '':
            continue
        tagged_token = token.split('/')
        word = tagged_token[0] 
        tag = tagged_token[1]
        # unfortunately, not every phrase is separated by ==== but I'm scrunching this class so I'm letting that slide
        if tag == 'q_zero' and len(total_tag_list) > 0: # don't add q_final to the beginning of the list
            total_tag_list.append('q_final')
        total_tag_list.append(tag)
        tagged_tokens_list.append(tagged_token)
        vocabulary.add(word)
    total_tag_list.append('q_final') # add last final tag to list
    return total_tag_list, tagged_tokens_list, vocabulary

def get_transition_counts(list):    
    transition_counts = {}
    for i in range(0, len(list) - 1):
        # storing bigram tag counts based on first tag in sequence
        tag_one = list[i]
        tag_two = list[i + 1]
        if tag_one in transition_counts:
            tag_one_dict = transition_counts[tag_one]
            if tag_two in tag_one_dict:
                tag_one_dict[tag_two] += 1.0
            else:
                tag_one_dict[tag_two] = 1.0
        else:
            transition_counts[tag_one] = {tag_two : 1.0}
    return transition_counts

def get_transition_probs(dict_of_dicts):
    transition_probs = {}
    for tag_one in dict_of_dicts.keys():
        total_count = 0.0
        transition_probs[tag_one] = {}
        tag_one_dict = dict_of_dicts[tag_one]
        for tag_two in tag_one_dict.keys():
            total_count += tag_one_dict[tag_two]
        for tag_two in tag_one_dict.keys():
            transition_probs[tag_one][tag_two] = tag_one_dict[tag_two]/total_count
    return transition_probs

def get_emission_counts(tagged_words_list):
    emission_counts = {}
    for tagged_word in tagged_words_list:
        # storing counts based on tag
        tag = tagged_word[1]
        word = tagged_word[0]
        if tag in emission_counts:
            tag_dict = emission_counts[tag]
            if word in tag_dict:
                tag_dict[word] += 1.0
            else:
                tag_dict[word] = 1.0
        else:
            emission_counts[tag] = {word : 1.0}
    return emission_counts

def get_emission_probs(dict_of_dicts):
    emission_probs = {}
    for tag in dict_of_dicts.keys():
        total_count = 0.0
        emission_probs[tag] = {}
        tag_dict = dict_of_dicts[tag]
        for word in tag_dict.keys():
            total_count += tag_dict[word]
        for word in tag_dict.keys():
            emission_probs[tag][word] = tag_dict[word]/total_count
    return emission_probs

if __name__ == "__main__":
    main()