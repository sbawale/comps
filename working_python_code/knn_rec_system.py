import os, webbrowser
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from preprocess_data_gf import *
from helper_functions import *
from similarity import *
from knn_scratch import *

# Preprocess data
fonts = preprocess_data_gf()
# print('fonts head: ',fonts.head())
# print('feature cols only: ', fonts[['category','is_body','is_italic','is_serif','weight']].head())
# print('keys: ', fonts.keys())
# print('find Yellowtail: ', fonts.loc['Yellowtail'])

# One-hot encode fonts for scaling
ohe_fonts = pd.concat(
    [pd.get_dummies(fonts[['family']]),
    pd.get_dummies(fonts[['category']]),
    pd.get_dummies(fonts[['weight']]),
    fonts[['is_body']],
    fonts[['is_serif']],
    fonts['is_italic']],
    axis=1)
print('ohe_fonts:\n',ohe_fonts)
# print('\nohe_fonts cols: ',ohe_fonts.columns)
# pd.DataFrame(ohe_fonts).to_csv(r'ohe.csv',header=True)
font_vectors = ohe_fonts

families = fonts['family'].unique()
categories = ['display','handwriting','monospace','serif','sans-serif']
font_weights = ['thin','extralight','light','regular','medium','semibold','bold','extrabold','black']

le_cat = LabelEncoder()
le_weight = LabelEncoder()
le_family = LabelEncoder()

le_cat.fit(categories)
le_weight.fit(font_weights)
le_family.fit(families)

copy = fonts

copy['category'] = le_cat.transform(copy['category'])
copy['weight'] = le_weight.transform(copy['weight'])
copy['family'] = le_family.transform(copy['family'])
# print(copy)
# scaler = MinMaxScaler()
scaler = StandardScaler()
scaler.fit_transform(copy[['family','category','weight']])
# print(copy)
# print("cat: ",cat)
# print('weight:',wt)
# print('fam:',fam)
# print(cat.shape)
# print(np.fliplr(cat).shape)

# cat_df = pd.DataFrame(data=cat,columns=['category'])
# wt_df = pd.DataFrame(data=cat,columns=['weight'])
# fam_df = pd.DataFrame(data=cat,columns=['family'])

# cat_df.reset_index(drop=True, inplace=True)
# wt_df.reset_index(drop=True, inplace=True)
# fam_df.reset_index(drop=True, inplace=True)

# # print('\ncat_df:\n',cat_df)

# temp1 = fonts[['is_body','is_serif','is_italic']]#.reset_index(drop=True, inplace=True)
# temp1 = temp1.reset_index(drop=True, inplace=True)
# # print(temp1)
# temp1 = pd.concat(
#     [fonts['is_body'],
#     fonts['is_serif'],
#     fonts['is_italic']],
#     axis=1)
# temp1 = temp1.reset_index(drop=True, inplace=True)
# temp2 = pd.concat([cat_df,wt_df,fam_df],axis=1)
# # print('\ntemp1:\n',temp1)
# # print('\ntemp2:\n',temp2)
# temp = pd.concat(
#     [temp1,
#     temp2],
#     axis=1)
# # print('temp:',temp)
# scaler = MinMaxScaler()
# scaler.fit_transform(temp)
# print('temp:',temp)
# print(cat.type)
# Scale one-hot encoded fonts
# min_max_scaler = MinMaxScaler()
# font_vectors = min_max_scaler.fit_transform(ohe_fonts)
# print('\nfont_vectors\n',font_vectors)
# pd.DataFrame(font_vectors).to_csv(r'vectors.csv', header=True)
# print(font_vectors.shape)

# Build KNN model using font vectors
# nbrs = NearestNeighbors(n_neighbors=200, metric='cosine', algorithm='auto').fit(font_vectors)
# distances, indices = nbrs.kneighbors(font_vectors)
nbrs = NearestNeighbors(n_neighbors=10, metric='euclidean', algorithm='auto').fit(font_vectors)
distances, indices = nbrs.kneighbors(font_vectors)
# print('\nknn model:\n',nbrs)
# print('\ndistances:\n',distances)
# print('\nindices:\n',indices)

# ************* Test 1 *************
choice = 'Open Sans 400'
# get_font_combinations(fonts,nbrs,choice,5)
full_recs = get_font_combinations(choice,fonts,font_vectors,nbrs,10)
# print(full_recs)
full_recs_df = pd.DataFrame(full_recs)
full_recs_df.to_csv(r'open_sans_k6.csv', index=None, header=True)
print('\nrecommendations:\n',full_recs)

print('\nNow testing knn from scratch...\n')
# Index: 1878
# print(font_vectors.head())
# print(font_vectors.keys())
# print(font_vectors.index)
# font_vectors = font_vectors.reset_index()
# print(font_vectors.keys())
# print(font_vectors['Abhaya Libre 500'])
neighbors = get_neighbors(font_vectors, font_vectors.loc[choice], 10)
print("\noriginal: \n",font_vectors.loc[choice])
print("neighbors:")
for neighbor in neighbors:
    print(neighbor)


# ************* Test 2 *************
# current = font_vectors[5]
# # print('\ncurrent:\n',current)
# # print('\nreshaped current:\n',current.reshape(1,-1))
# d,i = nbrs.kneighbors(current.reshape(1,-1))
# recs = i[0]
# # print('\nd: \n',d)
# # print('\ni: \n',i)

# full_recs = []
# for i in range(0,5):
#     x = recs[i]
#     # print('x: ',x)
#     # full_recs[i] = fonts.loc[fonts['idx'] == x]
#     full_recs.append(fonts.iloc[x])

# print('\nrecommendations:\n',full_recs)


# ************* Test K Value and Distance Metric *************
# k val must be > 5
font = 'Open Sans 400'
num_neighbors = 5

def test_k_val_distance(k,metric,font,fonts,vectors,num_neighbors):
    filename = 'recs_k' + str(k) + '_' + metric + '.csv'
    distance = ''
    print(metric)

    if k <= 5:
        print("K must be greater than 5")
    elif metric == 'c':
        distance = 'cosine'
    elif metric == 'e':
        distance = 'euclidean'
    else:
        print("Invalid metric")

    knn = NearestNeighbors(n_neighbors=k, metric=distance, algorithm='auto').fit(vectors)
    recs= get_font_combinations(font,fonts,vectors,knn,num_neighbors)

    # for i in range(0,len(recs)):
    #     webbrowser.open_new(recs[i]['url'])

    df = pd.DataFrame(recs)
    df.to_csv(filename, index=None, header=True)

    return df


# recsk6c = test_k_val_distance(6,'c',font,fonts,font_vectors,num_neighbors)
# webbrowser.open_new('www.google.com')
# recsk6e = test_k_val_distance(6,'e',font,fonts,font_vectors,num_neighbors) # like this one better

# recsk100c = test_k_val_distance(100,'c',font,fonts,font_vectors,num_neighbors)
# webbrowser.open_new('www.google.com')
# recsk100e = test_k_val_distance(100,'e',font,fonts,font_vectors,num_neighbors)

# recsk200c = test_k_val_distance(200,'c',font,fonts,font_vectors,num_neighbors)
# webbrowser.open_new('www.google.com')
# recsk200e = test_k_val_distance(200,'e',font,fonts,font_vectors,num_neighbors)

# knn_k4_c = NearestNeighbors(n_neighbors=4, metric='cosine', algorithm='auto').fit(font_vectors)
# recs_k4_c = get_font_combinations(font,fonts,font_vectors,knn_k4_c,num_neighbors)
# df_k4c = pd.DataFrame(knn_k4_c)
# df_k4c.to_csv(r'k4c.csv', index=None, header=True)


# knn_k4_e = NearestNeighbors(n_neighbors=4, metric='euclidean', algorithm='auto').fit(font_vectors)
# recs_k4_e = get_font_combinations(font,fonts,font_vectors,knn_k4_e,num_neighbors)
# df_k4e = pd.DataFrame(knn_k3_e)
# df_k4e.to_csv(r'k4e.csv', index=None, header=True)



# ************* Test Distance Metric *************