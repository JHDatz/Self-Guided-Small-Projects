## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-06-30

## This function provides the Maximum Likelihood (MLE) estimates of the Naive
## Bayes model. The justifications for the formula can be found on the homework
## solution page. To compute the estimates, we need the training data X and Y.

## The returning matrix params gives us the prior estimate of P(Y) in the first
## column as well as the parameter estimates for the words. The rows constitute
## classes, and columns constitute word estimates.

function [params] = maxLikelyEstimates(X, Y)
  
  params = [];
  
  temp = [Y, X];
    
  for i = 1:max(Y(:, 1))
    compute_params = (sum(temp(temp(:,1) == i, 2:end)))/(sum(sum(temp(temp(:, 1) == i, 2:end))));
    prior_on_y = length(temp(temp(:, 1) == i))/size(temp)(1);
    params = [params; [prior_on_y, compute_params]];

  endfor

endfunction
