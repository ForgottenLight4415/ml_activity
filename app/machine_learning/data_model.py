import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from app.machine_learning.plotting.plots import *

import app.machine_learning.supervised as sp
import app.machine_learning.unsupervised as usp
from sklearn.cluster import KMeans

from enum import Enum


class Algorithm(Enum):
    SUPERVISED = 1
    UNSUPERVISED = 2


class DataModel:
    original_df: pd.DataFrame = None
    split_dataset: tuple[np.ndarray] = None
    column_names: tuple[str] = None

    algorithm: Algorithm = None
    algorithm_name: str = None
    target: str = None

    model = None
    model_info = None
    predictions = None
    score = None

    def __init__(self, data_frame: pd.DataFrame, learning_method: str, algorithm: str):
        self.original_df = data_frame
        self.algorithm = Algorithm.SUPERVISED if learning_method == "supervised" else Algorithm.UNSUPERVISED
        self.algorithm_name = algorithm
        self.column_names = tuple(["{}".format(col) for col in self.original_df.columns])

    def train_model(self, target: str | None, drop_cols, **kwargs):
        if target:
            self.target = target
        else:
            raise ValueError("Target not defined")
        if self.algorithm == Algorithm.SUPERVISED:
            match self.algorithm_name:
                case "linear_regression":
                    self.model, self.model_info, self.split_dataset, self.predictions = sp.linear_regression(
                        self.original_df, self.target, drop_cols
                    )
        elif self.algorithm == Algorithm.UNSUPERVISED:
            match self.algorithm_name:
                case "hierarchical_clustering":
                    self.model, self.model_info, self.split_dataset, self.predictions = usp.hierarchical_clustering(
                        self.original_df, self.target, drop_cols, kwargs['n_clusters']
                    )
                case "pca":
                    self.model, self.model_info, self.split_dataset, self.predictions = usp.pca(
                        self.original_df, self.target, drop_cols, kwargs['n_components']
                    )
                case "kmeans":
                    self.model, self.model_info, self.split_dataset, self.predictions = usp.kmeans(
                        self.original_df, self.target, drop_cols
                    )

    def make_predictions(self, data):
        if self.model is not None:
            return self.model.predict(data)

    def make_image(self):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        if self.algorithm == Algorithm.SUPERVISED:
            match self.algorithm_name:
                case "linear_regression":
                    plot_model = PlotModel(axis, "Linear Regression", self.column_names[0], self.column_names[1])
                    linear_regression_plot(
                        plot_model,
                        self.split_dataset[0],
                        self.split_dataset[2],
                        self.split_dataset[1],
                        self.predictions
                    )
        elif self.algorithm == Algorithm.UNSUPERVISED:
            if self.algorithm_name == "hierarchical_clustering":
                plot_model = PlotModel(
                    axis, "Truncated Hierarchical Clustering Dendrogram", "Cluster size", "Distance"
                )
                hierarchical_clustering_plot(plot_model, self.split_dataset[0])
            elif self.algorithm_name == "pca":
                plot_model = PlotModel(
                    axis,
                    "Principal Component Analysis Dimensionality Reduction",
                    "Component 1",
                    "Component 2"
                )
                pca_plot(
                    plot_model, self.split_dataset[0], self.split_dataset[1], self.split_dataset[2], self.original_df
                )
            elif self.algorithm_name == "kmeans":
                plot_model = PlotModel(
                    axis,
                    "The Elbow Method",
                    "Number of clusters",
                    "WCSS"
                )
                kmeans_plot(
                    plot_model, range(1, 11), self.split_dataset[2]
                )
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

    def evaluate_image(self, clusters):
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        model = KMeans(n_clusters=clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
        data = model.fit_predict(self.split_dataset[0])
        for i in range(clusters):
            axis.scatter(self.split_dataset[0][data == i, 0], self.split_dataset[0][data == i, 1], label="Cluster {}".format(i))

        axis.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], s=300, c='yellow', label='Centroids')
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")