import streamlit as st
from annotated_text import annotated_text
import user_input_list as ui
import datetime

def display_header():
    
    # Header with annotated text for a visually appealing introduction
    st.write("## CrowdfundProphet: Your Crowdfunding Predictor App :chart_with_upwards_trend:")

    annotated_text(
    "Welcome to the",
    ("Crowdfunding Likelihood Predictor", "Machine Learning Based App", "black"),
    ". This ",
    ("tool", "Proof of Concept", "orange"),
    " helps you gauge the ",
    ("probability of success", "chances", "green"),
    " of your crowdfunding campaign. Just input your business details, and let's ",
    ("predict!", "binary classification", "red"),
    "\n\n",    
    )

    
    # Display copyright, name, and GitHub link 
    st.markdown("""
        <p style='text-align: left;'>
            © Aditya Prakash Singh
            <a href="https://github.com/apsinghAnalytics/CrowdFundProphetApp" target="_blank">
                <img src="https://simpleicons.org/icons/github.svg" alt="GitHub" style="height:24px; display:inline-block; vertical-align: middle;">
            </a>
        </p>
        """, unsafe_allow_html=True)

  
def generate_selections(special_cat_columns, categorical_columns):
    

    special_cat_inputs = {}
    for col in special_cat_columns:
        if col == 'IntermediaryName':
            selected_Intermediary = st.selectbox(
                "Crowdfunding Platform?", list(ui.intermediary_dict.keys()), index=65)  # index is set to NextSeed for default
            special_cat_inputs['IntermediaryFreq'] = ui.intermediary_dict[selected_Intermediary]['IntermediaryFreq']
            special_cat_inputs['avgTargetOfferingByIntermediary'] = ui.intermediary_dict[selected_Intermediary]['avgTargetOfferingByIntermediary']

        elif col == 'stateOrCountryName':
            selected_stateOrCountryName = st.selectbox(
                "In which US state or Country is your business based?", list(ui.stateOrCountry_dict.keys()), index=43)  # index is set to Texas for default
            special_cat_inputs['avgTargetOfferingByStateOrCountry'] = ui.stateOrCountry_dict[selected_stateOrCountryName]['avgTargetOfferingByStateOrCountry']

    categorical_inputs = {}
    for col in categorical_columns:
        # This uses the categorical input selected from the selection box to creates a column name similar to that by one-hot encoding
        
        prefix = col + '_'        
        input_df_cols = [prefix + item for item in ui.ui_cat_dict[col]] 
        selected_df_col = prefix + st.selectbox(ui.column_descriptions[col], ui.ui_cat_dict[col], index= ui.ui_cat_indexes[col])
        
        for column in input_df_cols:
            categorical_inputs[column] = 1 if column == selected_df_col else 0

    return special_cat_inputs, categorical_inputs


def generate_numerical_inputs(numerical_columns, categorical_inputs):    
    
    numerical_inputs = {}
    today = datetime.date.today()

    for col in numerical_columns:
        min_value = ui.ui_num_dict[col][0]
        max_value = ui.ui_num_dict[col][1]
        default_value = ui.ui_num_dict[col][2]

        if col == 'companyAge':
            founding_date = st.date_input(f"{ui.column_descriptions[col]}", min_value=min_value, max_value=max_value, value=default_value)
            numerical_inputs[col] = (today - founding_date).days

        elif col == 'campaignDuration':
            deadline_date = st.date_input(f"{ui.column_descriptions[col]}", min_value=min_value, max_value=max_value, value=default_value)
            numerical_inputs[col] = (deadline_date - today).days

        elif col in ['totalAssetMostRecentFiscalYear', 'initialTargetOffering']:
            numerical_inputs[col] = st.number_input(f"{ui.column_descriptions[col]} Enter value between {min_value} and {max_value} USD", min_value, max_value, default_value)

        elif col == 'maximumOfferingAmount':
            min_value = numerical_inputs['initialTargetOffering']
            if categorical_inputs['oversubscriptionAccepted_N'] == 1:
                max_value = default_value = min_value
            numerical_inputs[col] = st.number_input(f"{ui.column_descriptions[col]}", min_value, max_value, default_value)

        elif col == 'cashEqMostRecentFiscalYear':
            max_value = numerical_inputs['totalAssetMostRecentFiscalYear']
            numerical_inputs[col] = st.number_input(f"{ui.column_descriptions[col]}", min_value, max_value, default_value)

        else:
            numerical_inputs[col] = st.number_input(f"{ui.column_descriptions[col]}", min_value, max_value, default_value)

    return numerical_inputs
