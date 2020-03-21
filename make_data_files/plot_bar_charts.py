# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from summarise_data import *

def plot_bar_chart(df, key):

    # set font
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = 'Helvetica'

    # set the style of the axes and the text color
    plt.rcParams['axes.edgecolor']='#333F4B'
    plt.rcParams['axes.linewidth']=0.8
    plt.rcParams['xtick.color']='#333F4B'
    plt.rcParams['ytick.color']='#333F4B'
    plt.rcParams['text.color']='#333F4B'

    df.sort_values(by = key, inplace = True)

    # we first need a numeric placeholder for the y axis
    my_range=list(range(1,len(df.index)+1))

    fig, ax = plt.subplots(figsize=(5,3.5))

    plt.hlines(y=my_range, xmin=0, xmax=df[key], color='#007ACC', alpha=0.5, linewidth=5)

    plt.plot(df[key], my_range, "o", markersize=5, color='#007ACC', alpha=0.6)

    ax.set_xlabel('Building count', fontsize=10, fontweight='black', color = '#333F4B')
    ax.set_ylabel('')

    ax.tick_params(axis='both', which='major', labelsize=8)
    plt.yticks(my_range, df.index)

    fig.text(-0.23, 0.96, 'Building type', fontsize=10, fontweight='black', color = '#333F4B')

    # change the style of the axis spines
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)

    # set the spines position
    ax.spines['bottom'].set_position(('axes', -0.04))
    ax.spines['left'].set_position(('axes', 0.015))

    #plt.savefig('building_types_heating.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_cbecs_heating():
    df = summarise_cbecs()
    df.drop(labels = ['All'], axis = 0, inplace = True)
    key = 'heating'
    plot_bar_chart(df, key)

def plot_cbecs_cooling():
    df = summarise_cbecs()
    df.drop(labels = ['All'], axis = 0, inplace = True)
    key = 'ng_cool'
    plot_bar_chart(df, key)