# hmm_model.py, Sophia Davis, for 10/25/2013
# This program reads in a list of files containing a POS-tagged corpus from from the command line,
# calculates transition and emission probabilities, and generates a vocabulary and list of 
# tags. This hmm model is then 'pickled,' and can then be used by the hmm_tagger.py program  
# to tag new text.

import sys
import re
import pickle
from sets import Set

def main():
    corpus = ''
    
    print "Initializing corpus..."
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
    
    # split corpus into each token/tag unit
    observations = get_tagged_list(corpus)
    
    total_tag_list = observations[0]
    vocabulary = observations[2]

    # get transition probabilities
    transition_counts = get_transition_counts(total_tag_list)
    transition_probs = get_transition_probs(transition_counts)
    tag_list = transition_counts.keys()
    tag_list = [tag for tag in tag_list if tag not in ['q_zero', 'q_final']]

    # get emission probabilities
    tagged_observations = observations[1]
    emission_counts = get_emission_counts(tagged_observations)
    emission_probs = get_emission_probs(emission_counts)
    
    to_pickle = [transition_probs, emission_probs, tag_list, vocabulary]
    pickle.dump(to_pickle, open('model.dat', 'w'))
    print "Saving to model.dat"

# splits a tagged corpus into units of word/tag
# returns a list of all tags in corpus, all words in corpus (vocabulary), and a list of word/tag units
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
        token = re.sub(r"\\\/", r"", token) # remove \/ from words containing white space
        token = re.sub(r"(.*)(\|)(.*)", r"\g<1>", token) # if words have been tagged 
                                                    # with multiple tags, take the first
        tagged_token = token.split('/')
        word = tagged_token[0]
        tag = tagged_token[1]
        
        if tag == 'q_zero' and len(total_tag_list) > 0: # don't add q_final to the beginning of the list
            total_tag_list.append('q_final')
        total_tag_list.append(tag)
        tagged_tokens_list.append(tagged_token)
        vocabulary.add(word)
    total_tag_list.append('q_final') # add last final tag to list
    return total_tag_list, tagged_tokens_list, vocabulary

# takes a list of all tags in corpus, produces dictionary of transition counts
# each key is the first tag in the bigram sequence
# its values are a dictionary of {ending tag : count}
def get_transition_counts(tag_list):    
    transition_counts = {}
    for i in range(0, len(tag_list) - 1):
        tag_one = tag_list[i]
        tag_two = tag_list[i + 1]
        if tag_one in transition_counts:
            tag_one_dict = transition_counts[tag_one]
            if tag_two in tag_one_dict:
                tag_one_dict[tag_two] += 1.0
            else:
                tag_one_dict[tag_two] = 1.0
        else:
            transition_counts[tag_one] = {'other' : 0.0, tag_two : 1.0} 
    return transition_counts

# takes dictionary of tag transition counts and converts these to 
# a dictionary of tag transition probabilities
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
        values = filter(lambda x: x != 0.0, transition_probs[tag_one].values())
        minimum = min(values)
        transition_probs[tag_one]['other'] = minimum/100 # this pseudo-smoothing method
                                # means "probabilities" will not sum to one, but seems to
                                # be fairly effective
    return transition_probs

# takes a list of all units of word/tag in corpus, produces dictionary of emission counts
# each key is a tag
# its values are a dictionary of {word : count}
def get_emission_counts(tagged_words_list):
    emission_counts = {}
    for tagged_word in tagged_words_list:
        tag = tagged_word[1]
        word = tagged_word[0]
        if tag in emission_counts:
            tag_dict = emission_counts[tag]
            if word in tag_dict:
                tag_dict[word] += 1.0
            else:
                tag_dict[word] = 1.0
        else:
            emission_counts[tag] = {'<unknown>' : 0.0, word : 1.0}
    return emission_counts

# takes dictionary of tag transition counts and converts these to 
# a dictionary of tag transition probabilities
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
        values = filter(lambda x: x != 0.0, emission_probs[tag].values())
        minimum = min(values)
        emission_probs[tag]['<unknown>'] = minimum/100  # again, pseudo-smoothing method
    return emission_probs

if __name__ == "__main__":
    main()