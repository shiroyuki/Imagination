import logging
from logging import Logger
from unittest import TestCase

from imagination.assembler.handlers import AbstractContainerCreator, EntityCreator, FactorizationCreator, LambdaCreator
from imagination.debug import LoggerFactory


class LoggerFactoryTest(TestCase):
    """ This test case is just to run the logger to verify that the loggers are working as designed. """

    def setUp(self):
        self.lf = LoggerFactory().instance()

    def test_minimal_logger(self):
        logger = self.lf.get_for_type(AbstractContainerCreator, level=logging.INFO, mode='minimal')
        self.assertTrue(isinstance(logger, Logger))
        self.assertEqual(logger.name, 'i.a.h.AbstractContainerCreator')

    def test_compact_logger(self):
        logger = self.lf.get_for_type(EntityCreator, level=logging.INFO, mode='compact')
        self.assertTrue(isinstance(logger, Logger))
        self.assertEqual(logger.name, 'i.a.h.EntityCreator')

    def test_full_logger(self):
        logger = self.lf.get_for_type(FactorizationCreator, level=logging.INFO, mode='full')
        self.assertTrue(isinstance(logger, Logger))
        self.assertEqual(logger.name, 'imagination.assembler.handlers.FactorizationCreator')

    def test_json_logger(self):
        logger = self.lf.get_for_type(LambdaCreator, level=logging.INFO, mode='json')
        self.assertTrue(isinstance(logger, Logger))
        self.assertEqual(logger.name, 'imagination.assembler.handlers.LambdaCreator')
        logger.info('From the JSON logger')

