import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Dataviz:
    def __init__(self):
        self.folder = "datasets/"
        self.data_array = []
    
    def load_dataset(self, file_path):
        self.data_array.append(pd.read_csv(self.folder + file_path, low_memory=False))
        
    def plot_general_presentation(self):
        if self.data_array:
            df = self.data_array[0]
        else:
            return
        
        count = {}
        labels = []
        for category in df['traffic_category']:
            if category not in labels:
                labels.append(category)
                count.update({category: 1})  
            count[category] += 1

        sns.set_theme(style="whitegrid")
        sizes = [value for key, value in count.items()]

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel")[:3])
        plt.title('Hiraki2021 dataset, avec un total de 555 277 requêtes')
        plt.show()
    
    def plot_flow_duration(self):
        if self.data_array:
            df = self.data_array[0]
        else:
            return

        # Convertir la durée des flux en numérique, ignorer les erreurs
        df['flow_duration'] = pd.to_numeric(df['flow_duration'], errors='coerce')
        df = df.dropna(subset=['flow_duration', 'traffic_category', 'Label'])

        mean_flow_duration = df.groupby(['Label', 'traffic_category'])['flow_duration'].mean().unstack()
        sns.set_theme(style="whitegrid")
        palette = sns.color_palette("Set2", n_colors=len(mean_flow_duration.columns))
        
        mean_flow_duration.plot(kind='barh', stacked=False, color=palette, figsize=(10, 6))

        plt.xlabel('Durée Moyenne du Flow (ms)')
        plt.ylabel('Catégories')
        plt.title('Durée Moyenne des Flows par Catégorie et Label')
        
        plt.legend(title='Traffic Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
        
        
    def protocol_connection_indicators(self):
        if not self.data_array:
            print("No dataset loaded. Please load a dataset first.")
            return
        
        df = self.data_array[0]
        
        # Ensure columns exist
        required_columns = ['flow_SYN_flag_count', 'flow_ACK_flag_count', 'flow_FIN_flag_count', 'down_up_ratio', 'Label']
        for col in required_columns:
            if col not in df.columns:
                print(f"Column '{col}' is missing from the dataset.")
                return
        
        # Aggregate mean values for malicious and benign labels
        summary = df.groupby('Label')[['flow_SYN_flag_count', 'flow_ACK_flag_count', 'flow_FIN_flag_count', 'down_up_ratio']].mean()
        
        # Visualization
        fig, ax = plt.subplots(2, 1, figsize=(10, 10))
        
        # Bar plot for flag counts
        summary[['flow_SYN_flag_count', 'flow_ACK_flag_count', 'flow_FIN_flag_count']].plot.bar(ax=ax[0], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax[0].set_title('Mean Protocol Flags by Label')
        ax[0].set_ylabel('Mean Count')
        ax[0].legend(title="Flags")
        
        plt.tight_layout()
        plt.show()
        

    def temporal_and_activity_features(self):
        if not self.data_array:
            print("No dataset loaded. Please load a dataset first.")
            return

        # Load the dataframe
        df = self.data_array[0]

        # Ensure necessary columns are present
        required_columns = ['flow_iat.avg', 'flow_iat.std', 'active.avg', 'idle.avg', 'Label']
        for col in required_columns:
            if col not in df.columns:
                print(f"Column '{col}' is missing from the dataset.")
                return

        # Create new columns to explore attack behaviors (short IAT with high activity can indicate bursts)
        df['iat_mean_std_ratio'] = df['flow_iat.avg'] / df['flow_iat.std']  # Measure of IAT burstiness
        df['active_idle_ratio'] = df['active.avg'] / df['idle.avg']  # Ratio of active vs idle periods

        # Plot Flow IAT Mean vs Std (Visualizing attack bursts)
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='flow_iat.avg', y='flow_iat.std', hue='Label', palette='viridis', alpha=0.6)
        plt.title('Flow IAT Mean vs Std', fontsize=16)
        plt.xlabel('Flow IAT Mean (seconds)', fontsize=12)
        plt.ylabel('Flow IAT Std (seconds)', fontsize=12)
        plt.legend(title="Label", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    
if __name__ == "__main__":
    obj = Dataviz()
    obj.load_dataset("hiraki2021.csv")
    obj.load_dataset("cic-ids.csv")
    obj.plot_general_presentation()
    obj.plot_flow_duration()
    obj.protocol_connection_indicators()
    obj.temporal_and_activity_features()