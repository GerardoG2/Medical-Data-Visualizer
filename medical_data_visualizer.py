import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# create dataframe for medical data
df = pd.read_csv("medical_examination.csv", header = 0)

# Add an overweight column to the data
height_in_meters = df['height']/100
df['BMI'] = df['weight']/(height_in_meters**2)
df['overweight'] = (df['BMI']>25).astype(int)
df = df.drop(columns = ['BMI'])

# normalize data by using 1 for "bad" and 0 for "good" - cholesterol and glucose levels
df['gluc'] = ( df['gluc'] > 1 ).astype(int)
df['cholesterol'] = ( df['cholesterol'] > 1 ).astype(int)

# 
def draw_cat_plot():
    # convert data to long format to prepare for categorical plot
    df_cat = pd.melt(df, id_vars='cardio', value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index()
    df_cat = df_cat.rename(columns = {0:'total'})

    catplot = sns.catplot(data=df_cat, kind="bar", x="variable", y="total", hue="value", col='cardio')
    plt.xlabel("variable")
    fig = catplot.fig

    
    fig.savefig('catplot.png')
    return fig



def draw_heat_map():
    # 11
    df_heat = df[
                ( df['ap_lo'] <= df['ap_hi'] ) &
                ( df['height'] >= df['height'].quantile(.025) ) &
                ( df['height'] <= df['height'].quantile(.975) ) &
                ( df['weight'] >= df['weight'].quantile(.025) ) &
                ( df['weight'] <= df['weight'].quantile(.975) )
                ]  

    # create correlation matrix 
    corr = df_heat.corr()

    # remove duplicates using an upper triangular mask matrix
    mask = np.triu(np.ones_like(corr, dtype =bool))

    
    fig, ax = plt.subplots(figsize=(16,9))

    
    sns.heatmap(corr, mask=mask, annot=True, linewidths=.5, square=True, fmt="0.1f")


    
    fig.savefig('heatmap.png')
    return fig
