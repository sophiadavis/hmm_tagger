# Write an program named hmm_tagger.py or HmmTagger.java that acts as an HMM by using the 
# Viterbi algorithm and the model file that you created to determine the most probable tag 
# sequence given a sequence of words/tokens. The program should read the sequence of tokens 
# from standard input, then load the model file, then use that to output a tag sequence, 
# with the corresponding words. The word sequence input will be the .pos files piped 
# through the following sed script:


# read from stdin
# load model file
# deal with unknown words
# output tag sequence with corresponding words


# Like the last assignment, you will need to deal with unknown words and their probabilities. 
# Begin with a simple estimator, using a single <UNK> token to handle this.
# 
# If you have time, check out the books suggestions for this in section 5.8.2.
import pickle
import sys

def main():
    # 
    model = pickle.load( open('model.dat', 'r') ) # model = [transition_probs, emission_probs, tag_list, vocabulary]
    transition_probs = model[0]
    emission_probs = model[1]
    tag_list = model[2]
    vocabulary = model[3]
    
    word_sequence = ''
    for line in sys.stdin:
        for word in line:
            word_sequence = word_sequence + word
    
            
    

if __name__ == "__main__":
    main()