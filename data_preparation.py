"""
Data Preparation Module for Starbucks Capstone Challenge

This module contains functions for loading and preprocessing the Starbucks datasets.
Functions include loading the data, cleaning the profile and transcript datasets,
merging the datasets, and segmenting users based on age. 

This module allows the preparation of datasets to be used in modeling and analysis 
phases of the Starbucks Capstone Challenge.

Example:
    portfolio, profile, merged_data = preprocess_data()

Attributes:
    DATA_PATH (str): The directory path where the dataset files are located.

Functions:
    load_data: Load the datasets from the specified paths.
    clean_data: Clean the profile and transcript datasets.
    merge_data: Merge the datasets to create a comprehensive dataframe.
    segment_data: Segment the users in the merged dataset based on age.
    preprocess_data: Process the data and merge the datasets.
"""

import pandas as pd

DATA_PATH = "/Users/luca/Documents/Udacity - all learning materials/Capstone Project - Starbuck/Data/"

def load_data():
    """Load the datasets from the specified paths.
    
    Returns:
        tuple: Three dataframes for portfolio, profile, and transcript.
    """
    portfolio = pd.read_json(DATA_PATH + 'portfolio.json', orient='records', lines=True)
    profile = pd.read_json(DATA_PATH + 'profile.json', orient='records', lines=True)
    transcript = pd.read_json(DATA_PATH + 'transcript.json', orient='records', lines=True)
    return portfolio, profile, transcript

def clean_data(profile, transcript):
    """Clean the profile and transcript datasets.
    
    Args:
        profile (DataFrame): The profile dataset.
        transcript (DataFrame): The transcript dataset.
        
    Returns:
        tuple: Two cleaned dataframes for profile and transcript.
    """
    profile_cleaned = profile[profile['age'] != 118]
    transcript['offer_id'] = transcript['value'].apply(lambda x: x.get('offer id') or x.get('offer_id'))
    transcript['transaction_amount'] = transcript['value'].apply(lambda x: x.get('amount', 0))
    transcript_cleaned = transcript.drop(columns='value')
    return profile_cleaned, transcript_cleaned

def merge_data(transcript_cleaned, profile_cleaned, portfolio):
    """Merge the datasets to create a comprehensive dataframe.
    
    Args:
        transcript_cleaned (DataFrame): The cleaned transcript dataset.
        profile_cleaned (DataFrame): The cleaned profile dataset.
        portfolio (DataFrame): The portfolio dataset.
        
    Returns:
        DataFrame: The merged dataframe.
    """
    merged_data = pd.merge(transcript_cleaned, profile_cleaned, left_on='person', right_on='id', how='inner')
    merged_data = pd.merge(merged_data, portfolio, left_on='offer_id', right_on='id', how='left')
    return merged_data

def segment_data(merged_data):
    """Segment the users in the merged dataset based on age.
    
    Args:
        merged_data (DataFrame): The merged dataset.
        
    Returns:
        DataFrame: The dataset with an additional column for age segments.
    """
    bins = [18, 35, 60, 100]
    labels = ['Young', 'Middle-aged', 'Senior']
    merged_data['age_group'] = pd.cut(merged_data['age'], bins=bins, labels=labels, right=False)
    return merged_data


def preprocess_data(portfolio, profile, transcript):
    """Process the data and merge the datasets.
    
    Args:
        portfolio (DataFrame): The portfolio dataset.
        profile (DataFrame): The profile dataset.
        transcript (DataFrame): The transcript dataset.
        
    Returns:
        DataFrame: The merged and processed dataset.
    """
    # Clean the data
    profile_cleaned, transcript_cleaned = clean_data(profile, transcript)
    
    # Merge the datasets
    merged_data = merge_data(transcript_cleaned, profile_cleaned, portfolio)
    
    # Segment the data
    merged_data = segment_data(merged_data)
    
    return merged_data





    