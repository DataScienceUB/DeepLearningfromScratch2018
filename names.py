from __future__ import absolute_import, division, print_function

import tflearn

def textfile_to_seq(file, seq_maxlen=25, redun_step=3):
    """ string_to_semi_redundant_sequences.
    Vectorize a string and returns parsed sequences and targets, along with
    the associated dictionary.
    Arguments:
        string: `str`. Lower-case text from input text file.
        seq_maxlen: `int`. Maximum length of a sequence. Default: 25.
        redun_step: `int`. Redundancy step. Default: 3.
    Returns:
        `tuple`: (inputs, targets, dictionary)
    """
    import numpy as np
    import re
    print("Vectorizing text...")
    
    import codecs
    f = codecs.open('toponims.txt', "r", "utf-8")
    string = f.read()
    string.encode('utf-8')
    string = re.sub( '([A-Z])', '^\\1', string ).lower()
    chars = set()
    chars.update(string)
    char_idx = {c: i for i, c in enumerate(chars)}

    sequences = []
    next_chars = []
    for i in range(0, len(string) - seq_maxlen, redun_step):
        sequences.append(string[i: i + seq_maxlen])
        next_chars.append(string[i + seq_maxlen])

    X = np.zeros((len(sequences), seq_maxlen, len(chars)), dtype=np.bool)
    Y = np.zeros((len(sequences), len(chars)), dtype=np.bool)
    for i, seq in enumerate(sequences):
        for t, char in enumerate(seq):
            X[i, t, char_idx[char]] = 1
        Y[i, char_idx[next_chars[i]]] = 1

    print("Text total length: " + str(len(string)))
    print("Distinct chars: " + str(len(chars)))
    print("Total sequences: " + str(len(sequences)))
    return X, Y, char_idx

def random_sequence_from_string(string, seq_maxlen):
    import random
    rand_index = random.randint(0, len(string) - seq_maxlen - 1)
    return string[rand_index: rand_index + seq_maxlen]

def random_sequence_from_textfile(path, seq_maxlen):
    import codecs
    import re
    f = codecs.open(path, "r", "utf-8")
    text = f.read()
    text.encode('utf-8')
    text = re.sub( '([A-Z])', '^\\1', text ).lower()
    return random_sequence_from_string(text, seq_maxlen)

path = 'toponims.txt'
maxlen = 20

X, Y, char_idx = \
    textfile_to_seq(path, seq_maxlen=maxlen, redun_step=3)

g = tflearn.input_data(shape=[None, maxlen, len(char_idx)])
g = tflearn.lstm(g, 64, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 64)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                       learning_rate=0.01)

m = tflearn.SequenceGenerator(g, dictionary=char_idx,
                              seq_maxlen=maxlen,
                              clip_gradients=5.0)

for i in range(100):
    seed = random_sequence_from_textfile(path, maxlen)
    m.fit(X, Y, validation_set=0.1, batch_size=128,
          n_epoch=1, run_id='toponims')
    print("-- TESTING...")
    print("-- EPOCH = ", i)
    print("-- Test with temperature of 1.2 --")
    print(m.generate(30, temperature=1.2, seq_seed=seed))
    print("-- Test with temperature of 1.0 --")
    print(m.generate(30, temperature=1.0, seq_seed=seed))
    print("-- Test with temperature of 0.5 --")
    print(m.generate(30, temperature=0.5, seq_seed=seed))