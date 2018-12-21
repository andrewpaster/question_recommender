from flask import Flask
from flask import request
import spacy
import pandas as pd
import json


df = pd.read_csv('stress_management_mturk.csv')

# replace missing value
df.loc[df.index == 12, 'Stress3Ex'] = 'None given'


# put the stressors, examples, and strategies into separate dataframes
stresses = pd.concat([df['Stress1'], df['Stress2'], df['Stress3']], axis=0).reset_index(drop=True)
examples = pd.concat([df['Stress1Ex'], df['Stress2Ex'], df['Stress3Ex']], axis=0).reset_index(drop=True)
strategy = pd.concat([df['Strategy1'], df['Strategy2'], df['Strategy3']], axis=0).reset_index(drop=True)


# load the spacy model
nlp = spacy.load('en_core_web_md')

# fixes the issue with the spacy library where stop words are not included with the model
for word in nlp.Defaults.stop_words:
    nlp.vocab[word].is_stop = True


def find_similar_phrase(search_phrase, phrases):
    """finds similar phrases in the corpus to this phrase
    
    Args: 
        search_phrase (str): 
        phrases (list): list of strings to compare with the search_phrase
        
    Returns:
        results (list): similarity scores for all documents in the 
    
    """
    results = []
    doc2 = nlp(search_phrase)
    for phrase in phrases:
        doc1 = nlp(phrase)
        results.append(doc1.similarity(doc2)) # stores similarity between the phrase and all other phrases in corpus
        
    return results


# separate short phrases and long phrases
short_phrases = pd.concat([df['Stress1'],
                     df['Stress2'], 
                     df['Stress3']]).reset_index(drop=True)

long_phrases = pd.concat([df['Stress1Ex'],
                     df['Stress2Ex'], 
                     df['Stress3Ex']]).reset_index(drop=True)


app = Flask(__name__)

@app.route('/index', methods=['GET'])
def index():

    result_dict = 'Use GET request to input a phrase ?phrase=Some phrase'

    if request.method == 'GET':
        similar_phrase = request.args.get("phrase")

        # differentiates between longer phrases and shorter phrases
        if len(similar_phrase.split(' ')) < 5:
            results = find_similar_phrase(similar_phrase, short_phrases)
        else:
            results = find_similar_phrase(similar_phrase, long_phrases)

        best_matches = sorted(list(enumerate(results)), key=lambda x:-x[1])[0:5]

        result_dict = dict()

        for i, result in enumerate(best_matches):
            
            record = dict()
            record['strategy'] = strategy[result[0]]
            
            if len(similar_phrase.split(' ')) < 5:
                record['phrase'] = short_phrases[result[0]]
            else:
                record['phrase'] = long_phrases[result[0]]
        
            result_dict[i] = record
	
    return json.dumps(result_dict)

if __name__ == "__main__":
	app.run()
