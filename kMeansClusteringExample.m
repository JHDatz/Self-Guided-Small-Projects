## Author: Joseph Datz
## Created August 2020

# Create a synthetic distribution first to model after.

clear; clc

mu = [1 2;-3 -5];
sigma = [1 1];
gm = gmdistribution(mu,sigma);
coords = random(gm,100);
initialization = [-4, 0; 2, -4]; # Start with a guess for where the center is.

# Next is the algorithm for k-means clustering; assign a data point to a cluster,
# and then readjust the position of the cluster. Repeat until convergence.

for j = 1:3
  distance = [];
  for i = 1:size(initialization)(1)
    distance = [distance; sum((coords' - initialization(i,:)').^2)]; # Compute the distance of each data point to the two clusters.
  endfor
  
  # Assignment of each data point to the clusters.

  [maxes, clusterID] = max(distance);
  temp = [clusterID', coords];
  
  # Draw a plot a few times to show convergence of the clusters.

  hold on;
  axis ([-6 4 -8 6])
  h1 = scatter(temp(temp(:,1) == 1, 2), temp(temp(:,1) == 1, 3),10, 'filled', 'r');
  h2 = scatter(temp(temp(:,1) == 2, 2), temp(temp(:,1) == 2, 3),10,'filled', 'b');
  h3 = scatter(initialization(1,1), initialization(1,2), 50, 'r', 'x');
  h4 = scatter(initialization(2,1), initialization(2,2), 50, 'b', 'x');
  pause()
  delete(h1)
  delete(h2)
  delete(h3)
  delete(h4)

  #. Calculate new center
  for i = 1:size(initialization)(1)
    initialization(i, :) = sum(temp(temp(:,1) == i, 2:size(temp)(2)))/length(temp(temp(:,1) == i));
  endfor
endfor
