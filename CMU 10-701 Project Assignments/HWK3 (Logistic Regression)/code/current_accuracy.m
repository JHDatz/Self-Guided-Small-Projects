## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-10-17

# This is a quick write-up to turn evaluating accuracy into a one liner.
# X and Y are the data we're evaluating the accuracy of, W is the matrix
# of the Logistic Regression model.

function [accuracy] = current_accuracy (X, Y, W)
  
  accuracy = (Y == predictions(X,W))/length(Y);

endfunction
