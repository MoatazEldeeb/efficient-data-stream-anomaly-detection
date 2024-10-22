import csv
import os
import random
import time
import numpy as np


def generate_data_stream(n_points=1000, trend=0.01, seasonality_amplitude=10, noise_std=1, seasonality_period=50, stream_speed=1):
    """
    Simulates a data stream with a trend, seasonality, and noise.

    Parameters:
    - n_points: Number of data points to generate. if None it will run indefinitely
    - trend: The linear trend component (e.g., 0.01 for a gradual upward trend).
    - seasonality_amplitude: Amplitude of the seasonal fluctuations.
    - noise_std: Standard deviation of the random noise.
    - seasonality_period: The period of the seasonality (e.g., 50 for periodic fluctuations).
    - stream_speed: Time delay between each data point (in seconds).

    Yields:
    - Data points one at a time.
    """
    if n_points is None:
        t=0
        while True:
            # Trend component: grows over time (linear trend)
            trend_component = trend * t
            t+=1
            
            # Seasonality component: a sine wave to simulate periodic behavior
            seasonality_component = seasonality_amplitude * np.sin(2 * np.pi * t / seasonality_period)
            
            # Random noise component: normally distributed noise
            noise_component = np.random.normal(0, noise_std)
            
            # Combine all components to form the final data point
            value = trend_component + seasonality_component + noise_component

            # Wait to simulate a real-time data stream
            time.sleep(stream_speed)

            yield value
    else:
        for t in range(n_points):
            # Trend component: grows over time (linear trend)
            trend_component = trend * t
            
            # Seasonality component: a sine wave to simulate periodic behavior
            seasonality_component = seasonality_amplitude * np.sin(2 * np.pi * t / seasonality_period)
            
            # Random noise component: normally distributed noise
            noise_component = np.random.normal(0, noise_std)
            
            # Combine all components to form the final data point
            value = trend_component + seasonality_component + noise_component

            # Wait to simulate a real-time data stream
            time.sleep(stream_speed)

            yield value


x_value = 0
y_value = 1

field_names= ['x_value','y_value']

try:
    os.remove('data.csv')
except OSError:
    pass


with open('data.csv','a') as csv_file:
    csv_writer = csv.DictWriter(csv_file,fieldnames=field_names)
    
    csv_writer.writeheader()



n = 10000
data_stream = generate_data_stream(n_points=n, trend=0.01, seasonality_amplitude=5, noise_std=4, seasonality_period=200,stream_speed = 0.2)

i = 0
while x_value < n:
    with open('data.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

        y_value = next(data_stream)
        m = {
            "x_value" : x_value,
            "y_value": y_value
        }
        x_value+=1
        csv_writer.writerow(m)

        print(x_value,y_value)
        