import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Visualize:
    def __init__(self, log_path):
        self.log_df = pd.read_csv(log_path)
        self.log_df['datetime'] = pd.to_datetime(self.log_df['datetime'], errors='coerce') 
        self.log_df['hour'] = self.log_df['datetime'].dt.hour
    
    def plot_errors_over_time(self):
        """
        Vẽ biểu đồ đường thể hiện số lượng lỗi và request hợp lệ qua thời gian.
        """
        self.log_df['request_type'] = self.log_df['status'].apply(lambda x: 'Lỗi' if x != 200 else 'Hợp lệ')
        hourly_counts = self.log_df.groupby(['hour', 'request_type']).size().unstack(fill_value=0)
        
        print("so luong loi va request hop le qua thoi gian")
        print(hourly_counts)

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=hourly_counts, markers=True, dashes=False)
        plt.title("Số lượng lỗi và Request hợp lệ qua thời gian")
        plt.xlabel("Giờ")
        plt.ylabel("Số Lượng")
        plt.xticks(range(24))
        plt.legend(title="Loại Request", labels=['Lỗi', 'Hợp lệ'])
        plt.grid(True)
        plt.show()

    def plot_request_distribution(self):
        """
        Vẽ biểu đồ tròn thể hiện phân bố các loại request (GET, POST, PUT, DELETE,...).
        """
        request_counts = self.log_df['method'].value_counts()
        plt.figure(figsize=(8, 8))
        request_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        plt.title("Phân bố các loại Request")
        plt.ylabel("")
        plt.show()

    def plot_bytes_sent_per_hour(self):
        """
        Vẽ biểu đồ đường thể hiện tổng lượng dữ liệu gửi đi mỗi giờ.
        """
        hourly_bytes_sent = self.log_df.groupby('hour')['bytes_sent'].sum()
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=hourly_bytes_sent.index, y=hourly_bytes_sent.values, palette="viridis")
        plt.title('Bytes gửi mỗi giờ')
        plt.xlabel('Giờ')
        plt.ylabel('Tổng số bytes gửi')
        plt.xticks(rotation=0)
        # Automatically adjust subplot parameters to give specified padding
        plt.tight_layout()
        plt.show()


    def plot_combined_chart(self):
        '''
        Vẽ biểu đồ kết hợp: bytes gửi mỗi giờ và số lỗi qua thời gian.
        '''

        # Data aggregation
        hourly_bytes_sent = self.log_df.groupby('hour')['bytes_sent'].sum()
        self.log_df['is_error'] = self.log_df['status'].apply(lambda x: 1 if x != 200 else 0)
        hourly_errors = self.log_df.groupby('hour')['is_error'].sum()

        # Plotting
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot bytes sent
        ax1.bar(hourly_bytes_sent.index, hourly_bytes_sent.values, color='skyblue', alpha=0.7, label='Bytes Sent')
        ax1.set_xlabel('Hour')
        ax1.set_ylabel('Bytes Sent', color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')

        # Plot errors on the secondary axis
        ax2 = ax1.twinx()
        ax2.plot(hourly_errors.index, hourly_errors.values, color='red', marker='o', label='Errors')
        ax2.set_ylabel('Errors', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Titles and legends
        fig.suptitle('Bytes Sent per Hour and Errors Over Time', fontsize=14)
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        plt.grid(True)
        plt.tight_layout()

        plt.show()
    

    def plot_status_distribution(self):
            """
            Vẽ biểu đồ thanh thể hiện tần suất của mỗi status.
            """
            status_counts = self.log_df['status'].value_counts()
            plt.figure(figsize=(10, 6))
            sns.barplot(x=status_counts.index, y=status_counts.values, palette="viridis")
            plt.title('Tần suất của mỗi Status')
            plt.xlabel('Status')
            plt.ylabel('Tần suất')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()





if __name__ == "__main__":
     path = r'/Users/phamthiphuongthuy/Desktop/Intern/server_log/data/parsed_logs.csv'
     visualizer = Visualize(path)
     visualizer.plot_errors_over_time()
     visualizer.plot_request_distribution()
     visualizer.plot_bytes_sent_per_hour()
     visualizer.plot_combined_chart()
     visualizer.plot_status_distribution() 