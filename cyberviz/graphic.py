from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple, List

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import squarify


@dataclass
class Graphic:
    title: str
    legend: str
    inputs: List[float] = None
    labels: List[str] = None
    fig_size: Optional[Tuple[int, int]] = (18, 12)
    grid: Optional[bool] = False
    save: Optional[bool] = False

    @staticmethod
    def new_plot(title: str,legend: str, inputs, labels: List[str], fig_size: Optional[Tuple[int, int]] = (18, 12), grid: Optional[bool] = False, save: Optional[bool] = False):
        return Graphic(title=title, legend=legend, inputs=inputs, labels=labels, fig_size=fig_size, grid=grid, save=save)


class BaseGraphic(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def plot_graph(input: str):
        pass

class TreemapGraphic:
    def __init__(self):
        super().__init__()
        self.family = "chart"
        self.functions = ["comparison", "distribution"]
        self.shape = "square"


    def plot_graph(self, graph: Graphic):
        sizes = graph.inputs
        colors = sns.color_palette("pastel", len(sizes))

        fig, ax = plt.subplots(figsize=graph.fig_size)

        ax.pie(
            sizes,
            labels=graph.labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1}
        )

        ax.axis('equal')
        ax.set_title(graph.title, loc='left')

        if graph.legend is not None:
            ax.legend(title=graph.legend, bbox_to_anchor=(1.05, 1), loc='upper left')

        if graph.grid:
            ax.grid()

        if graph.save:
            fig.savefig(f"{graph.title.replace(' ', '_')}.png", bbox_inches="tight")
        else:
            st.pyplot(fig)

"""
class HistGraphic:
    def __init__(self):
        super().__init__()
        self.family = "chart"
        self.functions = ["distribution"]
        self.shape = "bar"

    def plot_graph(self, graph: Graphic):
        plt.figure(graph.fig_size)

        sns.histplot(data=graph.input, x=graph.x_header[0], y=graph.y_header[0], hue='Label', palette={graph.x_header[0]: graph.x_header[1], graph.y_header[0]: graph.y_header[1]}, alpha=0.6)

        plt.title(graph.title ,fontsize=16)
        plt.xlabel(graph.x_label, fontsize=12)
        plt.ylabel(graph.y_label, fontsize=12)
        plt.legend(title=graph.legend, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

        if graph.path:
            plt.savefig()
"""