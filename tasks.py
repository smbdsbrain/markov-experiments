import logging

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
