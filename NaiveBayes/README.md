# Naive Bayes Classifier

### Overview
It's a naive Bayes classifier to identify hotel reviews as either true or fake, and either positive or negative. It uses the word tokens as features for classification. 

The nblearn3.py will learn a naive Bayes model from the training data, and the nbclassify3.py will use the model to classify new data. 

### Data
* One file train-labeled.txt containing labeled training data with a single training instance (hotel review) per line (total 960 lines). The first 3 tokens in each line are:
    1. a unique 7-character alphanumeric identifier
    2. a label True or Fake
    3. a label Pos or Neg
* These are followed by the text of the review.
* One file dev-text.txt with unlabeled development data, containing just the unique identifier followed by the text of the review (total 320 lines).
* One file dev-key.txt with the corresponding labels for the development data, to serve as an answer key.