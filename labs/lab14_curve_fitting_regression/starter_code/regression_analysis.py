import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(filename):
    df = pd.read_csv(filename)
    return df


def fit_line(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept


def predict(x, slope, intercept):
    y_fit = slope * x + intercept
    return y_fit


def main():
    filename = "../data/study_scores.csv"
    df = pd.read_csv(filename)

    plt.figure()
    plt.plot(df['hours'], df['score'], 'o', label='Exam Score')
    plt.title('Computer Science 250 Final Exam Score')
    plt.xlabel("Study Hours")
    plt.ylabel("Exam Score")


    slope, intercept = fit_line(df['hours'], df['score'])
    y_fit = predict(df['hours'], slope, intercept)
    plt.plot(df['hours'], y_fit, 'r-', label=f'Linear Fit - y = {slope:.2f}x + {intercept:.2f}')

    plt.legend()
    plt.show()


main()
