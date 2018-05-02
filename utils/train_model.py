import logging

import markovify
import os
from multiprocessing import Pool
import multiprocessing as mp

state_size = 3


def run(config):
    # model = markovify.Text('Hello, world!', state_size=3)
    state_size = config.get('state_size', 3)
    p = Pool(config['cpu_count'])

    results = p.map(make_model_from_text, os.listdir(path="../texts"))

    p.close()
    p.join()

    results = [result for result in results if result]
    logging.info('start combining')

    last_model = None
    if len(results) % 2 != 0:
        last_model = results[-1]

    while len(results) > 1:
        p = Pool(config['cpu_count'])

        pairs = zip(results[::2], results[1::2])
        results = p.map(merge_models, pairs)

        p.close()
        p.join()

    if last_model:
        model = markovify.combine(models=[last_model, results[0]])
    else:
        model = results[0]

    logging.info('Saving model...')
    model_json = model.to_json()
    with open(f"../model.json", 'w') as f:
        f.write(model_json)


def make_model_from_text(text_name):
    logging.info(f'Start build chain on {text_name}')
    try:
        with open(f"../texts/{text_name}") as f:
            text = f.read()
        return markovify.Text(text, state_size=state_size)
    except Exception as e:
        logging.error(e)


def merge_models(model_pair):
    logging.info('combine models...')
    return markovify.combine(models=[model_pair[0], model_pair[1]])