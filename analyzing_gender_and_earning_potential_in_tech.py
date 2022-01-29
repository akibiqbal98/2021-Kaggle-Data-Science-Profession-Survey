# -*- coding: utf-8 -*-
"""Analyzing Gender and Earning Potential in Tech.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yehC7ABXaFKbRSdcAidrx38Aqmcb1_Yz

# Attempting to Quantify Gender Differences in Kaggle Dev Survey 

In this notebook I:

- First visualize and normalize gender differences in the sample
Run a multiple linear regression to understand which factors contribute most to earning potential.
- Run a lasso regression to narrow variable set and try to quantify the extent gender impacts earning potential.
- Run a random forest on same data to evaluate feature importance (A nonlinear model like this is a good check).
- Compare models for just subsets of women and men to hopefully normalize for more variables.
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt #likley won't be used much as i'm experimenting with plotly 
import plotly.graph_objects as go #you will be learning how go and px work with me! 
import plotly.express as px 

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

url = 'https://raw.githubusercontent.com/akibiqbal98/2021-Kaggle-Data-Science-Profession-Survey/master/kaggle_survey_2021_responses.csv'
df = pd.read_csv(url)
df.head()

df.shape

df_fin = df.iloc[1:, :]

#create a dictionary for questions 
Questions = {}

#create list of questions 
#not very efficient, but keeps things ordered
qnums = list(dict.fromkeys([i.split('_')[0] for i in df_fin.columns]))

#add data for each question to key value pairs in dictionary
for i in qnums:
    if i in ['Q1','Q2','Q3']: #since we are using .startswith() below this prevents all questions that start with 
        Questions[i] = df_fin[i] #[1,2,3] from going in the key value pair (Example in vid)
    else:
        Questions[i] = df_fin[[q for q in df_fin.columns if q.startswith(i)]]

# create disctionary for different gender selections 
Genders = {}
for i in df_fin.Q2.unique():
    Genders[i] = df_fin[df_fin.Q2 == i]

#look at gender distribution
df_fin.Q2.value_counts()/ df_fin.Q2.value_counts().sum()

#filter dataframe for male & female for simplicity (not that prefer not & nonbinary aren't important!)
df_mf = df_fin[df_fin.Q2.isin(['Man','Woman'])]

#DS is clearly already a male dominated field (or at least this sample of kaggle users is)
df_mf.Q2.value_counts()/ df_mf.Q2.value_counts().sum()

#Female Distribution by Role 
fig= px.histogram(df_mf,x='Q4',color ='Q2')
fig.show()

#Female Distribution by Role Normalized by sample of respective population 
fig= px.histogram(df_mf,x='Q4',color ='Q2', histnorm='probability density')
fig.show()

#Percent more or less than distribution of the average population of women (Absolute)
male_degrees = df_mf[df_mf.Q2 == 'Man'].Q4.value_counts()
female_degrees = df_mf[df_mf.Q2 == 'Woman'].Q4.value_counts()
total_degrees = df_mf.Q4.value_counts()
more_women = (female_degrees/total_degrees)-.1918 #greater proportion of women than sample
more_women['Color'] = np.where(more_women.values <0, 'blue','red')
fig = go.Figure(go.Bar(x=(female_degrees/total_degrees).index, y= (female_degrees/total_degrees).values-.197, marker_color=more_women.Color))
fig.update_layout(title= "Level of Female Education Relative to AVG of Sample (19.18%)")
fig.show()

#Female Distribution by Country
fig= px.histogram(df_mf,x='Q3',color ='Q2')
fig.update_xaxes(categoryorder= "total descending")
fig.show()

male_country = df_mf[df_mf.Q2 == 'Man'].Q3.value_counts()
female_country = df_mf[df_mf.Q2 == 'Woman'].Q3.value_counts()
total_country = df_mf.Q3.value_counts()

total_country

female_country

#Percent more or less than distribution of the average population of women 
more_women = (female_country/total_country)-.197 #greater proportion of women than sample
more_women['Color'] = np.where(more_women.values <0, 'blue','red')
fig = go.Figure(go.Bar(x=(female_country/total_country).index, y= (female_country/total_country).values-.197, marker_color=more_women.Color))
fig.update_layout(title= "Amount of Women By Country Relative to AVG of Sample (19.7%)")
fig.update_layout(xaxis={'categoryorder':'total descending'})
fig.show()

"""**Notes:**
> As we can see from the graph Tunisia has more avarage female than all other countries. 

> On the other hand japan's tech is mostly dominating by male.
"""

#function for creating new graphs 
def create_norm_graph(qnum, data, title, baseline):
    male = data[data.Q2 == 'Man'][qnum].value_counts()
    female = data[data.Q2 == 'Woman'][qnum].value_counts()
    total = data[qnum].value_counts()
    more_women = (female/total)-baseline #greater proportion of women than sample
    more_women['Color'] = np.where(more_women.values <0, 'blue','red')
    fig = go.Figure(go.Bar(x=(female/total).index, y= (female/total).values-baseline, marker_color=more_women.Color))
    fig.update_layout(title= title)
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.show()
    return

# which countries have the most relative female representitives in the survey?
create_norm_graph('Q3',df_mf,"Amount of Women By Country Relative to AVG of Sample (19.18%)",.1918)

#Which roles have the most women relative to the baseline?
create_norm_graph('Q5',df_mf,"Amount of Women By Role Relative to AVG of Sample (19.7%)",.1918)

#create new baseline for only employed people
df_workers_mf = df_mf[~df_mf['Q5'].isin(['Student','Currently not employed'])]
df_workers_mf.Q2.value_counts()/df_workers_mf.Q2.value_counts().sum()

# Women's experience 
create_norm_graph('Q6',df_workers_mf,"Amount of Women By Experience Relative to AVG of Sample (16.9%)",.169)

#absolute number is a lot lower 
df_workers_mf.Q6.value_counts()

#by income level 
create_norm_graph('Q25',df_workers_mf,"Amount of Women By Income Level Relative to AVG of Sample (16.9%)",.169)
df_workers_mf.Q25.value_counts()

#graph for just data scientists 
df_mf_ds= df_mf[df_mf['Q5'] =='Data Scientist']
create_norm_graph('Q25',df_mf_ds,"Amount of Women By Country Relative to AVG of Sample (16.9%)",.169)

#count for perspective, some sample size issues here
df_mf_ds.Q25.value_counts()

#graph for US 
df_mf_US= df_mf[df_mf['Q3'] =='United States of America']
create_norm_graph('Q25',df_mf_US,"Amount of Women By Country Relative to AVG of Sample (16.9%)",.169)

#graph for India 
df_mf_US= df_mf[df_mf['Q3'] =='India']
create_norm_graph('Q25',df_mf_US,"Amount of Women By Country Relative to AVG of Sample (16.9%)",.169)

#Income by role (awful graph I know)
fig= px.histogram(df_fin.dropna(subset=['Q25','Q5']),x='Q25',color ='Q5')
fig.update_xaxes(categoryorder= "total descending")
fig.show()

#Income by experience 
fig= px.histogram(df_fin.dropna(subset=['Q25','Q6']),x='Q25',color ='Q6')
fig.update_xaxes(categoryorder= "total descending")
fig.show()

#Income by education
fig= px.histogram(df_fin.dropna(subset=['Q25','Q4']),x='Q25',color ='Q4')
fig.update_xaxes(categoryorder= "total descending")
fig.show()

"""## Building a Model

- **I thought it made more sense to use a regression here to try to predict salary. Although it will be very rough around the edges, I think converting the salaries from categorical to numeric will allow us to more easily interperet the data.**

> convert dollar ranges to numeric 

> explore converting other continuious variables 

>build model with just gender 
"""

#replace '$',',','>' in data 
df_model = df_fin.dropna(subset=['Q25'])
df_model['salary_cleaned'] = df_model.Q25.apply(lambda x: str(x).replace('$','').replace(',','').replace('>','').strip())
df_model.salary_cleaned.value_counts()

#create min range and max range for salary 
df_model['salary_min'] = df_model.salary_cleaned.apply(lambda x: 500000 if '-' not in x else int(x.split('-')[0]))
df_model['salary_max'] = df_model.salary_cleaned.apply(lambda x: 500000 if '-' not in x else int(x.split('-')[1]))

df_model.salary_max.value_counts()

#Convert to rough continuous variable 
df_model['aprox_salary'] = (df_model.salary_min+df_model.salary_max)/2
df_model.aprox_salary.value_counts()

#simple linear regression just gender 
import statsmodels.api as sm

#filter for men & women 
df_model_fin = df_model[df_model.Q2.isin(['Man','Woman'])] 
#filter for workers 
df_model_fin = df_model_fin[~df_model_fin['Q5'].isin(['Student','Currently not employed'])]
df_model_fin.drop('Time from Start to Finish (seconds)', axis =1, inplace = True)

df_model_fin.isnull().any()

# create dummy variables, this is needed because essentially all our data is categorical
model_dummies = pd.get_dummies(df_model_fin)
model_dummies

# We only need one gender in this case because we trimmed it to only have Men & Women
Y = model_dummies.aprox_salary
X = model_dummies.Q2_Man

#for statsmodels, we need to add a constant to create intercept 
X = sm.add_constant(X)

#fit model with data 
model = sm.OLS(Y,X)
results= model.fit()

#create summary report 
results.summary()

# create function to add additional questions to dataframe for easier processing
def qnums(question_list, dataframe):
    q_out = [] 
    for i in question_list:
        for j in dataframe.columns:
            if i == j.split('_')[0]:
                q_out.append(j)
    return dataframe.loc[:,q_out]
        
#create data for questions 2,4,5
q245 =  qnums(['Q2','Q4','Q5'], model_dummies)
q245

#drop one of the gender columns, it is redundant 
X = q245.drop('Q2_Man', axis=1)
X = sm.add_constant(X)

#build model with additional features education, gender, and role 
model = sm.OLS(Y,X)
results= model.fit()
results.summary()

#questions 2,4,5,7 add in programming languages 
        
q2457 =  qnums(['Q2','Q4','Q5','Q7'], model_dummies).drop('Q2_Man', axis=1)
q2457

X = q2457
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results= model.fit()
results.summary()

#questions 2,3,4,5,7 add in country (huge boost in model performance)
        
q24573 =  qnums(['Q2','Q4','Q5','Q7','Q3'], model_dummies).drop('Q2_Man', axis=1)
q24573

X = q24573
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results= model.fit()
results.summary()

#questions 2,3,4,5,6,7,21
#question 21 is about the size of the company 
        
q245736 =  qnums(['Q2','Q4','Q5','Q7','Q3','Q6','Q21'], model_dummies).drop('Q2_Man', axis=1)
X = q245736
X = sm.add_constant(X)

model2 = sm.OLS(Y,X)
results= model2.fit()
results.summary()

#fit model with lasso parameters Set alpha high enough to eliminate some variables 
results_reg = model2.fit_regularized(L1_wt=1, alpha= 5)
final = sm.regression.linear_model.OLSResults(model2,results_reg.params,model2.normalized_cov_params)
print(final.summary())

from sklearn.ensemble import RandomForestRegressor

#compare random forest feature importance (allows us to rank)
clf_rf = RandomForestRegressor()
clf_rf.fit(X,Y)

feat_importances = pd.Series(clf_rf.feature_importances_, index=X.columns)
ax  = feat_importances.nlargest(25).sort_values().plot(kind='barh', figsize=(6,12))
ax.barh([2],feat_importances.loc['Q2_Woman'],color='red')

#build models for men and women independently. See how they estimate salary on the same data 
#I think this is a decent way to isolate individual effects of education, country, etc.
Women_Model = model_dummies[model_dummies.Q2_Man == 0]
Men_Model = model_dummies[model_dummies.Q2_Man == 1]

# create and train women's model 
women_fin =  qnums(['Q4','Q5','Q7','Q3','Q6','Q21'], Women_Model)
Y_W = Women_Model.aprox_salary
X_W = women_fin
X_W = sm.add_constant(X_W)

Women_Model

model_W = sm.OLS(Y_W,X_W)
results_W= model_W.fit()
results_W.summary()

results_reg_W = model_W.fit_regularized(L1_wt=1, alpha= 5)
final_W = sm.regression.linear_model.OLSResults(model_W,results_reg_W.params,model_W.normalized_cov_params)
print(final_W.summary())

#create and train men's model 
men_fin =  qnums(['Q4','Q5','Q7','Q3','Q6','Q21'], Men_Model)
Y_M = Men_Model.aprox_salary
X_M = men_fin
X_M = sm.add_constant(X_M)

model_M = sm.OLS(Y_M,X_M)
results_M= model_M.fit()
results_M.summary()

results_reg_M = model_M.fit_regularized(L1_wt=1, alpha= 5)
final_M = sm.regression.linear_model.OLSResults(model_M,results_reg_M.params,model_M.normalized_cov_params)
print(final_M.summary())

#run model on all data & compare 
combined_data = qnums(['Q4','Q5','Q7','Q3','Q6','Q21'], model_dummies)
male_preds = final_M.predict(np.array(sm.add_constant(combined_data)))
female_preds = final_W.predict(np.array(sm.add_constant(combined_data)))

combined_data['male_preds'] = male_preds
combined_data['female_preds'] = female_preds

combined_data['aprox_salary'] = model_dummies.aprox_salary
combined_data

px.scatter(combined_data.sort_values('aprox_salary'), x = 'aprox_salary', y = ['male_preds','female_preds'])

model_comp = sm.OLS(combined_data['male_preds'],sm.add_constant(combined_data['female_preds']))
results_comp = model_comp.fit()
results_comp.summary()

"""- **The male_model is predicting approx. 2% higher than the female_model salary is**"""

combined_data['projected_diff'] = combined_data.male_preds - combined_data.female_preds

combined_data.projected_diff.mean()

combined_data.projected_diff.std()

combined_data['women_prj_higher'] = combined_data.projected_diff.apply(lambda x: 1 if x < 0 else 0)

combined_data.women_prj_higher.value_counts()

