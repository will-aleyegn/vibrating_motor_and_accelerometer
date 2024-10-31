# Vibrating Motor and MPU6050 Accelerometer Setup

## Hardware Components
- Raspberry Pi (with GPIO pins)
- MPU6050 Accelerometer/Gyroscope module
- Small 3V DC vibrating motor (0.06W, ~20mA) [https://www.amazon.com/gp/product/B0967SC28N/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1]

## Pin Connections

### MPU6050 to Raspberry Pi
| MPU6050 Pin | Raspberry Pi Pin | Description |
|-------------|-----------------|-------------|
| VCC         | Pin 1 (3.3V)    | Power       |
| GND         | Pin 6 (Ground)  | Ground      |
| SCL         | Pin 5 (GPIO 3)  | I2C Clock   |
| SDA         | Pin 3 (GPIO 2)  | I2C Data    |
| XDA         | Not Connected   | -           |
| XCL         | Not Connected   | -           |
| AD0         | Not Connected   | -           |
| INT         | Not Connected   | -           |

### Motor to Raspberry Pi
| Motor Wire  | Raspberry Pi Pin | Description |
|-------------|-----------------|-------------|
| Positive    | GPIO 18 (Pin 12)| Control signal |
| Negative    | Ground Pin      | Ground      |


## Running the Experiment

The experiment consists of three phases:
1. 5 seconds baseline recording (motor off)
2. 30 seconds motor running
3. 5 seconds post-motor recording

To run:
```bash
sudo python3 motor_ON_mpu6050_reader.py
```

Data will be saved to a timestamped CSV file containing:
- Timestamps
- Motor state (0/1)
- Accelerometer readings (X, Y, Z)
- Gyroscope readings (X, Y, Z)
- Temperature

## Data Collection
The script records:
- Accelerometer data (in g's)
- Gyroscope data (in degrees/second)
- Temperature data
- Motor state
- Timestamps

Example data format:
```csv
timestamp,motor_state,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,temp
2024-10-31T12:00:00.000,0,0.05,-0.02,1.00,-0.21,0.35,-0.15,25.6
```
