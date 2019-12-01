# Example of getting neighbors for an instance
import math, random, warnings
import numpy as np
import pandas as pd
from math import sqrt
from scipy.spatial import distance
from collections import Counter

def get_k_neighbors(fonts, predict, k, num_neighbors):
    # if len(fonts) >= k:
    #     warnings.warn('K is set to a value less than total voting groups!')
    distances = []

    for font in fonts.iterrows():
        print('font: ',font)
        for features in fonts[font]:
            print('features: ',features)
            euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([euclidean_distance,font])

    similar = sorted(distances)
    dissimilar = sorted(distances, reverse=True)

    return similar[0:num_neighbors], dissimilar[0:num_neighbors]

# calculate the Euclidean distance between two vectors
def euclidean_distance(row1, row2):
    distance = 0.0
    print('row1:\n',row1)
    print('row2:\n',row2)
    print(len(row1))
    # distance += np.square(row1 - row2)
    for i in range(len(row1)-1):
        # distance += (row1[i] - row2[i])**2
        print('row1[i]:\n',row1[i])
        print('row2[i]:\n',row2[i])
        distance += np.square(row1[i] - row2[i])
    return sqrt(distance)

# def E_Distance(x1, x2, length):
#     distance = 0
#     for x in range(length):
#         distance += np.square(x1[x] - x2[x])
#     return np.sqrt(distance)

# Locate the most similar neighbors
def get_neighbors(train, test_row, num_neighbors):
    train = pd.DataFrame(train)
    print('train:\n',train)
    print('train type: ',type(train))
    print('indices: ',train.index)
    # train = train.reset_index()
    # print('new indices: ',train.index)
    # print(row = next(train.iterrows())[1])
    distances = list()
    for train_row in train.iterrows():
        print('train_row:\n',train_row)
        dist = euclidean_distance(test_row, train_row)
        # dist = distance.euclidean(train_row,test_row)
        # dist = math.sqrt(sum([(a - b) ** 2 for a, b in zip(train, test_row)]))
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1], reverse=True)
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors

# def get_neighbors(train, test_row, num_neighbors):
#     print('train:\n',train)
#     print('train type: ',type(train))
#     distances = list()
#     for train_row in train.iterrows():
#         print('train_row:\n',train_row)
#         dist = euclidean_distance(test_row, train_row)
#         # dist = distance.euclidean(train_row,test_row)
#         # dist = math.sqrt(sum([(a - b) ** 2 for a, b in zip(train, test_row)]))
#         distances.append((train_row, dist))
#     distances.sort(key=lambda tup: tup[1], reverse=True)
#     neighbors = list()
#     for i in range(num_neighbors):
#         neighbors.append(distances[i][0])
#     return neighbors

# Test distance function
dataset = [[2.7810836,2.550537003,0],
    [1.465489372,2.362125076,0],
    [3.396561688,4.400293529,0],
    [1.38807019,1.850220317,0],
    [3.06407232,3.005305973,0],
    [7.627531214,2.759262235,1],
    [5.332441248,2.088626775,1],
    [6.922596716,1.77106367,1],
    [8.675418651,-0.242068655,1],
    [7.673756466,3.508563011,1]]
# neighbors = get_neighbors(dataset, dataset[0], 3)
# for neighbor in neighbors:
#     print(neighbor)