import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.optimize import curve_fit


def load_data(filename):
    df = pd.read_csv(filename)
    return df

def fit_line(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

def fit_statsmodel(df):
    y = df['score']
    Xsm = df['hours']
    Xsm = sm.add_constant(Xsm)
    model = sm.OLS(y, Xsm)
    results = model.fit()
    return results

def fit_curve_fit(df):
    xi = df['hours']
    yi = df['score']
    init_vals = [0,0]
    popt, pcov = curve_fit(fitfunction, xi, yi, p0=init_vals, absolute_sigma=False)
    perr = np.sqrt(np.diag(pcov))
    slope_cf = popt[0]
    intercept_cf = popt[1]
    dslope_cf = perr[0]
    dintercept_cf = perr[1]
    return slope_cf, intercept_cf, dslope_cf, dintercept_cf

def predict(x, slope, intercept):
    y_fit = slope * x + intercept
    return y_fit

def fitfunction(x,*param):
    return param[0]*x + param[1]

def main():
    # Get the file into a dataframe
    filename = "../data/study_scores.csv"
    df = load_data(filename)

    # calculate the slope and intercept of the best fit line
    slope, intercept = fit_line(df['hours'], df['score'])
    print("Best fit: y = {slope:.4f}x + {intercept:.4f}".format(slope=slope, intercept=intercept))
    print('-------------------------------------')

    # get the best fit line (as data for plotting)
    y_fit = predict(df['hours'], slope, intercept)

    # make the plot
    plt.figure()
    plt.plot(df['hours'], df['score'], 'o', label='Exam Score')
    plt.plot(df['hours'], y_fit, 'r-', label=f'Linear Fit - y = {slope:.4f}x + {intercept:.4f}')
    plt.title('Computer Science 250 Final Exam Score')
    plt.xlabel("Study Hours")
    plt.ylabel("Exam Score")
    plt.legend()
    plt.show()

    # Use statsmodels for comparison!
    results = fit_statsmodel(df)
    print(results.summary())
    print('---------------------------------------')

    # Now, use curve_fit for comparison to statsmodels errors
    slope_cf, intercept_cf, dslope_cf, dintercept_cf  = fit_curve_fit(df)
    print(f"Curve Fit: y = ({slope_cf:.4f} +/- {dslope_cf:.3f})x + ({intercept_cf:.4f} +/- {dintercept_cf:.3f})")

main()
