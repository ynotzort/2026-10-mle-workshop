#!/usr/bin/env python
# coding: utf-8

from datetime import date
import argparse
from loguru import logger

import pandas as pd
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error


def read_dataframe(filename: str) -> pd.DataFrame:
    """loads and preprocesses the NYC Taxi dataset

    Args:
        filename (str): path or url to the dataset

    Returns:
        pd.DataFrame: processed dataframe
    """

    try:
        df = pd.read_parquet(filename)

        df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
        df.duration = df.duration.dt.total_seconds() / 60

        df = df[(df.duration >= 1) & (df.duration <= 60)]

        categorical = ['PULocationID', 'DOLocationID']
        df[categorical] = df[categorical].astype(str)
        
        return df
    except Exception as e:
        logger.error(f"ERROR: reading {filename} failed")
        logger.exception(e)
        raise

def train(train_date: date, val_date: date, out_path: str) -> None:
    """Train and validate a model on specified dates and save it.

    Args:
        train_date (date): training date
        val_date (date): validation date
        out_path (str): where to save it
    """

    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet"
    train_url = base_url.format(year=train_date.year, month=train_date.month)
    val_url = base_url.format(year=val_date.year, month=val_date.month)
    
    df_train = read_dataframe(train_url)
    df_val = read_dataframe(val_url)

    logger.info(f"df_train length is {len(df_train)}")
    logger.info(f"df_val length is {len(df_val)}")

    categorical = ['PULocationID', 'DOLocationID']
    numerical = ['trip_distance']

    train_dicts = df_train[categorical + numerical].to_dict(orient='records')
    val_dicts = df_val[categorical + numerical].to_dict(orient='records')

    target = 'duration'
    y_train = df_train[target].values
    y_val = df_val[target].values

    dv = DictVectorizer()
    lr = LinearRegression()
    pipeline = make_pipeline(dv, lr)

    pipeline.fit(train_dicts, y_train)
    y_pred = pipeline.predict(val_dicts)

    logger.info(f"MSE: {mean_squared_error(y_val, y_pred, squared=False)}")
    with open(out_path, 'wb') as f_out:
        pickle.dump(pipeline, f_out)
