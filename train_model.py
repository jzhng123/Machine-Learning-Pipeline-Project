<<<<<<< HEAD
import os
from flask import Flask, request, render_template, g, redirect, Response, session, abort, flash
import pandas as pd
import io
import requests
import pandasql as ps
from joblib import dump, load
import numpy as np
=======
import numpy as np
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load

import warnings
warnings.filterwarnings('ignore')


def train_model(csv):

    df= pd.read_csv(csv)
    df.drop('Unnamed: 0',axis=1)
    df['pop_level'] = df[' shares']
    df['pop_level'].loc[df[' shares'].between(0, 1000)] = 0
    df['pop_level'].loc[df[' shares'].between(1001, 2000)] = 1
    df['pop_level'].loc[df[' shares'].between(2000, 3000, inclusive=False)] = 2
    df['pop_level'].loc[df[' shares'].between(3000, 4000)] = 3
    df['pop_level'].loc[df[' shares'].between(4000, 5000, inclusive=False)] = 4
    df['pop_level'].loc[df[' shares'] >= 5000] = 5

    df.drop(' shares', axis=1)
    X_train = df.loc[:, df.columns != 'pop_level']
    y_train = df['pop_level']

    X_train.dtypes == "object"
    categorical = X_train.dtypes == "object"
    numerical = X_train.dtypes != "object"

    preprocess = make_column_transformer(
        (StandardScaler(), numerical),
        (OneHotEncoder(handle_unknown='ignore',
                       sparse=False), categorical))

    model_rf = make_pipeline(preprocess, RandomForestClassifier(random_state=42, n_estimators=20))

    param_grid_rf = {"randomforestclassifier__max_features": np.asarray(['sqrt', 'log2']),
                     'randomforestclassifier__n_estimators': [200, 500],
                     'randomforestclassifier__max_depth': [3, 6]}

    grid_model_rf = GridSearchCV(model_rf, param_grid=param_grid_rf, cv=5, n_jobs=-1,
                                 scoring=['accuracy', 'f1_macro', 'f1_micro', 'f1_weighted'],
                                 refit='accuracy')
    grid_model_rf.fit(X_train, y_train)

    max_depth=grid_model_rf.best_params_['randomforestclassifier__max_depth']
    max_features=grid_model_rf.best_params_['randomforestclassifier__max_features']
    n_estimators=grid_model_rf.best_params_['randomforestclassifier__n_estimators']

    model_rf_2 = make_pipeline(preprocess, RandomForestClassifier(max_depth=max_depth,
                                                                  max_features=max_features,
                                                                  n_estimators=n_estimators,
                                                                  random_state=42))

    model_rf_2.fit(X_train, y_train)

    dump(model_rf_2, 'ModelRF.joblib')


csv='train.csv'

train_model(csv)


>>>>>>> 5fb9dce8fb3b1030001cdfdeff25cdc8468fb860

