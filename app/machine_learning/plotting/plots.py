import numpy as np
from matplotlib.axes import Axes

from scipy.cluster.hierarchy import dendrogram, linkage


class PlotModel:
    def __init__(self, axis: Axes, title: str, x_label: str, y_label: str):
        self.axis = axis
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def set_parameters(self):
        self.axis.set_title(self.title)
        self.axis.set_xlabel(self.x_label)
        self.axis.set_ylabel(self.y_label)


def linear_regression_plot(plot_model: PlotModel, scatter_x: np.ndarray, scatter_y: np.ndarray, line_x: np.ndarray,
                           line_y: np.ndarray):
    plot_model.set_parameters()
    plot_model.axis.scatter(scatter_x, scatter_y, s=5)
    plot_model.axis.plot(line_x, line_y, c='orange')


def hierarchical_clustering_plot(plot_model: PlotModel, x: np.ndarray):
    z = linkage(x, "ward")
    dendrogram(
        z, p=12, leaf_rotation=45, leaf_font_size=12, show_contracted=True, truncate_mode="lastp", ax=plot_model.axis
    )
    plot_model.set_parameters()


def pca_plot(plot_model: PlotModel, x: np.ndarray, y: np.ndarray):
    plot_model.set_parameters()
    plot_model.axis.scatter(x[:, 0], x[:, 1], c=y, cmap='plasma' )
