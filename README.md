# Question Recommender

This app uses survey data where people were asked to name a stressor and then give suggestions for how they cope with the stressor. When you input a new stressor, the code finds the five closest matching stressors and then outputs the coping mechanisms. Closeness is defined by the angle between word embeddings.

# TODO: Finish installation instructions

## Requirements
* pandas
* spacy

## Instructions

pip install pandas
pip install spacy

python -m spacy download en_core_web_lg
