## Author: Joseph Datz <joseph@joseph-Inspiron-15-3567>
## Created: 2020-06-30

## This function reads in the files of the data and converts them to a matrix
## format, making them much easier to work with. The data can also be loaded
## trainingfile.mat and testfile.mat, where they are preprocessed.

## In X, each row is an entry from an article, and each column represents a word
## from vocabulary.txt. The entries of the matrix are the counts of each word
## from every article.

## Y is simply a column with the class output of each row.

function [X, Y] = readInData(data, predictors, vocab)
  tempDataMatrix = dlmread(data, sep = ' ');
  vocab = textread(vocab, '%s');

  X = sparse(max(tempDataMatrix(:, 1)),length(vocab));
  Y = sparse(dlmread(predictors));
  row = 0;
  
  for i = 1:length(tempDataMatrix)
    if tempDataMatrix(i, 1) != row
      row = tempDataMatrix(i, 1);
    endif
    X(row, tempDataMatrix(i,2)) = tempDataMatrix(i, 3);
  endfor
  
endfunction
