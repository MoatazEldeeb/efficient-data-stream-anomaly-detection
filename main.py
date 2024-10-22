import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')

SEASONAL_PERIOD = 200



def annomaly_detection(df: pd.DataFrame):
    """
    Calculates the anomalies in a datafram

    Parameters:
    - df: A pandas datafram in which the algorithm will run detecting anomalies

    Returns:
    - outliers indexes
    """

    # Get the trend by averaging (convolution) the values by window size = SEASONAL_PERIOD
    df['trend'] = df['y_value'].rolling(window=SEASONAL_PERIOD, center=True).mean()

    # Detrend the data by subtracting the trend
    detrended = df['y_value'] - df['trend']

    # Calculate seasonality by averaging each corresponding position in period
    seasonality = detrended.groupby(df.index % SEASONAL_PERIOD).mean()

    # Map the seasonal values back to the original data
    df['seasonal'] = df.index % SEASONAL_PERIOD
    df['seasonal'] = df['seasonal'].map(seasonality)

    # Subtract the trend and seasonal from values to get the residual
    df['residual'] = df['y_value'] - df['trend'] - df['seasonal']

    # Calculate upper and lower limits of the residuals using the mean and standard deviation 
    resid_mean = df['residual'].mean()
    resid_std = df['residual'].std()
    lower = resid_mean - 3* resid_std
    upper = resid_mean + 3* resid_std

    # Get the indexes of the outliers using the limits
    outliers_indexes = df[(df['residual'] > upper) | (df['residual'] < lower)].index
    return outliers_indexes



def animate(i):
    """
        Function to be called each time the interval of [FuncAnimation]
        finishes.
    """
    # Read the csv
    data = pd.read_csv('data.csv')

    # Get x-axis values and y-axis values
    x= data['x_value']
    y = data['y_value']

    
    outlier_indexes = annomaly_detection(data)
    print("Anomalies:")
    print(outlier_indexes)

    # Clear output of plt figure
    plt.cla()

    # Plot the data points using blue color
    plt.plot(x,y, label='Values', color='blue', marker='o')
    # Highlight the outliers using red color
    plt.plot(outlier_indexes, data.loc[outlier_indexes, 'y_value'], 'ro', label='Anomalies')

    plt.title(f'Data Points with seasonal period = {SEASONAL_PERIOD}')

    # Add legend
    plt.legend()
    plt.tight_layout()

# Use FuncAnimation to call animate function every interval passes every interval microseconds
ani = FuncAnimation(plt.gcf(),animate,interval = 200)

plt.tight_layout()
plt.show()
