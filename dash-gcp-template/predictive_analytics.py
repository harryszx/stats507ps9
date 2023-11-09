#!/usr/bin/env python
# coding: utf-8
# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
import joblib

# Load data
df = pd.read_csv('us_chronic_disease_indicators.csv')

# Preprocess and train model
def train_and_save_model(df):
    # Filter the DataFrame
    df_filtered = df[(df['question'] == 'Mortality from heart failure') &
                     (df['datavaluetypeid'] == 'NMBR')]
    
    # Prepare the features and labels
    X = df_filtered[['locationabbr', 'yearstart', 'stratificationcategoryid1', 'stratificationid1']]
    y = df_filtered['datavalue']
    
    # Split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create a pipeline with one-hot encoding and a regression model
    categorical_features = ['locationabbr', 'stratificationcategoryid1', 'stratificationid1']
    ohe = OneHotEncoder(handle_unknown='ignore')
    regressor = LinearRegression()
    pipeline = make_pipeline(
        make_column_transformer((ohe, categorical_features), remainder='passthrough'),
        regressor
    )
    
    # Train the model
    pipeline.fit(X_train, y_train)
    
    # Save the model
    joblib.dump(pipeline, 'mortality_from_heart_failure_model.pkl')

# Function to load the model and make predictions
def predict(datavalue, locationabbr, race, gender):
    # Load the model
    model = joblib.load('mortality_from_heart_failure_model.pkl')
    
    # Create DataFrame from the inputs
    input_df = pd.DataFrame([[locationabbr, datavalue, race, gender]], 
                            columns=['locationabbr', 'yearstart', 'stratificationcategoryid1', 'stratificationid1'])
    
    # Make prediction
    return model.predict(input_df)

# Call the training function
train_and_save_model(df)


# %%




