## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-06-30

## This short function provides all prediction outputs on a dataset X with
## a given set of parameters. The log() function is used instead of the
## probabilities directly to make the computation favorable to matrix multiplication.

function [predict] = predictions(X, params)
  
  [maxValue, predict] = max(log(params)*[ones(size(X)(1), 1), X]');
  predict = predict';

endfunction
