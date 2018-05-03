import logging
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
    import markovify

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


@task()
def train_lstm(ctx):
    from keras.callbacks import ModelCheckpoint

    from utils.lstm_utils import define_model, get_dataset, get_text

    corpus_name = ctx.config.get('corpus_name', 'output_corpus.txt')
    raw_text = get_text(corpus_name)
    data = get_dataset(raw_text)
    model = define_model(data)

    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=0, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    # fit the model
    model.fit(data['input'], data['output'], nb_epoch=200, batch_size=64, callbacks=callbacks_list)

@task()
def get_sentence_lstm(ctx):
    import numpy
    from utils.lstm_utils import define_model, get_dataset, get_input_output, get_text

    filename = ctx.config.get('weight_file', 'weights')
    corpus_name = ctx.config.get('corpus_name', 'output_corpus.txt')
    raw_text = get_text(corpus_name)
    data = get_dataset(raw_text)
    model = define_model(data)

    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    chars = sorted(list(set(raw_text)))
    char_to_int = dict((char, number) for number, char in enumerate(chars))
    int_to_char = dict((i, c) for i, c in enumerate(chars))

    n_chars = len(raw_text)
    n_vocab = len(chars)

    # prepare the dataset of input to output pairs encoded as integers
    sequence_length = 100

    input, output = get_input_output(raw_text, n_chars, char_to_int, sequence_length)

    start = numpy.random.randint(0, len(input) - 1)
    pattern = input[start]

    iterations = int(ctx.config.get('iterations', 200))

    for i in range(iterations):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_char[index]
        seq_in = [int_to_char[value] for value in pattern]
        print(result)
        # sys.stdout.write(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]


    print("\nDone.")
