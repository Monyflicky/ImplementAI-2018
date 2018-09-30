#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 20:46:39 2018

@author: cayman329
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 19:45:17 2018

@author: cayman329
"""

import plac
import random
from pathlib import Path
import spacy


# training data
TRAIN_DATA = [
    ('3 large tomatoes, diced', {
        'entities': [(0, 1, 'NUM'),(8, 16, 'INGR')]
    }),
    ('1 large onion, diced', {
        'entities': [(0, 1, 'NUM'), (8, 13, 'INGR')]
    }),
    ('1/4 cup chopped fresh basil', {
            'entities': [(0, 3, 'NUM'), (24, 29, 'INGR')
    ]}

output_dir=("Output directory for saved HTML", "positional", None, Path))
def main(output_dir=None):
    nlp = English()  # start off with blank English class

    Doc.set_extension('overlap', method=overlap_tokens)
    doc1 = nlp(u"1 onion.")
    doc2 = nlp(u"3 large onions, chopped.")
    print("Text 1:", doc1.text)
    print("Text 2:", doc2.text)
    print("Overlapping tokens:", doc1._.overlap(doc2))

    Doc.set_extension('to_html', method=to_html)
    doc = nlp(u"This is a sentence about Apple.")
    # add entity manually for demo purposes, to make it work without a model
    doc.ents = [Span(doc, 5, 6, label=nlp.vocab.strings['ORG'])]
    print("Text:", doc.text)
    doc._.to_html(output=output_dir, style='ent')


def to_html(doc, output='/tmp', style='dep'):
    """Doc method extension for saving the current state as a displaCy
    visualization.
    """
    # generate filename from first six non-punct tokens
    file_name = '-'.join([w.text for w in doc[:6] if not w.is_punct]) + '.html'
    html = displacy.render(doc, style=style, page=True)  # render markup
    if output is not None:
        output_path = Path(output)
        if not output_path.exists():
            output_path.mkdir()
        output_file = Path(output) / file_name
        output_file.open('w', encoding='utf-8').write(html)  # save to file
        print('Saved HTML to {}'.format(output_file))
    else:
        print(html)


def overlap_tokens(doc, other_doc):
    """Get the tokens from the original Doc that are also in the comparison Doc.
    """
    overlap = []
    other_tokens = [token.text for token in other_doc]
    for token in doc:
        if token.text in other_tokens:
            overlap.append(token)
    return overlap


if __name__ == '__main__':
plac.call(main)

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
        def main(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe('ner')

   



    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
            print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == '__main__':
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]


    



