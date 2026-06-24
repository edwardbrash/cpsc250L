import pandas as pd
import matplotlib.pyplot as plt


def load_weather_data(filename):
    df = pd.read_csv(filename)
    return df


def print_summary(df):
    # print summary statistics
    print(df.describe())
    # extract the mean temperature and print it
    df['average daily temperature'] = (df['high Celsius']+df['low Celsius'])/2.0
    average_temp = df['average daily temperature'].mean()
    print('Average daily temperature: ' + str(average_temp))

def add_celsius(df):
    df['high Celsius'] = (df['high']-32.0)/1.8
    df['low Celsius'] = (df['low']-32.0)/1.8
    return df

def clean_temperature_range(df, T_low_cut, T_high_cut):
    df = df[df['high Celsius'] <= T_high_cut]
    df = df[df['low Celsius'] >= T_low_cut]
    return df


def plot_temperatures(df):
    # plot both high and low temperatures on the same graph
    figure = plt.figure()
    ax = figure.add_subplot(1,1,1)
    ax.plot(df['day'], df['high Celsius'], label='High')
    ax.plot(df['day'], df['low Celsius'], label='Low')
    ax.set_title('Weather Data')
    ax.set_xlabel('Day')
    ax.set_ylabel('Temperature (Celsius)')
    ax.legend()
    plt.show()


def main():

    filename = "../data/weather_june.csv"

    dataframe = load_weather_data(filename)

    dataframe = add_celsius(dataframe)

    T_low_cut = 19.0
    T_high_cut = 31.0
    dataframe = clean_temperature_range(dataframe, T_low_cut, T_high_cut)

    print_summary(dataframe)

    plot_temperatures(dataframe)


main()
