import pandas as pd
import seaborn as sns
import matplotlib as mpl  
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('diabetes.csv')
# print(df.info())
Columns = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age','Outcome']

def min_max_std():
	for name in Columns:
		field = df[name]
		print(field.describe())

def hist():
	for name in Columns:
		field = df[name]
		hist = sns.distplot(field)
		hist.set_xlabel(name)
		plt.show()

def corr():
	print(df.corr())

def missing():
	missing_field = ['Glucose', 'BloodPressure', 'SkinThickness', 'BMI']
	for name in missing_field:
		print(df[name].replace(0,df[name].mean()))

def z_score_nor():
	for name in Columns:
		col_zscore = name + 'z_score'
		df[col_zscore] = (df[name]-df[name].mean())/df[name].std()
	print (df)
def mi_ma_nor():
	for name in Columns:
		col_mimascore = name + 'mima_score'
		df[col_mimascore] = (df[name] - df[name].min())/(df[name].max()-df[name].min())
	print(df)

def binning_age():
	bins = [20, 31, 41, 51, 61, 71, 81]
	df['bin_age'] = pd.cut(df['Age'],bins)
	print (df.loc[:,['Age','bin_age']])

def multi_value2col():
	val = [21, 31, 41, 51, 61, 71, 81]	
	for v in val:
		age_x_y = 'age_' + str(v) + '_' + str(v + 10)
		# if (df['Age'] >= 21):
		age = []
		for row in df['Age']:
			if (row >= v) and (row <= (v + 10)):
				age.append(1)
			else: 
				age.append(0)
		df[age_x_y] = age  
		print (df.loc[:,['Age',age_x_y]])
multi_value2col()
# print(df.corr())
# print(df['BMI'][0])
# Glucose = df['Glucose']
# Glu_mean = Glucose.mean()
# a = Glucose.replace(0,Glu_mean)
# miss_glu = a[a == 0]
# print(miss_glu)