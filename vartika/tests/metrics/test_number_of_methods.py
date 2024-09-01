"""
All unit tests that are related to the number of methods metric.
"""

# Authors: Grzegorz Lato <grzegorz.lato@gmail.com>
# License: MIT

import unittest
from typing import Dict
import logging
import coloredlogs

from tests.testdata.c import C_TEST_FILES
from tests.testdata.cpp import CPP_TEST_FILES
from tests.testdata.groovy import GROOVY_TEST_FILES
from tests.testdata.java import JAVA_TEST_FILES
from tests.testdata.javascript import JAVASCRIPT_TEST_FILES
from tests.testdata.typescript import TYPESCRIPT_TEST_FILES
from tests.testdata.kotlin import KOTLIN_TEST_FILES
from tests.testdata.objc import OBJC_TEST_FILES
from tests.testdata.ruby import RUBY_TEST_FILES
from tests.testdata.swift import SWIFT_TEST_FILES
from tests.testdata.py import PYTHON_TEST_FILES
from tests.testdata.go import GO_TEST_FILES

from vartika.languages.cparser import CParser
from vartika.languages.cppparser import CPPParser
from vartika.languages.javaparser import JavaParser
from vartika.languages.javascriptparser import JavaScriptParser
from vartika.languages.objcparser import ObjCParser
from vartika.languages.pyparser import PythonParser
from vartika.languages.abstractparser import AbstractParser

from vartika.analysis import Analysis
from vartika.analyzer import Analyzer
from vartika.metrics.noofmethods.noofmethods import NumberOfMethodsMetric
from vartika.results import FileResult

LOGGER = logging.getLogger('TESTS')
coloredlogs.install(level='INFO', logger=LOGGER, fmt='\n%(asctime)s %(name)s %(levelname)s %(message)s')


class NumberOfMethodsTestCase(unittest.TestCase):

    def setUp(self):

        self.test_data: Dict[str, Dict[str, str]] = {
            CParser.parser_name(): C_TEST_FILES,
            CPPParser.parser_name(): CPP_TEST_FILES,
            JavaParser.parser_name(): JAVA_TEST_FILES,
            JavaScriptParser.parser_name(): JAVASCRIPT_TEST_FILES,
            ObjCParser.parser_name(): OBJC_TEST_FILES,
            PythonParser.parser_name(): PYTHON_TEST_FILES,
        }

        self.parsers: Dict[str, AbstractParser] = {
            CParser.parser_name(): CParser(),
            CPPParser.parser_name(): CPPParser(),
            JavaParser.parser_name(): JavaParser(),
            JavaScriptParser.parser_name(): JavaScriptParser(),
            ObjCParser.parser_name(): ObjCParser(),
            PythonParser.parser_name(): PythonParser(),
        }

        self.analysis = Analysis()
        self.analyzer = Analyzer(None, self.parsers)
        self.analysis.analysis_name = "test"
        self.analysis.source_directory = "/source"

        self.number_of_methods_metric = NumberOfMethodsMetric(self.analysis)

    def tearDown(self):
        pass

    def test_number_of_methods_for_file_results(self):
        """Generate file results for all parsers and check if metrics could be calculated."""
        results: Dict[str, FileResult] = {}

        for parser_name, test_data_dict in self.test_data.items():
            for file_name, file_content in test_data_dict.items():
                self.parsers[parser_name].generate_file_result_from_analysis(
                    self.analysis, file_name=file_name, full_file_path="/source/tests/" + file_name, file_content=file_content)

                self.assertTrue(bool(self.parsers[parser_name].results))
                results.update(self.parsers[parser_name].results)
                self.analysis.collect_results_from_parser(self.parsers[parser_name])

        self.assertTrue(bool(results))
        self.assertTrue(bool(self.analysis.file_results))
        self.assertFalse(bool(self.analysis.entity_results))

        for _, result in results.items():
            self.assertFalse(bool(result.metrics))

        self.assertTrue(bool(self.number_of_methods_metric.metric_name))
        self.analysis.metrics_for_file_results.update({
            self.number_of_methods_metric.metric_name: self.number_of_methods_metric
        })

        self.assertTrue(bool(self.analysis.contains_code_metrics))
        self.assertFalse(bool(self.analysis.contains_graph_metrics))

        self.assertFalse(self.analysis.local_metric_results)
        self.assertFalse(self.analysis.overall_metric_results)
        self.analyzer._calculate_code_metric_results(self.analysis)
        self.assertTrue(self.analysis.local_metric_results)
        self.assertTrue(self.analysis.overall_metric_results)

    def test_number_of_methods_for_entity_results(self):
        """Generate entity results for all parsers and check if metrics could be calculated."""
        results: Dict[str, FileResult] = {}

        for parser_name, test_data_dict in self.test_data.items():
            for file_name, file_content in test_data_dict.items():
                self.parsers[parser_name].generate_file_result_from_analysis(self.analysis, file_name=file_name, full_file_path="/tests/" + file_name, file_content=file_content)

                self.assertTrue(bool(self.parsers[parser_name].results))
                results.update(self.parsers[parser_name].results)
                self.analysis.collect_results_from_parser(self.parsers[parser_name])

        self.assertFalse(self.analysis.entity_results)

        for _, parser in self.parsers.items():
            try:
                parser.generate_entity_results_from_analysis(self.analysis)
                self.analysis.collect_results_from_parser(parser)
            except NotImplementedError:
                continue

        self.assertTrue(self.analysis.entity_results)

        self.assertTrue(bool(self.number_of_methods_metric.metric_name))
        self.analysis.metrics_for_file_results.update({
            self.number_of_methods_metric.metric_name: self.number_of_methods_metric
        })

        self.assertFalse(self.analysis.local_metric_results)
        self.assertFalse(self.analysis.overall_metric_results)
        self.analyzer._calculate_code_metric_results(self.analysis)
        self.assertTrue(self.analysis.local_metric_results)
        self.assertTrue(self.analysis.overall_metric_results)
