## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-06-30

## This file is used as the master script that ties in MLE and MAP estimates
## for the Naive Bayes Multinomial model. We will be computing both estimates,
## testing the accuracy of both, graph the accuracy of the MAP model on a log 
## plot, and create a statistic using information theory to find which words 
## are the most important in predictions.

clear; clc;
pkg load statistics

# Load in the data and transform it into a matrix.

[X_train, Y_train] = readInData('train.data', 'train.label', 'vocabulary.txt');
[X_test, Y_test] = readInData('test.data', 'test.label', 'vocabulary.txt');

# Compute the Maximum Likelihood Estimate to train the model.

params = maxLikelyEstimates(X_train, Y_train);

# Test the overall accuracy of the MLE parameters on the test data.

Y_hat = predictions(X_test, params);
sum(Y_test == Y_hat)/length(Y_test)
A = confusemat(Y_test, Y_hat)

# Now working with the MAP estimates, use the best parameter according to the
# homework sheet and test the overall accuracy.

params2 = mapEstimates(X_train, Y_train, i);
Y_bayes_hat = predictions(X_test, params2);
sum(Y_test == Y_bayes_hat)/length(Y_test)
A = confusemat(Y_test, Y_bayes_hat)

# Since there is a free parameter in the Maximum a Posteriori estimate, we search
# a large space of possible choices for the parameter to find the best choice.

parameter_accuracy = [];

for i = 0:0.00001:1
  
  # Compute the MAP estimate, calculate accuracy, and track the accuracy change.
  
  params2 = mapEstimates(X_train, Y_train, i);
  Y_bayes_hat = predictions(X_test, params2);
  parameter_accuracy = [parameter_accuracy, sum(Y_test == Y_bayes_hat)/length(Y_test)];

endfor