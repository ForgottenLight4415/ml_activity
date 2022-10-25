import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split

def preprocess_data(data: pd.DataFrame, target: str):
    data.dropna(inplace=True)
    X = data.drop(target, axis=1)
    y = data.loc[:, target]
    return train_test_split(X, y, train_size=0.8, random_state=20), data


def linear_regression(dataFile, target):
    df = pd.read_csv(dataFile)
    split_data, original_data = preprocess_data(df, target)
    X_train, X_test, y_train, y_test = split_data
    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    model_info = dict({
        "Algorithm" : "Linear Regression",
        "Rows (Original data)" : df.shape[0],
        "Columns (Original data)" : df.shape[1],
        "Rows (Processed data)" : original_data.shape[0],
        "Columns (Processed data)" : original_data.shape[1],
        "Rows dropped (due to NaN values)" : df.shape[0] - original_data.shape[0],
        "Column names" : ["{}".format(col) for col in df.columns],
        "Target" : target,
        "Model accuracy" : "{accuracy:.4f} %".format(accuracy=score * 100)
    })
    return model, model_info