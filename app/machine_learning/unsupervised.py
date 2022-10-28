import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import accuracy_score


def preprocess_data(data: pd.DataFrame, target: str, drop_cols: list[str]):
    data.drop(drop_cols, axis=1, inplace=True)
    data.dropna(inplace=True)
    X = data.drop(target, axis=1)
    scaling = StandardScaler()
    scaling.fit(X)
    scaled_data = scaling.transform(X)
    y = data.loc[:, target]
    return scaled_data, y, data


def hierarchical_clustering(df: pd.DataFrame, target: str, drop_cols: list[str], n_clusters: int):
    X, y, original_data = preprocess_data(df, target, drop_cols)
    model = AgglomerativeClustering(n_clusters=n_clusters, affinity="euclidean", linkage="ward")
    model.fit(X)
    score = accuracy_score(y, model.labels_)
    model_info = dict({
        "Algorithm": "Hierarchical Clustering",
        "Rows (Original data)": df.shape[0],
        "Columns (Original data)": df.shape[1],
        "Rows (Processed data)": original_data.shape[0],
        "Columns (Processed data)": original_data.shape[1],
        "Rows dropped (due to NaN values)": df.shape[0] - original_data.shape[0],
        "Column names": ["{}".format(col) for col in df.columns],
        "Clusters": n_clusters,
        "Target": target,
        "Model accuracy": "{accuracy:.4f} %".format(accuracy=score * 100)
    })
    return model, model_info, [X, y], None


def pca(df: pd.DataFrame, target: str, drop_cols: list[str], n_components: int):
    X, y, original_data = preprocess_data(df, target, drop_cols)
    model = PCA(n_components=n_components)
    model.fit(X)
    X = model.transform(X)
    model_info = dict({
        "Algorithm": "PCA",
        "Rows (Original data)": df.shape[0],
        "Columns (Original data)": df.shape[1],
        "Rows (Processed data)": original_data.shape[0],
        "Columns (Processed data)": original_data.shape[1],
        "Rows dropped (due to NaN values)": df.shape[0] - original_data.shape[0],
        "Column names": ["{}".format(col) for col in df.columns],
        "Components": n_components,
        "Target": target,
    })
    return model, model_info, [X, y], None
