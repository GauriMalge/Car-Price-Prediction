import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


# ... Keep your other functions (load_data, clean_and_prepare_data, process_features, train_linear_model) exactly the same ...

def load_data(path):
    df = pd.read_csv(path, header=None)
    return df

def clean_and_prepare_data(df):
    df.columns = [
        "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
        "num-of-doors", "body-style", "drive-wheels", "engine-location",
        "wheel-base", "length", "width", "height", "curb-weight",
        "engine-type", "num-of-cylinders", "engine-size", "fuel-system",
        "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm",
        "city-mpg", "highway-mpg", "price"
    ]
    df.replace("?", np.nan, inplace=True)
    df["normalized-losses"] = df["normalized-losses"].astype("float")
    df["bore"] = df["bore"].astype("float")
    df["price"] = df["price"].astype("float")
    df["stroke"] = df["stroke"].astype("float")
    df["horsepower"] = df["horsepower"].astype("float")
    df["peak-rpm"] = df["peak-rpm"].astype("float")

    df["normalized-losses"] = df["normalized-losses"].replace(np.nan, df["normalized-losses"].mean())
    df["num-of-doors"] = df["num-of-doors"].replace(np.nan, "four")
    df["bore"] = df["bore"].replace(np.nan, np.mean(df["bore"]))

    for feature in ["price", "peak-rpm", "stroke", "horsepower"]:
        avg = df[feature].mean()
        df[feature] = df[feature].replace(np.nan, avg)

    df = df.rename(columns={"num-of-doors": "doors"})
    return df

def process_features(df):
    bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
    group_names = ["Low", "Medium", "High"]
    df["binned_horsepower"] = pd.cut(df["horsepower"], bins, labels=group_names, include_lowest=True)

    dummy_variables = pd.get_dummies(df["fuel-type"]).astype("int")
    dummy_variables.rename(columns={"gas": "fuel-type-gas", "diesel": "fuel-type-diesel"}, inplace=True)
    df = pd.concat([df, dummy_variables], axis=1)
    df["city-L/100km"] = 235 / df["city-mpg"]
    return df




