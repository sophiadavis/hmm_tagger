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



# am I doing the first part correctly?
# somehow smooth counts


# Like the last assignment, you will need to deal with unknown words and their probabilities. 
# Begin with a simple estimator, using a single <UNK> token to handle this.
# 
# If you have time, check out the books suggestions for this in section 5.8.2.
import pickle
import sys
import re


def main():
    # 
    model = pickle.load( open('model_newest.dat', 'r') ) # model = [transition_probs, emission_probs, tag_list, vocabulary]
    vocabulary = model[3]
    cleaned_input = []
    word_sequence = []
    for line in sys.stdin:
        words = line.split(' ')
        for word in words:
            word = re.sub(r"\\\/", r"", word) # for words separated with white space
            word = re.sub(r"([.,!?:;()@#$%^&*{}|\/<>~`'])", r" \g<1>", word) # separate punctuation from words
            tokens = word.split(' ')
            for token in tokens:
                cleaned_input.append(token)
        for word in cleaned_input:    
            if word in vocabulary:
                word_sequence.append(word)
            else:
                word_sequence.append('<unknown>')
    hmm_viterbi(word_sequence, model)

def hmm_viterbi(sequence, hmm_model):
    v_zeros = initialization(sequence, hmm_model)
    viterbi_matrix = recursion_step(v_zeros, sequence, hmm_model)
    final_step = termination(viterbi_matrix, sequence, hmm_model)
    viterbi_matrix_final = final_step[0]
    argmax = final_step[1][1]
#     print 'final argmax: ' + argmax
    time_step = len(sequence) - 1
    path = []
    while time_step != 0:
        print viterbi_matrix_final[time_step][argmax]
        current_argmax = viterbi_matrix_final[time_step][argmax][1]
        path.append(current_argmax)
        argmax = viterbi_matrix_final[time_step][argmax][1]
        time_step -= 1
    print path
    
    
def initialization(sequence, hmm_model):
    
    transition_probs = hmm_model[0]
    emission_probs = hmm_model[1]
    tag_list = hmm_model[2]
    print transition_probs
    print emission_probs
    print tag_list
    
    # storing each timestep as a separate entry in a dictionary
    # each timestep consists of another dictionary of  { tag : [max, argmax] }
    viterbi = {0 : {} }
    word = sequence[0] 
    for tag in tag_list:
        if tag in transition_probs['q_zero']:
            a = transition_probs['q_zero'][tag]
        else:
            a = transition_probs['q_zero']['other']
        if word in emission_probs[tag]:
            b = emission_probs[tag][word]
        else:
            b = emission_probs[tag]['<unknown>'] 
        viterbi[0][tag] = [a*b]
    return viterbi

def recursion_step(viterbi, sequence, hmm_model):
    
    transition_probs = hmm_model[0]
    emission_probs = hmm_model[1]
    tag_list = hmm_model[2]
    
    time_step = 1
    
    while time_step < len(sequence):
        viterbi[time_step] = {}
        word = sequence[time_step]
        
        for tag in tag_list:
            max = 0
            for tag_previous in viterbi[time_step - 1]:
                v_previous = viterbi[time_step - 1][tag_previous][0]
                if tag in transition_probs[tag_previous]:
                    a = transition_probs[tag_previous][tag]
                else:
                    a = transition_probs[tag_previous]['other']
                if word in emission_probs[tag]:
                    b = emission_probs[tag][word]
                else:
                    b = emission_probs[tag]['<unknown>'] 
                v_current = v_previous * a * b
                if v_current > max:
                    max = v_current
                    argmax = tag_previous
            viterbi[time_step][tag] = [max, argmax]
        time_step += 1
    return viterbi

def termination(viterbi, sequence, hmm_model):
    
    transition_probs = hmm_model[0]
    emission_probs = hmm_model[1]
    tag_list = hmm_model[2]
    
    final_time_step = len(sequence)
    viterbi[final_time_step] = {}
    
    for tag_previous in tag_list:
        max = 0
        if 'q_final' in transition_probs[tag_previous]:
            a = transition_probs[tag_previous]['q_final']
        else:
            a = transition_probs[tag_previous]['other']
        v_previous = viterbi[final_time_step - 1][tag_previous][0]
        v_current = v_previous * a
        if v_current > max:
            max = v_current
            argmax = tag_previous
    viterbi[final_time_step]['q_final'] = [max, argmax]
    return viterbi, [max, argmax]
    
if __name__ == "__main__":
    main()