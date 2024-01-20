import streamlit as st
import pandas as pd
from PIL import Image

import backend_functions as b
import mlModel as ml

st.set_page_config(page_title="CrowdfundProphet", page_icon='crystalball.png', layout="wide")

# Define numerical and categorical columns
numerical_columns = ['companyAge', 'campaignDuration' , 'initialTargetOffering', 'maximumOfferingAmount'
                     , 'totalAssetMostRecentFiscalYear', 'cashEqMostRecentFiscalYear', 'netIncomeMostRecentFiscalYear']
special_cat_columns = ['IntermediaryName', 'stateOrCountryName']
categorical_columns = ['quarter', 'securityOfferedType', 'oversubscriptionAccepted', 'legalStatusForm']


def generate_app():
    
    b.display_header() # visually appealing header with annotated texts, including github link           

    # Creating columns with specified ratios for splitting the layout of the screen in the ratio 1:2:2
    col1, col2, col3 = st.columns([1, 2, 2])

    with col1: # The left most division column of the user interface for selection/categorical inputs
        
        st.markdown("#### :gear: Selections")
        # Selections of Platform, State/Country, Fiscal Quarter of the Campaign, Security type, Oversubscriptions Acceptance, and Business Structure
        # Generate categorical inputs in one hot encoded format required for the model from selections
        # Generate special categorical inputs for selection of Platform and State/Country, in which selections are mapped to numerical inputs as required for the ML model        
                
        special_cat_inputs, categorical_inputs= b.generate_selections(special_cat_columns, categorical_columns)

        
    with col2: # the middle column of the user interface for number and date inputs
         
        st.markdown("#### :abacus: Numbers")

        # Date inputs like company founding date and campaign deadline as converted to companyAge and campaignDuration, respectively, input formats recognized by the ML model
        # Numerical inputs like the target offering Amount, the maximum offering, the total assets, cash Equivalents, and net income is requested from the user
        numerical_inputs= b.generate_numerical_inputs(numerical_columns, categorical_inputs)
        
            
    with col3: # The right most column where the prediction button is and is where the final prediction result is made by feeding the inputs to the ML model
        st.markdown("#### :crystal_ball: Prediction")
        
        if st.button('Predict Likelihood'):
            # Combine inputs into a DataFrame
            input_data = {**numerical_inputs, **special_cat_inputs, **categorical_inputs}
            input_df = pd.DataFrame([input_data])

            # Feed the input df to the trained ML model to get the probability of campaign success

            probability_class_1 = ml.predictionModel(input_df) * 100 
            if probability_class_1 > 50:
                st.write(f"Congratulations!!! \n \n  You have a shot at crowdfunding success with a probability of {probability_class_1:.2f}%")
                congratulations_image = Image.open('congratulations.png')  # Image for conveying congratulations
                st.image(congratulations_image, use_column_width=True, caption= "generated using DALL·E 3")

            else:
                st.write(f"Sorry :( \n \n  Your chances of getting crowdfunding are low with a probability of {probability_class_1:.0f}%")
                sorry_image = Image.open('sorry.png')  # Image for conveying sorry
                st.image(sorry_image, use_column_width=True, caption= "generated using DALL·E 3")
                
# Run the app
if __name__ == '__main__':
    generate_app()



