import pandas as pd
import datetime

# For companyAge 
today = datetime.date.today()  # Calculate today's date
default_date_age = today - datetime.timedelta(days=368) # Calculate the default date (1 week in the past)
min_date_age = today - datetime.timedelta(days=19353) # Calculate the earliest allowed date (19353 days in the past based on historical campaign data)
max_date_age = today - datetime.timedelta(days=1) # Calculate the earliest allowed date (19353 days in the past)

# For campaignDuration
default_date_duration = today + datetime.timedelta(days=30) # default is 30 days ahead
min_date_duration  = today + datetime.timedelta(days=5) # atleast a 5 day long campaign
max_date_duration  = today + datetime.timedelta(days=1460) # four years ahead

# This dictionary provides the min, maximum, and the average value to display for the slider function in streamlit
ui_num_dict={
'initialTargetOffering': [0, 5000000, 50000],
'maximumOfferingAmount': [0, 5000000, 110000],
'totalAssetMostRecentFiscalYear': [0, 200000000, 300000],
'cashEqMostRecentFiscalYear': [-60000, 50000000, 250000],
'netIncomeMostRecentFiscalYear': [-30000000, 20000000, -1000],
'campaignDuration': [min_date_duration, max_date_duration, default_date_duration],
'companyAge': [min_date_age, max_date_age, default_date_age]
}


#This dictionary provides the lists for the selectbox function (dropdown) in streamlit
ui_cat_dict= {
'quarter':['1Q','2Q','3Q','4Q'],
'securityOfferedType': ['Common Stock', 'Debt', 'Other','Preferred Stock'],
'oversubscriptionAccepted': ['Y','N'],
'legalStatusForm':['Corporation','General Partnership','Limited Liability Company','Limited Partnership','Other']
}

#This sets the default indexes in the select drop down items
ui_cat_indexes= {
'quarter':2, #3Q
'securityOfferedType': 1, #Debt
'oversubscriptionAccepted': 0, #Y
'legalStatusForm':2 #Y
}

# Descriptions for the user input, also contains formatting (orange and bold) 
column_descriptions = {
    'initialTargetOffering': 'What is your **:orange[target offering amount]**? \n \n',
    'maximumOfferingAmount': 'What is the **:orange[maximum amount for oversubscribed offerings]**?  \n \n This must be >= target offering',
    'totalAssetMostRecentFiscalYear': 'What are your **:orange[total assets for the most recent fiscal year]**? \n \n',
    'cashEqMostRecentFiscalYear': 'What is your **:orange[cash equivalents for the most recent fiscal year]** \n \n This must be <= total Assets?',
    'netIncomeMostRecentFiscalYear': 'What is your **:orange[net income for the most recent fiscal year]**?  \n \n Typically <= total Assets?',
    'companyAge': 'When was your **:orange[company founded]**?',
    'campaignDuration': 'When is the **:orange[campaign deadline]**? \n \n',
    'securityOfferedType': 'What are the types of **:orange[securities offered]**?',
    'oversubscriptionAccepted': 'Are you planning to **:orange[accept oversubscriptions]**?',
    'legalStatusForm': 'What is your **:orange[business structure]**?',
    'quarter': 'In which **:orange[fiscal quarter]** are you planning to file your campaign?',
}


# Create a dictionary to map Intermediary/Platform name to 'IntermediaryFreq' and 'avgTargetOfferingByIntermediary', inputs which are recognized by the trained ML modle

excel_file = 'intermediaryFreqMapping.xlsx' # Load the Excel file for Intermediary mapping data from the model built
df = pd.read_excel(excel_file)

# Create the nested dictionary
intermediary_dict = {}
for index, row in df.iterrows():
    intermediary_name = row['IntermediaryName']
    intermediary_dict[intermediary_name] = {
        'IntermediaryFreq': row['IntermediaryFreq'],
        'avgTargetOfferingByIntermediary': row['avgTargetOfferingByIntermediary']
    }

# Create a dictionary to map StateOrCountryName to 'avgTargetOfferingByStateOrCountry', an input which is recognized by the trained ML modle

df_stateCodeFreq = pd.read_excel('stateOrCountryFreqMapping.xlsx') # Load the excel files for the stateCode mapping data from the model built
df_stateCodeToName= pd.read_csv('stateOrCountryCode.csv')

df= pd.merge(df_stateCodeToName[['stateOrCountry','stateOrCountryName']], df_stateCodeFreq , on='stateOrCountry', how='inner')

df.drop(columns=['stateOrCountry'], inplace=True) # drop the column containing the stateOrCountry code, because it is not intuitive like a description

df.loc[len(df)] = ['Other', 0, 0] # Adding a new row with the specified values at the end of the DataFrame


# Create the nested dictionary
stateOrCountry_dict = {}
for index, row in df.iterrows():
    stateOrCountry_name = row['stateOrCountryName']
    
    stateOrCountry_dict[stateOrCountry_name] = {
        'stateOrCountryFreq': row['stateOrCountryFreq'],
        'avgTargetOfferingByStateOrCountry': row['avgTargetOfferingByStateOrCountry']
    }


