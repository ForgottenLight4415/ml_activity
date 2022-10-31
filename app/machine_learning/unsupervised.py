import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans


def preprocess_data(data: pd.DataFrame, target: str, drop_cols: list[str]):
    original_data = data
    data.drop(drop_cols, axis=1, inplace=True)
    data.dropna(inplace=True)
    X = data.drop(target, axis=1)
    scaling = StandardScaler()
    scaling.fit(X)
    scaled_data = scaling.transform(X)
    y = data.loc[:, target]
    return scaled_data, y, original_data, data


def hierarchical_clustering(df: pd.DataFrame, target: str, drop_cols: list[str], n_clusters: int):
    X, y, original_data, clean_data = preprocess_data(df, target, drop_cols)
    model = AgglomerativeClustering(n_clusters=n_clusters, affinity="euclidean", linkage="ward")
    model.fit(X)
    score = accuracy_score(y, model.labels_)
    model_info = dict({
        "Algorithm": "Hierarchical Clustering",
        "Rows (Original data)": df.shape[0],
        "Columns (Original data)": df.shape[1],
        "Rows (Processed data)": original_data.shape[0],
        "Columns (Processed data)": original_data.shape[1],
        "Rows dropped (due to NaN values)": df.shape[0] - clean_data.shape[0],
        "Column names": ["{}".format(col) for col in df.columns],
        "Clusters": n_clusters,
        "Target": target,
        "Model accuracy": "{accuracy:.4f} %".format(accuracy=score * 100)
    })
    return model, model_info, [X, y], None


def pca(df: pd.DataFrame, target: str, drop_cols: list[str], n_components: int):
    X, y, original_data, clean_data = preprocess_data(df, target, drop_cols)
    model = PCA(n_components=n_components)
    model.fit(clean_data)
    transformed_data = model.transform(clean_data)
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
    return model, model_info, [model.components_[0], model.components_[1], transformed_data], None


def kmeans(data, target, drop_cols):
    X, y, original_data, clean_data = preprocess_data(data, target, drop_cols)
    wcss = []
    model = None
    for i in range(1, 11):
        model = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        predictions = model.fit_predict(X)
        wcss.append(model.inertia_)
    model_info = dict({
        "Algorithm": "K-Means",
        "Rows (Original data)": data.shape[0],
        "Columns (Original data)": data.shape[1],
        "Rows (Processed data)": original_data.shape[0],
        "Columns (Processed data)": original_data.shape[1],
        "Rows dropped (due to NaN values)": data.shape[0] - original_data.shape[0],
        "Column names": ["{}".format(col) for col in data.columns],
        "Target": target,
        "Clusters": "Use elbow method to determine number of clusters and experiment for yourself."
    })
    return model, model_info, [X, y, wcss], predictions
