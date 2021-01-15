pkg load statistics
pkg load nan
clear; clc;

# Set parameters.

iterations = 5000
eta = 0.0001
#lambda = 1

# Load in data.

X_train = dlmread('tr_X.txt'); Y_train = dlmread('tr_y.txt');
X_test = dlmread('te_X.txt'); Y_test = dlmread('te_y.txt');

# Construct vectors for tracking the objective function and accuracy.

objective_tracker = zeros(1, iterations); train_error_tracker = zeros(1, iterations); test_error_tracker = zeros(1, iterations);

# Generate random initial weights. The kth class is constrained to have all
# zeroes for its vector.

W = [rand(max(Y_train)-1,size(X_train)(2)); zeros(1, size(X_train)(2))];

eta = 0.0001;

for i = 1:5000
  
  # Update W with the Gradient Ascent function. gAscent or gAscentRegular can
  # be used here.
  
  W = gAscent(X_train, Y_train, W, eta);
  # W = gAscentRegular(X_train, Y_train, W, eta, lambda)
   
  # Update objective function output and accuracy to reflect updates to W.
   
  objective_tracker(i) = objective_function(X_train, Y_train, W);
  train_error_tracker(i) = current_accuracy(X_train, Y_train, W);
  test_error_tracker(i) = current_accuracy(X_test, Y_test, W);

endfor

plot(1:length(objective_tracker), objective_tracker);
plot(1:length(objective_tracker), train_error_tracker);
hold on;
plot(1:length(objective_tracker), test_error_tracker);
