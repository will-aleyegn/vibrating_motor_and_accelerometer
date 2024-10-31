import time
import csv
from datetime import datetime
import os
from gpiozero import OutputDevice
import smbus

class MPU6050:
    def __init__(self, bus=1, address=0x68):
        try:
            self.bus = smbus.SMBus(bus)
            self.address = address
            
            # Wake up the MPU-6050
            self.bus.write_byte_data(self.address, 0x6B, 0)
        except Exception as e:
            print(f"Error initializing MPU6050: {e}")
            raise

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) | low
        if value > 32767:
            value -= 65536
        return value
    
    def get_data(self):
        acc_x = self.read_raw_data(0x3B) / 16384.0
        acc_y = self.read_raw_data(0x3D) / 16384.0
        acc_z = self.read_raw_data(0x3F) / 16384.0
        gyro_x = self.read_raw_data(0x43) / 131.0
        gyro_y = self.read_raw_data(0x45) / 131.0
        gyro_z = self.read_raw_data(0x47) / 131.0
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

def run_experiment(motor_pin=18, hold_time=30, sample_rate=100):
    """
    Run simple motor control (HIGH/LOW) and data collection experiment
    
    Args:
        motor_pin: GPIO pin number (BCM numbering)
        hold_time: Time to hold HIGH state in seconds
        sample_rate: Sensor sampling rate in Hz
    """
    try:
        # Initialize motor control using gpiozero
        motor = OutputDevice(motor_pin, initial_value=False)
        
        # Initialize sensor
        sensor = MPU6050()
        
        # Create timestamp for file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'motor_data_{timestamp}.csv'
        
        # Calculate delay between samples
        sample_delay = 1.0 / sample_rate
        
        print(f"Starting experiment...")
        print(f"- Recording baseline for 5 seconds")
        print(f"- Motor HIGH for {hold_time} seconds")
        print(f"- Recording post-motor for 5 seconds")
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'motor_state', 'acc_x', 'acc_y', 'acc_z', 
                         'gyro_x', 'gyro_y', 'gyro_z', 'temp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Record baseline (5 seconds)
            start_time = time.time()
            while time.time() - start_time < 5:
                data = sensor.get_data()
                data['timestamp'] = datetime.now().isoformat()
                data['motor_state'] = 0
                writer.writerow(data)
                time.sleep(sample_delay)
            
            # Turn motor on and record
            motor.on()
            print("Motor ON")
            
            start_time = time.time()
            while time.time() - start_time < hold_time:
                data = sensor.get_data()
                data['timestamp'] = datetime.now().isoformat()
                data['motor_state'] = 1
                writer.writerow(data)
                time.sleep(sample_delay)
            
            # Turn motor off and record post-motor data
            motor.off()
            print("Motor OFF")
            
            start_time = time.time()
            while time.time() - start_time < 5:
                data = sensor.get_data()
                data['timestamp'] = datetime.now().isoformat()
                data['motor_state'] = 0
                writer.writerow(data)
                time.sleep(sample_delay)
    
    except Exception as e:
        print(f"Error during experiment: {e}")
        raise
    
    finally:
        if 'motor' in locals():
            motor.close()
        print(f"\nExperiment completed. Data saved to {filename}")

if __name__ == "__main__":
    try:
        run_experiment(
            motor_pin=18,    # GPIO18 (Pin 12)
            hold_time=30,    # Hold HIGH for 30 seconds
            sample_rate=100  # 100Hz sampling rate
        )
    except KeyboardInterrupt:
        print("\nExperiment stopped by user")
    except Exception as e:
        print(f"\nError: {e}")