## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-06-30

## This function provides the Maximum a Posterior (MAP) estimates of the Naive
## Bayes model. The justifications for the formula can be found on the homework
## solution page. To compute the estimates, we need the training data X and Y
## as well as a free-to-vary parameter alpha.

## The returning matrix params gives us the prior estimate of P(Y) in the first
## column as well as the parameter estimates for the words. The rows constitute
## classes, and columns constitute word estimates.

function [params] = mapEstimates (X, Y, alpha)
  
  params = [];
  
  temp = [Y, X];
  
  # Parse the temp matrix by the classes to compute P(Mu | D)*P(Mu) for each
  # word and class, and compute an estimate for P(Y).
  
  for i = 1:max(Y(:, 1))
    compute_params = (sum(temp(temp(:,1) == i, 2:end)) + alpha)/(sum(sum(temp(temp(:, 1) == i, 2:end))) + size(X)(2)*alpha);
    prior_on_y = length(temp(temp(:, 1) == i))/size(temp)(1);
    params = [params; [prior_on_y, compute_params]];

  endfor

endfunction
