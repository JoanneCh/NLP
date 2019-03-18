### Overview
It's a Hidden Markov Model part-of-speech tagger for English and Chinese. The training data are provided tokenized and tagged; the test data will be provided tokenized, and the tagger will add the tags.

The hmmlearn3.py will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt.

The hmmdecode3.py will read the parameters of a hidden Markov model from the file hmmmodel.txt, use Viterbi algrithom to tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

### Data
* Two files (one English, one Chinese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
* Two files (one English, one Chinese) with untagged development data, with words separated by spaces and each sentence on a new line.
