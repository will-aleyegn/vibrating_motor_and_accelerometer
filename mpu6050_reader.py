import smbus
import time
import csv
from datetime import datetime

class MPU6050:
    def __init__(self, bus=1, address=0x68):
        self.bus = smbus.SMBus(bus)
        self.address = address
        
        # Wake up the MPU-6050
        self.bus.write_byte_data(self.address, 0x6B, 0)
    
    def read_raw_data(self, addr):
        # Read high and low bytes
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        
        # Combine high and low bytes
        value = (high << 8) | low
        
        # Convert to signed value
        if value > 32767:
            value -= 65536
        return value
    
    def get_data(self):
        # Read accelerometer data
        acc_x = self.read_raw_data(0x3B) / 16384.0  # Convert to g's
        acc_y = self.read_raw_data(0x3D) / 16384.0
        acc_z = self.read_raw_data(0x3F) / 16384.0
        
        # Read gyroscope data
        gyro_x = self.read_raw_data(0x43) / 131.0  # Convert to degrees/sec
        gyro_y = self.read_raw_data(0x45) / 131.0
        gyro_z = self.read_raw_data(0x47) / 131.0
        
        # Read temperature
        temp = self.read_raw_data(0x41) / 340.0 + 36.53
        
        return {
            'acc_x': acc_x,
            'acc_y': acc_y,
            'acc_z': acc_z,
            'gyro_x': gyro_x,
            'gyro_y': gyro_y,
            'gyro_z': gyro_z,
            'temp': temp
        }

def record_data(duration_seconds=60, sample_rate=10):
    sensor = MPU6050()
    filename = f'mpu6050_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    # Calculate number of samples
    num_samples = duration_seconds * sample_rate
    delay = 1.0 / sample_rate
    
    print(f"Recording data for {duration_seconds} seconds at {sample_rate} Hz")
    print(f"Saving to {filename}")
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'acc_x', 'acc_y', 'acc_z', 
                     'gyro_x', 'gyro_y', 'gyro_z', 'temp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        try:
            for _ in range(num_samples):
                data = sensor.get_data()
                data['timestamp'] = datetime.now().isoformat()
                writer.writerow(data)
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print("\nRecording stopped by user")
        
        print(f"\nData saved to {filename}")

if __name__ == "__main__":
    record_data(duration_seconds=60, sample_rate=10)