

from sklearn.linear_model import LinearRegression


def train_linear_model(df):
    features = ["horsepower", "engine-size", "curb-weight", "city-L/100km", "fuel-type-gas", "fuel-type-diesel"]
    X = df[features]
    y = df["price"]
    model = LinearRegression()
    model.fit(X, y)
    return model, features