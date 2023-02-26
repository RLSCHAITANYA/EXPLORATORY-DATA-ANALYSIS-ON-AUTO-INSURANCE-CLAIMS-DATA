#!/usr/bin/env python
# coding: utf-8

# # 1.PROBLEM INFO¶

# Exploratory Data Analysis(EDA) on Auto Insurance Claims Data Set

# # VARIABLE EXPLANATION
# 

# In[ ]:


1.months_as_customer 
2.age 
3.policy_number
4.policy_bind_date
5.policy_state
6.policy_csl
7.policy_deductable
8.policy_annual_premium
9.umbrella_limit
10.insured_zip
11.insured_sex
12.insured_education_level
13.insured_occupation
14.insured_hobbies
15.insured_relationship
16.capital-gains
17.capital-loss
18.incident_date
19.incident_type
20.collision_type
21.incident_severity
22.authorities_contacted
23.incident_state
24.incident_city
25.incident_location
26.incident_hour_of_the_day
27.number_of_vehicles_involved
28.property_damage
29.bodily_injuries
30.witnesses
31.police_report_available
32.total_claim_amount
33.injury_claim
34.property_claim
35.vehicle_claim
36.auto_make
37.auto_model
38.auto_year
39.fraud_reported
40_c39
      


# # IMPORTING LIBRARIES
# 
# 

# In[7]:


import pandas as pd  
import numpy as np     
import matplotlib.pyplot as plt 
import seaborn as sns   
import warnings 
from six.moves import urllib
import os
warnings.filterwarnings("ignore")


# In[11]:


data = pd.read_csv("C:/Users/CHAITANYA/Downloads/archive (2)/insurance_claims.csv")


# # DATACOLLECTION
# 

# In[12]:


data.head()


# In[13]:


data.tail()


# In[14]:


data.shape 


# In[15]:


data.describe()


# In[16]:


data.info()


# # EXPLORING DATA
# 

# In[17]:


data.columns


# In[18]:


numeric_features = [feature for feature in data.columns if data[feature].dtypes != 'O']
categorical_features = [feature for feature in data.columns if data[feature].dtypes == 'O']
print('We have {} numerical features : {}'.format(len(numeric_features), numeric_features))
print('\nWe have {} categorical features : {}'.format(len(categorical_features), categorical_features))


# In[19]:


data.isnull().sum()


# In[20]:


counts = data.nunique()
counts


# In[21]:


data[['police_report_available','collision_type']]


# The columns 'police_report_available' & 'collision_type' have some missing values and are represented as '?' so we will be replacing them with nan values.

# In[22]:


data = data.replace({ "?": np.nan})
data


# # ANALYSIS
# 

# # UNIVARITE ANALYSIS

# # BIVARAITE ANALYSIS

# In[52]:


difference_in_mean = data.groupby(["policy_state", "insured_sex"])[["months_as_customer","age","policy_annual_premium","total_claim_amount"
]].mean()
difference_in_mean

1.The mean age of Male is greater than Female in every state. Illinois is the only state where the mean annual premium for male is less than the mean annual premium of a female.
2.The Mean total claim amount in all 3 states is more than 50,000 Dollars. Mean Claim amount is higher for Females compared to the men.
3.Even though more than half of the people insured are females, male have been customer for higher number of months
# # CITY WISE CLAIM SETTELMENT ANALYSIS

# In[53]:


city_wise_analysis = data.groupby('incident_city')[['policy_annual_premium','total_claim_amount']].sum().sort_values(ascending=False, by='policy_annual_premium')
city_wise_analysis


# In[55]:


city_wise_analysis['Claim Settlement'] = city_wise_analysis['total_claim_amount']-city_wise_analysis['policy_annual_premium']
city_wise_analysis

The claim settlement is minimum for city SpringField, where the difference between the total claim amount and total annual premium collection is the highest.
# # WHICH AUTHORITY IS CONTACTED FIRST DURING ACCIDENTS

# In[56]:


Accident_emergency = pd.crosstab(data.authorities_contacted,data.incident_severity)
Accident_emergency

In case of a major damage, people are seen to be contacting the Fire Department authorities which may be due to fire post accident or as a precuationary measure. For other minor damages or total loss people have the tendency to contact the police.
# # CHANGE IN MEAN DEPENDING UPON THE NUMBER OF WITNESSES

# In[62]:


data[data.witnesses==0]['total_claim_amount'].mean()


# In[63]:


data[data.witnesses==1]['total_claim_amount'].mean()


# In[64]:


data[data.witnesses==2]['total_claim_amount'].mean()


# In[65]:


data[data.witnesses==3]['total_claim_amount'].mean()

From the above results, we can say that, the number of witnesses doesnot affect the total claim amount in the car insurance settlement.
# # MULTIVARITE ANALYSIS

# In[26]:


Gender_count = data.insured_sex.value_counts()


# In[27]:


Hobbies_pct = data.insured_hobbies.value_counts()*100/data.insured_hobbies.count()


# In[28]:


Profession_pct = data.insured_occupation.value_counts()*100/data.insured_occupation.count()


# In[29]:


Auto_model = data.auto_model.value_counts().head(5)


# In[30]:


Months_as_customer = pd.cut(data.months_as_customer,bins=[0,150,300,450],labels=['Newly Enrolled','Short-Term','Long-Term Customer'])


# In[32]:


fig,axes = plt.subplots(2,3,figsize=(15,10))
plt.tight_layout(pad=8)
plt.grid(False)
sns.set_style("whitegrid", {'axes.grid' : False})

axes[0,0].set_title('Gender Distribution',fontsize=15,color='blue')
axes[0,0].pie(data.insured_sex.value_counts(),labels=Gender_count.index,autopct='%1.1f%%',startangle=180)
axes[0,0].legend()

axes[0,1].set_xlabel('Number of People',fontsize=15)
axes[0,1].set_title('Hobbies Distribution',fontsize=15,color='blue')
axes[0,1].set_xlabel('Percentage',fontsize=15,color='blue')
axes[0,1].set_ylabel(None,color='blue')
sns.barplot(x=Hobbies_pct,y=Hobbies_pct.index,ax=axes[0,1]);

axes[0,2].set_title('Top 5 Choices for Cars',fontsize=15,color='blue')
axes[0,2].set_xlabel('Auto Model',fontsize=12,color='blue')
axes[0,2].set_ylabel('Count',fontsize=12,color='blue')
sns.barplot(x=Auto_model.index,y=Auto_model,ax=axes[0,2],alpha=0.5)

axes[1,0].hist(data.age,color='red',alpha=0.5);
axes[1,0].set_title('Age Distribution',fontsize=15,color='blue')
axes[1,0].set_xlabel('Age',fontsize=15,color='blue')
axes[1,0].set_ylabel('Number of People',fontsize=15,color='blue')

axes[1,1].set_title('Profession Distribution',fontsize=15,color='blue')
axes[1,1].set_xlabel('Percentage',fontsize=15,color='blue')
sns.barplot(y=Profession_pct.index,x=Profession_pct,ax=axes[1,1]);

axes[1,2].set_title('Months As Customer',fontsize=15,color='blue')
axes[1,2].pie(Months_as_customer.value_counts(),labels=Months_as_customer.value_counts().index,autopct='%1.1f%%',startangle=180);

1.More than half of the total people insured in the 3 states combined are Females.
2.Among the insured people, reading is the most preferred hobby followed by exercise. Together Accounting for more than 10%.
3.The Car, Ram, an suv is the most preferred car model among the insured people.
4.The mean age of all the insured people is 39 years. Most people fall in the age interval of 25-40 years.
5.More than 8% of people insured are machine operation ispector.
6.More than 47% of the insured people have been a customer for more than 150 months but less than 300 months.
# #  NUMBER OF MALE & FEMALE INSURED STATEWISE

# In[34]:


insurance_state = pd.crosstab(data.policy_state,data.insured_sex)
insurance_state.plot(kind='bar',grid=False)
plt.xticks(rotation=0,fontsize=12)
plt.xlabel('State',fontsize=12,color='blue')
plt.ylabel('Number of People',fontsize=12,color='blue')
plt.legend(fontsize=10)
plt.title('Number of Male & Female insured Statewise',fontsize=14,color='blue');


# Across all the 3 states, More Females have been insured compared to the Males.

# #  NUMBER OF ACCIDENTS ACROSS CITIES OCCURED AT DIFFERENT HOUR OF THE DAY

# In[35]:


State_report = pd.crosstab(data.incident_city,data.incident_hour_of_the_day)
plt.figure(figsize=(9,6))
sns.heatmap(State_report,fmt="d", annot=True, cmap='YlGnBu',linecolor='black',linewidths=.5)
plt.title('Number of Accidents',fontsize=15,color='blue')
plt.xlabel('Incident Hour of the Day', fontsize=15,color='blue')
plt.ylabel('Incident City', fontsize=15,color='blue');


# In[36]:


data.incident_hour_of_the_day.describe()


# In[37]:


plt.figure(figsize=(12,6))
plt.grid(False)
plt.title('Number of Accidents Hourly Distribution',color='blue',fontsize=14)
plt.xlabel('Incident Hour of the Day',fontsize=12,color='blue')
plt.ylabel(None,color='blue',fontsize=12);
sns.countplot(x=data.incident_hour_of_the_day,color='pink');


# In[38]:


Vehicles_involved = data.number_of_vehicles_involved.value_counts()


# In[39]:


Type_of_collision = data.collision_type.value_counts()


# In[40]:


Incident_Type = data.incident_type.value_counts()*100/data.incident_type.count()


# In[41]:


Incident_Severity =data.incident_severity.value_counts()*100/data.incident_severity.count()


# In[42]:


fig,axes = plt.subplots(1,2,figsize=(14,6))
plt.tight_layout(pad=8)

axes[0].set_title('Type of Accident',fontsize=15,color='blue')
Incident_Type.plot(kind='bar',ax=axes[0],grid=False)
xlabels=Incident_Type.index
axes[0].set_xticklabels(xlabels, rotation=15);
axes[0].set_ylabel('% of Total Accidents',fontsize=12,color='blue')

axes[1].set_title('Severity of Accident',fontsize=15,color='blue')
Incident_Severity.plot(kind='bar',ax=axes[1],grid=False);
xlabels=Incident_Severity.index
axes[1].set_xticklabels(xlabels, rotation=15)
axes[1].set_ylabel('% of Total Accidents',fontsize=12,color='blue');


# In[43]:


fig,axes = plt.subplots(1,2,figsize=(14,6))
plt.tight_layout(pad=8)

axes[0].set_title('Number of Vehicles Involved in Accident',fontsize=15,color='blue')
axes[0].pie(Vehicles_involved,labels=Vehicles_involved.index,autopct='%1.1f%%',startangle=180)

axes[1].set_title('Type of Collision',fontsize=15,color='blue')
axes[1].pie(Type_of_collision,labels=Type_of_collision.index,autopct='%1.1f%%',startangle=180);


# # CONCLUSION
1.More than half of the total people insured in the 3 states combined are Females.
2.Among the insured people, reading is the most preferred hobby followed by exercise. Together Accounting for more than 10%.
3.The Car, Ram, an suv is the most preferred car model among the insured people.
4.The mean age of all the insured people is 39 years. Most people fall in the age interval of 25-40 years.
5.More than 8% of people insured are machine operation ispector.
6.More than 47% of the insured people have been a customer for more than 150 months but less than 300 months.
7.Across all the 3 states, More Females have been insured compared to the Males.
8.The mean age of Male is greater than Female in every state. Illinois is the only state where the mean annual premium for male 9.is less than the mean annual premium of a female.
10.The Mean total claim amount in all 3 states is more than 50,000 Dollars. Mean Claim amount is higher for Females compared to the men.
11.Even though more than half of the people insured are females, male have been customer for higher number of months.
12.The number of witnesses doesnot affect the total claim amount in the car insurance settlement.
13.The claim settlement is minimum for city SpringField, where the difference between the total claim amount and total annual premium collection is the highest.
14.In case of a major damage, people are seen to be contacting the Fire Department authorities which may be due to fire post accident or as a precuationary measure. For other minor damages or total loss people have the tendency to contact the police.
The most preferred vehicle among the insured people is Ford Ram (An SUV) which is also the vehicle which has been involved in most number of accidents in the all states combined.
15.Females are more reluctant to report the accident