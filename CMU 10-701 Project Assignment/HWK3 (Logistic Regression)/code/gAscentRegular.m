## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-10-16

# This function holds the equation for updating the parameters
# of the logistic regression model, using regularization to deter
# overfitting of the model. X_train and Y_train are a necessary 
# part of the update formula, W is needed for updating to take 
# place, and eta is the learning rate parameter for gradient 
# ascent/descent optimization.

function [W] = gAscentRegular(X_train, Y_train, W, eta, lambda)
  
   [N, D] = logRegOutput(X_train, W);
   prob = N./D;
   
   W(1:end-1, :) = W(1:end-1, :) + eta*((cat2bin(Y_train) - prob)'*X_train)(1:end-1, :) - lambda*eta*W(1:end-1, :);

endfunction
