# 2021 Kaggle Machine Learning & Data Science Survey
 ![image](https://user-images.githubusercontent.com/51336709/151690629-fe271df2-efb0-4426-95f3-75a96d3ba2e2.png)

This repo represents the new Kaggle Survey analysis [the 2021 Kaggle Machine Learning &amp; Data Science Survey](https://www.kaggle.com/c/kaggle-survey-2021).


## Files

**The repo contains the following Files:**
- *2021_Kaggle_Data_Science_Profession_Survey.ipynb* - In this *ipynb* file  I approach data cleaning, data manipulation, and some light Exploratory data analysis and also i tried to answer these following questions:
   - Different skills by profession
   - Pay differences based on skills (tools, coding ability, languages)
    - What opportunities come from higher education
    - What did people leave blank the most?


- *Analyzing_Gender_and_Earning_Potential_in_Tech.ipynb* - In this notebook I:

    - First visualize and normalize gender differences in the sample
    - Run a multiple linear regression to understand which factors contribute most to earning potential.
    - Run a lasso regression to narrow variable set and try to quantify the extent gender impacts earning potential.
    - Run a random forest on same data to evaluate feature importance (A nonlinear model like this is a good check).
    - Compare models for just subsets of women and men to hopefully normalize for more variables.

## Algorithms & process 
    From a technical perspective, I do the following:
    - Outline my analysis 
    - load in and briefly explore the data 
    - Check for null values 
    - Organize the data so that it can be easily used to create charts 
    - Create some basic charts with plotly express and plotly go
    - Organize the data so that it can be segmented by profession 
    - Build one "advanced visual" showing you the 4 iterations that it took me to get there 
    - Build a dropdown button for comparing between different datas for "Advance visual"

## Graphs and Plots
   ![App Screenshot](https://github.com/akibiqbal98/2021-Kaggle-Data-Science-Profession-Survey/blob/master/Comparing%20coding%20by%20position.png.png)
  
   ![Education by positon](https://github.com/akibiqbal98/2021-Kaggle-Data-Science-Profession-Survey/blob/master/Comparing%20education%20by%20position.png.png)
   
   ![Age by positon](https://github.com/akibiqbal98/2021-Kaggle-Data-Science-Profession-Survey/blob/master/Age%20by%20position.png)
   
   
## Tech used 
   - Jupyter notebook
   - Numpy
   - Pandas
   - Matplotlib
   - [Plotly](https://plotly.com/)
   - [Statsmodel](https://www.statsmodels.org/stable/index.html)
   - [Scikit-learn](https://scikit-learn.org/stable/)




