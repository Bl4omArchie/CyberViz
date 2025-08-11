from typing import Optional, Tuple, List
from abc import ABC, abstractmethod


import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import squarify


class BaseGraphic(ABC):
    def __init__(self, title: str,legend: str, inputs, labels: List[str],
                 fig_size: Optional[Tuple[int, int]] = (18, 12),
                 grid: Optional[bool] = False, save: Optional[bool] = False):

        self.title = title
        self.legend = legend
        self.inputs = inputs
        self.labels = labels
        self.fig_size = fig_size
        self.grid = grid
        self.save = save

    @abstractmethod
    def plot_graph(self):
        pass


class TreemapGraphic(BaseGraphic):
    def plot_graph(self):
        sizes = self.inputs
        labels = self.labels
        colors = sns.color_palette("pastel", len(sizes))

        fig, ax = plt.subplots(figsize=self.fig_size)

        squarify.plot(
            sizes=sizes,
            label=labels,
            color=colors,
            alpha=0.8,
            ax=ax,
            pad=True
        )

        ax.axis('off')
        ax.set_title(self.title, loc='left')

        if self.legend is not None:
            ax.legend(title=self.legend, bbox_to_anchor=(1.05, 1), loc='upper left')

        if self.grid:
            ax.grid()

        if self.save:
            fig.savefig(f"{self.title.replace(' ', '_')}.png", bbox_inches="tight")
        else:
            st.pyplot(fig)


class PieChartGraphic(BaseGraphic):
    def plot_graph(self):
        sizes = self.inputs
        colors = sns.color_palette("pastel", len(sizes))

        fig, ax = plt.subplots(figsize=self.fig_size)

        ax.pie(
            sizes,
            labels=self.labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1}
        )

        ax.axis('equal')
        ax.set_title(self.title, loc='left')

        if self.legend:
            ax.legend(title=self.legend, bbox_to_anchor=(1.05, 1), loc='upper left')

        if self.grid:
            ax.grid()

        if self.save:
            fig.savefig(f"{self.title.replace(' ', '_')}.png", bbox_inches="tight")
        else:
            st.pyplot(fig)


class HistogramGraphic(BaseGraphic):
    def plot_graph(self):
        fig, ax = plt.subplots(figsize=self.fig_size)
        sns.histplot(self.inputs, bins=20, ax=ax, kde=False, color='skyblue')

        ax.set_title(self.title)
        ax.set_xlabel(self.legend)

        if self.grid:
            ax.grid()

        if self.save:
            fig.savefig(f"{self.title.replace(' ', '_')}.png", bbox_inches="tight")
        else:
            st.pyplot(fig)


CHART_CLASSES = {
    "Treemap": TreemapGraphic,
    "Pie Chart": PieChartGraphic,
    "Histogram": HistogramGraphic
}

def new_graph(graph_type, title: str,legend: str, inputs, labels: List[str],
                fig_size: Optional[Tuple[int, int]] = (18, 12),
                grid: Optional[bool] = False, save: Optional[bool] = False):
    
    obj = CHART_CLASSES.get(graph_type)
    if obj:
        return obj(title=title, legend=legend, inputs=inputs, labels=labels, fig_size=fig_size, grid=grid, save=save)
    else:
        raise ValueError(f"Graph type {graph_type} is not supported")
