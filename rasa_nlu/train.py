from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import argparse
import logging
import os

import typing
from typing import Text
from typing import Tuple

from rasa_nlu.components import ComponentBuilder
from rasa_nlu.converters import load_data
from rasa_nlu.model import Trainer

from rasa_nlu.config import RasaNLUConfig
from typing import Optional


if typing.TYPE_CHECKING:
    from rasa_nlu.persistor import Persistor


def create_argparser():
    parser = argparse.ArgumentParser(description='train a custom language parser')

    parser.add_argument('-p', '--pipeline', default=None,
                        help='pipeline to use for the message processing.')
    parser.add_argument('-o', '--output', default=None, help="path where model files will be saved")
    parser.add_argument('-d', '--data', default=None, help="file containing training data")
    parser.add_argument('-c', '--config', required=True, help="config file")
    parser.add_argument('-l', '--language', default=None, choices=['de', 'en'], help="model and data language")
    parser.add_argument('-t', '--num_threads', default=1, type=int,
                        help="number of threads to use during model training")
    parser.add_argument('-m', '--mitie_file', default=None,
                        help='file with mitie total_word_feature_extractor')
    return parser


def create_persistor(config):
    # type: (RasaNLUConfig) -> Optional[Persistor]
    """Create a remote persistor to store the model if the configuration requests it."""

    persistor = None
    if "bucket_name" in config:
        from rasa_nlu.persistor import Persistor
        persistor = Persistor(config['path'], config['aws_region'], config['bucket_name'])

    return persistor


def init():
    # type: () -> RasaNLUConfig
    """Combines passed arguments to create rasa NLU config."""

    parser = create_argparser()
    args = parser.parse_args()
    config = RasaNLUConfig(args.config, os.environ, vars(args))
    return config


def do_train(config, component_builder=None):
    # type: (RasaNLUConfig, Optional[ComponentBuilder]) -> Tuple[Trainer, Text]
    """Loads the trainer and the data and runs the training of the specified model."""

    trainer = Trainer(config, component_builder)
    persistor = create_persistor(config)
    training_data = load_data(config['data'])
    trainer.validate()
    trainer.train(training_data)
    persisted_path = trainer.persist(config['path'], persistor)
    return trainer, persisted_path


if __name__ == '__main__':

    config = init()
    logging.basicConfig(level=config['log_level'])

    do_train(config)
    logging.info("done")
