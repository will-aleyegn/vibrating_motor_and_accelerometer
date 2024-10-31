import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import datetime

def plot_sensor_data(filename):
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate time in seconds from start
    df['seconds'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
    
    # Set up the figure with GridSpec
    plt.figure(figsize=(15, 10))
    gs = GridSpec(3, 2)
    
    # Plot accelerometer data
    ax1 = plt.subplot(gs[0, :])
    ax1.plot(df['seconds'], df['acc_x'], label='X', color='#FF9999')
    ax1.plot(df['seconds'], df['acc_y'], label='Y', color='#66B2FF')
    ax1.plot(df['seconds'], df['acc_z'], label='Z', color='#99FF99')
    ax1.set_title('Accelerometer Readings', pad=10)
    ax1.set_ylabel('Acceleration (g)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot gyroscope data
    ax2 = plt.subplot(gs[1, :])
    ax2.plot(df['seconds'], df['gyro_x'], label='X', color='#FF9999')
    ax2.plot(df['seconds'], df['gyro_y'], label='Y', color='#66B2FF')
    ax2.plot(df['seconds'], df['gyro_z'], label='Z', color='#99FF99')
    ax2.set_title('Gyroscope Readings', pad=10)
    ax2.set_ylabel('Angular Velocity (°/s)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot temperature data
    ax3 = plt.subplot(gs[2, 0])
    ax3.plot(df['seconds'], df['temp'], color='#FF6B6B')
    ax3.set_title('Temperature', pad=10)
    ax3.set_xlabel('Time (seconds)')
    ax3.set_ylabel('Temperature (°C)')
    ax3.grid(True, alpha=0.3)
    
    # Create correlation matrix
    ax4 = plt.subplot(gs[2, 1])
    motion_data = df[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']].corr()
    
    # Create heatmap manually
    im = ax4.imshow(motion_data, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    
    # Add correlation values as text
    for i in range(len(motion_data.index)):
        for j in range(len(motion_data.columns)):
            text = ax4.text(j, i, f'{motion_data.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black")
    
    # Set labels
    ax4.set_xticks(np.arange(len(motion_data.columns)))
    ax4.set_yticks(np.arange(len(motion_data.index)))
    ax4.set_xticklabels(motion_data.columns, rotation=45, ha='right')
    ax4.set_yticklabels(motion_data.index)
    ax4.set_title('Sensor Correlation Matrix', pad=10)
    plt.colorbar(im, ax=ax4)
    
    # Adjust layout and save
    plt.tight_layout()
    
    # Save plot with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'mpu6050_analysis_{timestamp}.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved as {output_filename}")
    
    # Show plot
    plt.show()

def generate_basic_statistics(filename):
    """Generate basic statistics from the sensor data"""
    df = pd.read_csv(filename)
    
    # Calculate statistics for accelerometer and gyroscope data
    sensor_stats = df[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temp']].describe()
    
    # Calculate peak-to-peak values
    sensor_stats.loc['peak_to_peak'] = df[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temp']].max() - \
                                      df[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temp']].min()
    
    print("\nSensor Statistics:")
    print(sensor_stats)
    
    # Save statistics to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stats_filename = f'mpu6050_statistics_{timestamp}.csv'
    sensor_stats.to_csv(stats_filename)
    print(f"\nStatistics saved to {stats_filename}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python plot_mpu6050.py <data_file.csv>")
        sys.exit(1)
        
    data_file = sys.argv[1]
    plot_sensor_data(data_file)
    generate_basic_statistics(data_file)