# hmm_tagger.py, Sophia Davis, for 10/25/2013
# This program takes a sequence of words from standard input, and uses the hmm model created
# in hmm_model.py and the Viterbi algorithm to determine the most probable sequence of POS
# tags for the word sequence.

import pickle
import sys
import re

def main():
    model = pickle.load( open('model.dat', 'r') ) # model = [transition_probs, emission_probs, tag_list, vocabulary]
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
                token = re.sub(r"\n", r"", token)
                if token:
                    cleaned_input.append(token)  # strip whitespace (from punctuation)
        for word in cleaned_input: 
            if word in vocabulary:
                word_sequence.append(word)
            else:
                word_sequence.append('<unknown>')
    path = hmm_viterbi(word_sequence, model)
    path.reverse()
    output = ''
    for i in range(0, len(cleaned_input)):
        tagged_word = cleaned_input[i] + '/' + path[i] + ' '
        output = output + tagged_word
    print output

# takes an hmm model and word sequence
# 'guides' sequence of words through steps of Viterbi algorithm
# Viterbi probabilities are stored in a dictionary of { time step : { tag : [max, argmax] } }
def hmm_viterbi(sequence, hmm_model):
    v_zeros = initialization(sequence, hmm_model)
    viterbi_matrix = recursion_step(v_zeros, sequence, hmm_model)
    final_step = termination(viterbi_matrix, sequence, hmm_model)
    viterbi_matrix_final = final_step[0]
    argmax = final_step[1][1]
    time_step = len(sequence) - 1
    path = [argmax]
    while time_step != 0:
        current_argmax = viterbi_matrix_final[time_step][argmax][1]
        path.append(current_argmax)
        argmax = viterbi_matrix_final[time_step][argmax][1]
        time_step -= 1
    output = ''
    return path

# initialization step of the Viterbi algorithm
# takes a sequence of words and an hmm model and calculates probabilities of each possible tag
# starting the given sequence
# returns a dictionary of { time_step_0 : { tag : [max, argmax] } }
def initialization(sequence, hmm_model):
    transition_probs = hmm_model[0]
    emission_probs = hmm_model[1]
    tag_list = hmm_model[2]
    
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
            b = 0
        viterbi[0][tag] = [a*b]
    return viterbi

# recursion step of the Viterbi algorithm
# takes a sequence of words and an hmm model and calculates Viterbi probabilities for all tags
# at each time step, by keeping track of maximum probabilities from all tags at each 
# previous time step and the argmax that produced them
# returns a dictionary of { time_step : { tag : [max, argmax] } }
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
            argmax = None
            for tag_previous in tag_list:
                v_previous = viterbi[time_step - 1][tag_previous][0]
                if tag in transition_probs[tag_previous]:
                    a = transition_probs[tag_previous][tag]
                else:
                    a = transition_probs[tag_previous]['other']
                if word in emission_probs[tag]:
                    b = emission_probs[tag][word]
                else:
                    b = 0
                v_current = v_previous * a * b
                if v_current > max:
                    max = v_current
                    argmax = tag_previous
            if argmax:        
                viterbi[time_step][tag] = [max, argmax]
            else:
                viterbi[time_step][tag] = [0, 'Oops'] # hopefully this never happens
        time_step += 1
    return viterbi

# termination step of the Viterbi algorithm
# takes a sequence of words and an hmm model and calculates probabilities of each possible tag
# ending the given sequence
# returns a dictionary of { time_step_final : { tag : [max, argmax] } } and the final [max, argmax] pair
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