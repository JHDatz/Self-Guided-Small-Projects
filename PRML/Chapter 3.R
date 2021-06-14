# Joseph Datz
# 6/14/21
#
# This file is a set of functions made from Chapter 3 of Pattern Recognition
# and Machine Learning. It is meant to turn the mathematical operations of
# the book into functioning code.
#
# Chapter 3 Cover Bayesian Linear Regression methods. We start with the model
# assumption that our data can be modeled with a system of linear weights, and
# errors are normally distributed for some given precision. This leads to an MLE
# solution, a Bayesian MAP solution when we presume to know the precision, and
# then finally a MAP solution where the precision is not known.

# Solving for the best weights w under a least square approach. This is the
# solution suggested by a Maximum Likelihood Approach.

compute_weights <- function(X, Y, phi) {
  
  Phi <- sapply(phi, function(base) base(X))
  solve(t(Phi) %*% Phi) %*% t(Phi) %*% Y
  
}

# After getting weights w, this function gives output for the
# regression function.

compute_regression_curve <- function (xs, W, phi) {
  
  matr <- sapply(phi, function(base) base(xs))
  apply(matr, 1, function(row) sum(row*W))
  
}

# Provides a graph of a function after weights w are found.

draw_regression <- function(X, W, phi) {
  
  xs <- seq(min(X), max(X), len=50)
  ys_hat <- compute_regression_curve(xs, W, phi)
  points(xs, ys_hat, type="l", col="red")
  
}

# A set of example basis functions for modifying the data before collecting
# weights.

one <- function(x) rep(1,length(x))
id  <- function(x) x
sq  <- function(x) x^2
x3  <- function(x) x^3
x4  <- function(x) x^4

# Some example data for producing a curve. 

X <- c(1,2,3,5,7)
Y <- c(3,5,6,12,21)

# A simple line function. We compute weights but do not take
# advantage of our draw_regression() function yet.

phi <- c(one, id)
W <- compute_weights(X, Y, phi)

plot(X,Y,pch=19)
abline(W, col="red")

# A quadratic curve fit.

phi <- c(one, id, sq)
W <- compute_weights(X, Y, phi)

plot(X,Y,pch=19)
draw_regression(X,W,phi)

# A much more unique choice of using sin(x) as part of the curve fit.

phi <- c(one, id, function(x) sin(x))
W <- compute_weights(X, Y, phi)
plot(X,Y,pch=19)
draw_regression(X,W,phi)

# With regularization we can penalize the usage of heavy weights. In fact,
# regularization implicitly creates a constraint through the usage of Langrange
# Multipliers. This can allow us to safely use more complex models with a
# lesser risk of overfitting.

# This function uses regularization with the euclidean distance (gaussian prior).
# Other distance values can also be used if desired.

compute_regularized_weights <- function(X, Y, phi, lambda) {
  Phi <- sapply(phi, function(base) base(X))
  
  solve(lambda*diag(length(phi)) + t(Phi) %*% Phi) %*% t(Phi) %*% Y
}

# Two plots are used to generate a comparison. With no regularization, all
# points are matched exactly. With regularization, only the last point is

X <- c(1,2,3,5,7)
Y <- c(3,5,1,12,10)
phi <- c(one, id, sq, x3, x4)

par(mfrow=c(1,2))
W <- compute_weights(X, Y, phi)
plot(X, Y, pch=19, main = "No Regularization")
draw_regression(X, W, phi)

W <- compute_regularized_weights(X, Y, phi, 11)
plot(X, Y, pch=19, main = "With Lambda = 11")
draw_regression(X, W, phi)

# If we don't have all the data right away, a sequential learning model is
# necessary. This function computes updated weights using stochastic gradient
# descent for the Maximum Likelihood approach. Note that this does not converge.

