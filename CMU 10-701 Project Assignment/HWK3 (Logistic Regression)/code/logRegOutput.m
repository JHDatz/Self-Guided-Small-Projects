## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-10-17

# This function is a partially complete formula for logistic
# Regression. It's kept partial in case another function needs
# the numerator or denominator separately instead of the
# probability calculation, but it can be completed by typing
# "N./D".

function [N, D] = logRegOutput(X, W)
  N = exp(X*W');
  D = 1 + sum(N(:, 1:end-1), 2);

endfunction
