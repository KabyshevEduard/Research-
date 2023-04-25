import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

def open_dates(path, sheet_num):
    df = pd.read_excel(path, sheet_name=sheet_num).dropna(axis=0)
    return df

def LinReg(df):
    reg = LinearRegression()
    reg.fit(df[['Youngs modulus, GPa ', 'Ultimate strength, GPa']], df['Hardness, HB'])
    return reg.predict(df[['Youngs modulus, GPa ', 'Ultimate strength, GPa']])

def PolReg(df, n):
    pol_reg = Pipeline([('poly', PolynomialFeatures(degree=n)), ('linear', LinearRegression(fit_intercept=False))])
    pol_reg.fit(df[['Youngs modulus, GPa ', 'Ultimate strength, GPa']], df['Hardness, HB'])
    coeffs = pol_reg.named_steps['linear'].coef_
    print(coeffs)
    return pol_reg.predict(df[['Youngs modulus, GPa ', 'Ultimate strength, GPa']])

def main():
    df_1 = open_dates('C:/Users/Эдуард/Desktop/задание кафедры/train.xlsx', 0)
    df_2 = open_dates('C:/Users/Эдуард/Desktop/задание кафедры/test.xlsx', 0)
    df = pd.concat([df_1, df_2])
    df = df[(((df['Youngs modulus, GPa '] < df['Youngs modulus, GPa '].quantile(0.8)) & (df['Ultimate strength, GPa'] < df['Ultimate strength, GPa'].quantile(0.75))))]
    x_young = df['Youngs modulus, GPa '].values
    y_ultimate = df['Ultimate strength, GPa'].values
    z_hardness = df['Hardness, HB'].values

    a = str(input('Type of surface: '))
    n = int(input('Degree of polynom: '))

    if a == 'lin':
        plt.figure(figsize=(10, 8))
        axes = plt.axes(projection='3d')
        axes.scatter3D(df['Youngs modulus, GPa '].values, df['Ultimate strength, GPa'].values, df['Hardness, HB'].values)
        axes.plot_trisurf(df['Youngs modulus, GPa '].values, df['Ultimate strength, GPa'].values, LinReg(df), color='red', alpha=0.5)
        axes.set_xlabel('E')
        axes.set_ylabel('σпр, GPa')
        axes.set_zlabel('HB')
        plt.show()
    if a == 'poly':
        plt.figure(figsize=(10, 8))
        axes = plt.axes(projection='3d')
        axes.scatter3D(x_young, y_ultimate, z_hardness)
        axes.plot_trisurf(x_young, y_ultimate, PolReg(df, n), color='red', alpha=0.5)
        axes.set_xlabel('E, GPa')
        axes.set_ylabel('σпр, GPa')
        axes.set_zlabel('HB')
        plt.show()
        

if __name__ == '__main__':
    main()