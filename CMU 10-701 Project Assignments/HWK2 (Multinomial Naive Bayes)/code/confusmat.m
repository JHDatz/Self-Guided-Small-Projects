## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-06-30

## This short function provides a simple confusion matrix since it is not
## immediately available in Octave. Each row of the returning matrix A
## is the prediction made by the classifier, and each column is the actual
## class.

function [A] = confusmat(actual, predictions)
  
  A = zeros(max(actual), max(actual));
  
  for i = 1:max(actual)
    for j = 1:max(actual)
      A(i,j) = sum(((predictions == i) + (actual == j)) == 2);
    endfor
  endfor
  
  A = A';

endfunction
