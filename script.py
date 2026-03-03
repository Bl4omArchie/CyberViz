import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import pandas as pd
import squarify

class Dataviz:
    def __init__(self):
        self.folder = "data/"
        self.data_array = []
    
    def load_dataset(self, file_path):
        self.data_array.append(pd.read_csv(self.folder + file_path, on_bad_lines='skip'))


    def display_protocol_flags(self):
        # List of flag columns (update these based on your dataset's columns)
        flag_columns = [
            'flow_FIN_flag_count', 'flow_SYN_flag_count', 'flow_ACK_flag_count', 
        ]
        
        avg_protocol_data = self.data_array[0][flag_columns + ['Label']].groupby('Label').mean()
        
        # Tracer le graphique avec seaborn
        avg_protocol_data.plot(kind='bar', figsize=(12, 8))
        plt.title('Quantité Moyenne de chaque Protocole par Label')
        plt.xlabel('Label')
        plt.ylabel('Quantité Moyenne')
        plt.xticks(rotation=45)
        plt.legend(title='Protocoles')
        plt.show()


    def plot_general_treemap(self):
        if not self.data_array:
            print("No dataset loaded. Please load a dataset first.")
            return
        
        df = self.data_array[0]
        
        if 'traffic_category' not in df.columns:
            print("'traffic_category' column not found in dataset.")
            return
        
        count = df['traffic_category'].value_counts()
        labels = count.index
        sizes = count.values
        
        total = sum(sizes)
        labels_with_pct = [f"{label}\n{size} ({size / total:.1%})" for label, size in zip(labels, sizes)]
        
        colors = sns.color_palette("Set1", n_colors=len(labels))
        
        # Tracer le treemap
        plt.figure(figsize=(16, 10))
        squarify.plot(sizes=sizes, label=labels_with_pct, color=colors, alpha=0.85, text_kwargs={'fontsize': 10})
        plt.title("Répartition des Catégories de Trafic", fontsize=16, weight='bold')
        plt.tight_layout()
        plt.show()


    def temporal_and_activity_features(self):
        if not self.data_array:
            print("No dataset loaded. Please load a dataset first.")
            return

        df = self.data_array[0]

        required_columns = ['flow_iat.avg', 'flow_iat.std', 'active.avg', 'idle.avg', 'Label']
        for col in required_columns:
            if col not in df.columns:
                print(f"Column '{col}' is missing from the dataset.")
                return

        # Create new columns to explore attack behaviors (short IAT with high activity can indicate bursts)
        df['iat_mean_std_ratio'] = df['flow_iat.avg'] / df['flow_iat.std']
        df['active_idle_ratio'] = df['active.avg'] / df['idle.avg']

        # Plot Flow IAT Mean vs Std (Visualizing attack bursts)
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='flow_iat.avg', y='flow_iat.std', hue='Label', palette={0: 'green', 1: 'red'}, alpha=0.6)
        plt.title('Flow IAT Mean vs Std', fontsize=16)
        plt.xlabel('Flow IAT Mean (seconds)', fontsize=12)
        plt.ylabel('Flow IAT Std (seconds)', fontsize=12)
        plt.legend(title="Label", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

        # Plot Active/Idle Ratio
        plt.figure(figsize=(20, 14))
        sns.boxplot(x='Label', y='active_idle_ratio', data=df, palette={0: 'green', 1: 'red'})
        plt.title('Active vs Idle Periods (Ratio)', fontsize=16)
        plt.xlabel('Traffic Label', fontsize=12)
        plt.ylabel('Active/Idle Ratio', fontsize=12)
        plt.tight_layout()
        plt.show()

        # Additional analysis on bursty vs steady traffic
        df['short_flow'] = df['flow_duration'] < 10  # Define short flows for bursty analysis
        short_bursty_traffic = df[df['short_flow'] & (df['iat_mean_std_ratio'] > 1.5)]  # High burstiness in short flows

        print("Detected Short and Bursty Traffic (Potential Attacks):")
        print(short_bursty_traffic[['uid', 'flow_iat.avg', 'flow_iat.std', 'active.avg', 'idle.avg', 'Label']])


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
    
    obj.plot_general_treemap()
    #obj.temporal_and_activity_features()
    obj.inter_arrival_time_benchmark()
    obj.display_protocol_flags()

