import pandas as pd
import numpy as np
import os
import warnings
from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise.model_selection import cross_validate, train_test_split
from collections import defaultdict
from surprise import accuracy
from surprise.model_selection import GridSearchCV
from scipy.sparse import csr_matrix
from surprise.accuracy import rmse

warnings.filterwarnings("ignore")
os.chdir('E:\\newMovies')


def get_top_n_movies(num_user, pred, n, df_100):
    '''
    Функция, которая выводит топ фильмов, которые можно рекомендовать пользователю
    num_user - номер пользователя, для которого нужно получить рекомендации, type int
    pred - Список с предсказаниями оценок, которые были получены в результате работы функции test(), type list
    n - число фильмов, которое необходимо порекомендовать, type int
    Возвращает таблицу, в которой содержится информация о пользователе, фильме и оценка, которая была предсказана моделью
    '''
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in pred:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    info = []
    for i in range(n):
        info.append([num_user,
                     top_n[num_user][i][0],
                     df_100[df_100['movieId'] == top_n[num_user][i][0]]['title'].values[0],
                     top_n[num_user][i][1]])
    recommendation = pd.DataFrame(info, columns=['userId', 'movieId', 'title', 'rating'])
    return recommendation


df_100 = pd.read_csv('df_100.csv')
# opros2 = pd.read_csv('opros2.csv')
# main_data = pd.read_csv('main_data.csv')
# main_data['userId'] = pd.to_numeric(main_data['userId'], downcast='integer', errors='coerce')
# main_data['movieId'] = pd.to_numeric(main_data['movieId'], downcast='integer', errors='coerce')
# df_100['userId'] = pd.to_numeric(df_100['userId'], downcast='integer', errors='coerce')
# df_100['movieId'] = pd.to_numeric(df_100['movieId'], downcast='integer', errors='coerce')
# df_100.dropna(inplace=True)
# opros2.dropna(inplace=True)

#рек.система main_data
# reader = Reader(rating_scale=(1, 5))
# data = Dataset.load_from_df(main_data[['userId', 'movieId', 'rating']], reader)
# trainset = data.build_full_trainset()
# testset = trainset.build_anti_testset()
algo = SVD(n_factors=400, n_epochs=70, lr_all=0.01, reg_all=0.15, verbose=False)
# predictions = algo.fit(trainset).test(testset)
# print('success')
# #рек.система opros2
opros3 = pd.read_csv('opros3.csv')
reader2 = Reader(rating_scale=(1, 5))
data2 = Dataset.load_from_df(opros3[['userId', 'movieId', 'rating']], reader2)
trainset_1 = data2.build_full_trainset()
testset_1 = trainset_1.build_anti_testset()
pred2 = algo.fit(trainset_1).test(testset_1)








