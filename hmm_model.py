# cat wsj_*.pos | sed 's/^\[ //g;s/ \] *$//g' > wsj.txt
import sys
import re
# create test set
# deal with stupid ==== problem


tag_list = []
emission_probs = {}

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
    tag_list = get_tag_list(corpus)
    transition_counts = get_transition_counts(tag_list)
    get_transition_probs(transition_counts)
    print "Saving to model.dat"

def get_tag_list(text):
    total_tag_list = []
    for token in text:
        token = re.sub(r"\n", "", token)
        if token.startswith('='):
            token = 'q_zero/q_zero'
        if token == '':
            continue
        tagged_token = token.split('/')
        word = tagged_token[0] 
        tag = tagged_token[1]
        total_tag_list.append(tag)
    return total_tag_list

def get_transition_counts(list):    
    transition_counts = {}
    for i in range(0, len(list) - 1):
        # storing bigram tag counts based on first tag in sequence
        tag_one = list[i]
        tag_two = list[i + 1]
        if tag_one in transition_counts:
            tag_one_dict = transition_counts[tag_one]
            if tag_two in tag_one_dict:
                count = tag_one_dict[tag_two]
                tag_one_dict[tag_two] += 1.0
            else:
                tag_one_dict[tag_two] = 1.0
        else:
            transition_counts[tag_one] = {tag_two : 1}
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
            print 'tag_two_count: '
            print tag_one_dict[tag_two]
            print 'total: '
            print total_count
            print 'probability?: '
            print tag_one_dict[tag_two]/total_count
            print
    print transition_probs
    return transition_probs
            
            
            
            
    

# Determine your transition probability matrix A, and emission probabilities B, by using 
# counts from the corpus. Use a bigram Markov assumption to calculate the A matrix from the training data.

# Write a program called hmm_model.py or HmmModel.java that will create a model from a set 
# of pos-tagged training files. It should take as a command-line argument a list of files 
# to use for input, and output a the model to a file named model.dat. You can use pickle, text or java stuff 


if __name__ == "__main__":
    main()