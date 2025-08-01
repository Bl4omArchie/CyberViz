import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import squarify

"""
This code was made during a datavizualisation project at my school.
The subject was : from a dataset, plot graph and draw conclusion from it.
So I took the hikari 2021 dataset and make conclusion about attack and benign traffic.

To do so, I made tree graphics : 
- a treemap about the categories of traffic
- an inter arrival time benchmark
- a simple bar to visualize how are distributed flags between attack and benign traffic.

"""


class Dataviz:
    def __init__(self):
        self.folder = "data/"
        self.data_array = []
    
    def load_dataset(self, file_path):
        self.data_array.append(pd.read_csv(self.folder + file_path, on_bad_lines='skip'))


    # Treemap: visualizes the distribution of traffic categories based on their frequency in the dataset.
    #
    # Categories :
    #   - Benign : legitimate, user traffic
    #   - Background : automated traffic such as bots, system processes.
    #   - Probing : scan for open port or known vulnerabilities
    #   - Others : Brute-force, b-f XML, cryptominer etc.
    def plot_treemap(self):
        if not self.data_array:
            print("No dataset loaded. Please load a dataset first.")
            return

        df = self.data_array[0]

        if 'traffic_category' not in df.columns:
            print("'traffic_category' column not found in dataset.")
            return

        count = df['traffic_category'].value_counts()
        total = count.sum()
        percent = count / total

        major_mask = percent >= 0.04
        major_labels = count[major_mask]
        minor_labels = count[~major_mask]

        final_labels = []
        final_sizes = []

        for label, size in major_labels.items():
            pct = size / total
            final_labels.append(f"{label}\n{size} ({pct:.1%})")
            final_sizes.append(size)

        if not minor_labels.empty:
            grouped_name = ', '.join(minor_labels.index.tolist())
            grouped_label = f"Others\n({grouped_name})"
            grouped_size = minor_labels.sum()
            grouped_pct = grouped_size / total
            grouped_label += f"\n{grouped_size} ({grouped_pct:.1%})"

            final_labels.append(grouped_label)
            final_sizes.append(grouped_size)

        # Treemap
        colors = sns.color_palette("Set1", n_colors=len(final_labels))
        plt.figure(figsize=(16, 10))
        squarify.plot(
            sizes=final_sizes,
            label=final_labels,
            color=colors,
            alpha=0.85,
            text_kwargs={'fontsize': 10}
        )
        plt.title("Répartition des Catégories de Trafic", fontsize=16, weight='bold')
        plt.tight_layout()
        plt.show()


    # Hist : display the distribution of flags (ACK, SYN, FIN) for either is the traffic is considered as a threat or a legitimate one.
    def display_protocol_flags(self):
        if not self.data_array:
            print("No dataset loaded. Please load a dataset first.")
            return
        
        flag_columns = ['flow_FIN_flag_count', 'flow_SYN_flag_count', 'flow_ACK_flag_count']
        
        avg_protocol_data = self.data_array[0][flag_columns + ['Label']].groupby('Label').mean()
        
        avg_protocol_data.plot(kind='bar', figsize=(12, 8))
        plt.title('Quantité Moyenne de chaque Protocole par Label')
        plt.xlabel('Label')
        plt.ylabel('Quantité Moyenne')
        plt.xticks(rotation=45)
        plt.legend(title='Protocoles')
        plt.show()


    # Scatter plot:
    # Flow IAT (Inter-Arrival Time) refers to the time gaps between packets within a flow.
    #   - flow_iat.avg: the average inter-arrival time — how fast packets arrive, on average.
    #   - flow_iat.std: the standard deviation — how consistent or variable the timing is.
    #
    # Here we compares the average speed of packet arrivals (x-axis) to their regularity (y-axis) across flows.
    #
    # Observation: Malicious flows often have very low average IAT values, indicating fast, bursty traffic, a typical sign of attack behavior.
    def inter_arrival_time_benchmark(self):
        if not self.data_array:
            print("No dataset loaded. Please load a dataset first.")
            return

        df = self.data_array[0]

        required_columns = ['flow_iat.avg', 'flow_iat.std', 'active.avg', 'idle.avg', 'Label']
        for col in required_columns:
            if col not in df.columns:
                print(f"Column '{col}' is missing from the dataset.")
                return

        df['iat_mean_std_ratio'] = df['flow_iat.avg'] / df['flow_iat.std']
        df['active_idle_ratio'] = df['active.avg'] / df['idle.avg']

        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='flow_iat.avg', y='flow_iat.std', hue='Label', palette={0: 'green', 1: 'red'}, alpha=0.6)
        plt.title('Flow IAT Mean vs Std', fontsize=16)
        plt.xlabel('Flow IAT Mean (seconds)', fontsize=12)
        plt.ylabel('Flow IAT Std (seconds)', fontsize=12)
        plt.legend(title="Label", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    obj = Dataviz()
    obj.load_dataset("hikari.csv")
    obj.plot_treemap()
    obj.display_protocol_flags()
    obj.inter_arrival_time_benchmark()
