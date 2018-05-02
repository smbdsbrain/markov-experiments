import logging

import markovify
import os
from invoke import task

logging.basicConfig(level=logging.INFO)


@task
def train_model(ctx):
    from utils.train_model import run
    run(ctx.config)


@task
def ficbook_parser(ctx):
    from utils.ficbook_parser import run
    run()

@task
def lurkmore_parser(ctx):
    from utils.lurkmore_parser import run
    run()


@task(default=True)
def start_bot(ctx):
    from utils.bot import run
    run(ctx.config)


@task()
def combine_all_files(ctx):
    state_size = ctx.config.get('state_size', 2)
    files = os.listdir(path="texts")

    with open("output_corpus.txt", 'w') as f:
        f.write('\n')

    files = files[1:-1]

    for file in files:
        with open(f"texts/{file}") as input_file:
            text = input_file.read()
            try:
                markovify.Text(text, state_size=state_size)
                with open("output_corpus.txt", "a") as output_corpus:
                    output_corpus.write('\n' + text)
                logging.info('Added...')
            except Exception as e:
                logging.error(e)