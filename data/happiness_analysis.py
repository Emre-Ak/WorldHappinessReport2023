import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import scipy.stats as stats


def load_data(filepath):
    '''loading the world hapiness report'''
    df = pd.read_csv(filepath)
    return df


def clean_data(df):
    '''cleaning the data'''
    # drop Ladder score in Dystopia since the values in the column are all the same (no value)
    df.drop('Ladder score in Dystopia', axis=1, inplace=True)

    # drop not needed columns
    df.drop(df.iloc[:, 2:11], axis=1, inplace=True)

    # drop Country State of Palestine as it is the only country will NaN values and the ladder score cannot be calculated with the missing data
    df.drop(98, inplace=True)

    # rename Ladder score column into Happiness Score
    df.rename(columns={"Ladder score": "Happiness Score"}, inplace=True)

    # get top 10 happiest countries
    top_10 = df.groupby("Country name")["Happiness Score"].sum().sort_values(ascending=False).head(10)

    # get top 10 unhappiest countries
    bot_10 = df.groupby("Country name")["Happiness Score"].sum().sort_values(ascending=False).tail(10)

    # get top 10 happiest and top 10 unhappiest countries
    total_20 = pd.concat([top_10, bot_10], axis=0).sort_values(ascending=False)

    # prepare normalized colors for plot top 10 graph
    cmap = plt.cm.RdYlGn
    norm = plt.Normalize(vmin=df['Happiness Score'].min(), vmax=df["Happiness Score"].max())
    colors = [cmap(norm(value)) for value in df["Happiness Score"]]

    # plot top 10 happiest countries
    top_10_plot = top_10.plot.barh(title="Top 10 happiest Countries", xlabel="Country", ylabel="Happiness Score",
                                   color=colors, figsize=(10, 4), fontsize="large")
    top_10_plot = top_10_plot.invert_yaxis()

    # prepare normalized colors for plot bot 10 graph
    cmap2 = plt.cm.seismic
    norm2 = plt.Normalize(vmin=df['Happiness Score'].min(), vmax=df["Happiness Score"].max())
    colors2 = [cmap2(norm2(value)) for value in df["Happiness Score"]]

    # plot top 10 unhappiest (bottom) countries
    bot_10_plot = bot_10.plot.barh(title="Top 10 unhappiest Countries", xlabel="Country", ylabel="Happiness Score",
                                   color=colors2, figsize=(10, 4), fontsize="large")
    bot_10_plot = bot_10_plot.invert_yaxis()

    # plot top 10 happiest and top 10 unhappiest countries
    total_20_plot = total_20.plot.barh(title="Top 10 happiest and Top 10 unhappiest Countries", xlabel="Country",
                                       ylabel="Happiness Score", color=colors2, figsize=(10, 4), fontsize="large")
    total_20_plot = total_20_plot.invert_yaxis()

    plt.show()

    return df


def visualize_data(df):
    '''visualize the data'''

    # get sorted Happiness Score
    happiness = df.groupby("Country name")["Happiness Score"].sum().sort_values(ascending=False)
    happiness

    # get a visualization of the happiness distribution
    fit = stats.norm.pdf(happiness, np.mean(happiness), np.std(happiness))
    pl.plot(happiness, fit)
    pl.hist(happiness)
    plt.axvline(x=df["Happiness Score"].mean(), color="red")
    plt.axvline(x=5, color="black")
    pl.show()
    
    return df


def main():
    if len(sys.argv) == 2:

        filepath = sys.argv[1]

        print('Loading data...\n    World Happiness Report: {}'.format(filepath))
        df = load_data(filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Visualizing data...')
        df = visualize_data(df)

        print('Data is cleaned! For further information head over to the medium post. Link is provided in the README.md')

    else:
        print('Please provide the filepaths World Happiness Report' \
              'datasets as the first argument. \n\nExample: python hapiness_analysis.py ' \
              'WHR2023.csv ')


if __name__ == '__main__':
    main()