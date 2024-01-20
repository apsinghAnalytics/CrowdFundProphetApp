import pickle
import pandas as pd

def predictionModel(df):
    with open('stackedClassifier.pkl', 'rb') as file:
        model = pickle.load(file) #Loading the pickled model

    with open('rscaler.pkl', 'rb') as file: 
       #Loading the same robust scaler used in standardizing the numerical columns of the model developed
       rscaler = pickle.load(file)
           

    numerical_cols= ['companyAge', 'initialTargetOffering', 'maximumOfferingAmount', 
                     'totalAssetMostRecentFiscalYear', 'cashEqMostRecentFiscalYear', 
                     'netIncomeMostRecentFiscalYear', 'campaignDuration', 'IntermediaryFreq',
                       'avgTargetOfferingByIntermediary', 'avgTargetOfferingByStateOrCountry']
    
    columns_order=   ['companyAge', 'initialTargetOffering', 'maximumOfferingAmount', 'totalAssetMostRecentFiscalYear',
        'cashEqMostRecentFiscalYear', 'netIncomeMostRecentFiscalYear', 'campaignDuration', 'IntermediaryFreq',
        'avgTargetOfferingByIntermediary', 'avgTargetOfferingByStateOrCountry', 'quarter_1Q', 'quarter_2Q', 'quarter_3Q', 'quarter_4Q',
        'securityOfferedType_Common Stock', 'securityOfferedType_Debt', 'securityOfferedType_Other', 'securityOfferedType_Preferred Stock',
        'oversubscriptionAccepted_N', 'oversubscriptionAccepted_Y', 'legalStatusForm_Corporation', 'legalStatusForm_General Partnership',
        'legalStatusForm_Limited Liability Company', 'legalStatusForm_Limited Partnership', 'legalStatusForm_Other']
    
    df=df[columns_order] # Ensures that the columns are in the same order as was in the original ML code

    df_Standardized= df.copy()

    df_Standardized[numerical_cols]= rscaler.transform(df[numerical_cols]) #standardizing only the numerical cols

    # Getting the probabilities for each class
    probabilities = model.predict_proba(df_Standardized.head(1))

    # Extracting the probability of the positive class (class 1)
    probability_class_1 = probabilities[0, 1]

    return probability_class_1

    