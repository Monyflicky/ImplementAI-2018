#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 10:01:19 2018

@author: jackattack
"""
import plac
import random
from pathlib import Path
import spacy

def IndexBegEnd(s1: str, s2:str) -> list:
    n = len(s1)
    m = len(s2)
    if n > m:
        b = s1.find(s2)
        e = b+m+1
        l = [b, e]
        return l
    else:
        return []


myName = ingrList[i]
   
LABEL = 'FOOD'

TRAIN_DATA = [
    ('5 white onions, peeled and chopped', {
        'entities': [(IndexBegEnd('5 white onions, peeled and chopped', 'onions')[0], IndexBegEnd('5 white onions, peeled and chopped', 'onions')[1], 'FOOD')]
    }),
    ('A large enough quantity of tomatoes', {
        'entities': [(IndexBegEnd('A large enough quantity of tomatoes', 'tomatoes')[0], IndexBegEnd('A large enough quantity of tomatoes', 'tomatoes')[1], 'FOOD')]
    }),
    ('myRandomSentence()', {
        'entities': []
    }),
    ('peppers!', {
        'entities': [(IndexBegEnd('peppers!', 'peppers')[0], IndexBegEnd('peppers!', 'peppers')[1], 'FOOD')]
    }),

    ('myRandomSentence', {
        'entities': []
    }),
    
    ('3 cloves of garlic, minced', {
        'entities': [(IndexBegEnd('3 cloves of garlic, minced', 'garlic')[0], IndexBegEnd('3 cloves of garlic, minced', 'garlic')[1], 'FOOD')]
    }),
    
    ('2 pounds uncooked shrimp, peeled and deveined', {
        'entities': [(IndexBegEnd('2 pounds uncooked shrimp, peeled and deveined', 'shrimp')[0], IndexBegEnd('2 pounds uncooked shrimp, peeled and deveined', 'shrimp')[1], 'FOOD')]
    }),
    
    ('1 small bunch fresh basil, finely chopped', {
        'entities': [(IndexBegEnd('1 small bunch fresh basil, finely chopped', 'basil')[0], IndexBegEnd('1 small bunch fresh basil, finely chopped', 'basil')[1], 'FOOD')]
    }),
    
    ('1 small bunch fresh basil, finely chopped', {
        'entities': [(IndexBegEnd('1 small bunch fresh basil, finely chopped', 'basil')[0], IndexBegEnd('1 small bunch fresh basil, finely chopped', 'basil')[1], 'FOOD')]
    }),
    
    ('6 ears corn, husked and cleaned', {
        'entities': [(IndexBegEnd('6 ears corn, husked and cleaned', 'corn')[0], IndexBegEnd('6 ears corn, husked and cleaned', 'corn')[1], 'FOOD')]
    }),
     
   ]

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, new_model_name='animal', output_dir=None, n_iter=25):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')

    ner.add_label(LABEL)   # add new entity label to entity recognizer
    if model is None:
        optimizer = nlp.begin_training()
    else:
        # Note that 'begin_training' initializes the models, so it'll zero out
        # existing entity types.
        optimizer = nlp.entity.create_optimizer()

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            print(losses)

    # test the trained model
    test_text = 'Caramelized onions with sauce'
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc2 = nlp2(test_text)
        for ent in doc2.ents:
            print(ent.label_, ent.text)


if __name__ == '__main__':
    plac.call(main)
