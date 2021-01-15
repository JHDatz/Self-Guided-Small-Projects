## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-10-16

# This is the function that we are trying to optimize.
# X and W are needed for the denominator of logRegOutput.
# Y is needed to construct the vector of all probability
# outputs which go to the correct class in the Numerator
# of logRegOutput.

function [O] = objective_function (X, Y, W)
  
  [N, D] = logRegOutput(X, W);

  A = zeros(length(J), 1);
  for i = 1:length(J)
    A(i) = N(i, Y(i));
  endfor

  O = sum(log(A)-log(D));

endfunction
