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
# import pdb
# pdb.set_trace()

def main():
    # 
    model = pickle.load( open('model.dat', 'r') ) # model = [transition_probs, emission_probs, tag_list, vocabulary]
    vocabulary = model[3]
    word_sequence = []
    for line in sys.stdin:
        for word in line:
            if word in vocabulary:
                word_sequence.append(word)
            else:
                word_sequence.append('<unknown>')
    hmm_viterbi(word_sequence, model)

def hmm_viterbi(sequence, hmm_model):
    v_zeros = initialization(sequence, hmm_model)
    viterbi_body = recursion_step(v_zeros, sequence, hmm_model, 1) # , []
    viterbi_final = termination(viterbi_body, sequence, hmm_model)
    
def initialization(sequence, hmm_model):
    
    transition_probs = hmm_model[0]
    emission_probs = hmm_model[1]
    tag_list = hmm_model[2]
    
    N = len(tag_list)
    viterbi = {0 : {} }
    word = sequence[0] 
    for tag in tag_list:
#         print 'Nth tag is: ' + tag
        if tag in transition_probs['q_zero']:
            a = transition_probs['q_zero'][tag]
        else:
            a = transition_probs['q_zero']['other']
        b = emission_probs[tag][word]
        viterbi[0][tag] = [a*b]
#         print 'current probabilities: '
#         print a, b
#         print viterbi[0][tag]
#         print '---'
    return viterbi

def recursion_step(viterbi, sequence, hmm_model, time_step): # , path
    
    transition_probs = hmm_model[0]
    emission_probs = hmm_model[1]
    tag_list = hmm_model[2]
    
    while time_step < len(sequence):
        viterbi[time_step] = {}
        word = sequence[time_step - 1]
        for tag in tag_list:
            max = 0
#             print 'Nth tag is ' + tag
            for tag_previous in viterbi[time_step - 1]:
#                 print 'Looking at previous viterbi step: ' + tag_previous
                v_previous = viterbi[time_step - 1][tag_previous][0]
                if tag in transition_probs[tag_previous]:
                    a = transition_probs[tag_previous][tag]
                else:
                    a = transition_probs[tag_previous]['other']
                b = emission_probs[tag][word]
                v_current = v_previous*a*b
#                 print 'current probabilities are: '
#                 print a, b, v_previous
#                 print
                if v_current > max:
#                     print 'new max!'
                    max = v_current
                    best_previous_tag = tag_previous
#             print time_step
#             print viterbi[time_step]
            viterbi[time_step][tag] = [max, best_previous_tag]
#             print ' ----- '
        new_max = 0
        for key in viterbi[time_step]:
            if viterbi[time_step][key][0] > new_max:
                new_max = viterbi[time_step][key][0]
                new_best = viterbi[time_step][key][1] 
        print new_max
        print new_best
     
#         path.append(new_best)
        time_step += 1
    return viterbi

def termination(viterbi, sequence, hmm_model):
    
    transition_probs = hmm_model[0]
    emission_probs = hmm_model[1]
    tag_list = hmm_model[2]
    
    viterbi = {0 : {} }
    word = sequence[0] 
    for tag in tag_list:
#         print 'Nth tag is: ' + tag
        if tag in transition_probs['q_zero']:
            a = transition_probs['q_zero'][tag]
        else:
            a = transition_probs['q_zero']['other']
        b = emission_probs[tag][word]
        viterbi[0][tag] = [a*b]
#         print 'current probabilities: '
#         print a, b
#         print viterbi[0][tag]
#         print '---'
    return viterbi
    

    
            
    

if __name__ == "__main__":
    main()