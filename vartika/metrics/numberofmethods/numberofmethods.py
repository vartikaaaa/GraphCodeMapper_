from typing import Dict, Pattern
from enum import auto
import logging
import re

import coloredlogs # type: ignore

from vartika.analysis import Analysis

# interfaces for inputs
from vartika.abstractresult import AbstractResult, AbstractFileResult, AbstractEntityResult
from vartika.log import Logger

# enums and interface/type of the given metric
from vartika.metrics.abstractmetric import EnumLowerCase
from vartika.metrics.metrics import CodeMetric


LOGGER = Logger(logging.getLogger('metrics'))
coloredlogs.install(level='E', logger=LOGGER.logger(), fmt=Logger.log_format)


class NumberOfMethodsMetric(CodeMetric):

    class Keys(EnumLowerCase):
        NUMBER_OF_METHODS_IN_ENTITY = auto()
        NUMBER_OF_METHODS_IN_FILE = auto()
        AVG_NUMBER_OF_METHODS_IN_ENTITY = auto()
        AVG_NUMBER_OF_METHODS_IN_FILE = auto()

    def __init__(self, analysis: Analysis):
        super().__init__(analysis)

        self.regex_patters = {   #regex_patters: a dictionary of regular expression patterns for different programming languages.
            "JAVA":       r"\b(?!if|for|while|switch|catch)\b[a-zA-Z\d_]+?\s*?\([a-zA-Z\d\s_,\>\<\?\*\.\[\]]*?\)\s*?\{",
            "OBJC":       r"[\-\+]\s*?[a-zA-Z\d_\(\)\:\*\s]+?\s*?\{",
            "JAVASCRIPT": r"(function\s+?)([a-zA-Z\d_\:\*\-\<\>\?\,\[\]\.\s\|\=\$]+?)\(([a-zA-Z\d_\(\)\:\*\s\-\<\>\?\,\[\]\.\|\=\$\/]*?)\)*?[\:]*?\s*?\{",
            "C":          r"\b(?!if|for|while|switch)\b[a-zA-Z\d_]+?\s*?\([a-zA-Z\d\s_,\*]*?\)\s*?\{",
            "CPP":        r"\b(?!if|for|while|switch)\b[a-zA-Z\d\_\:\<\>\*\&]+?\s*?\([\(a-zA-Z\d\s_,\*&:]*?\)\s*?\w+\s*?\{",
            "PY":         r"(def)\s.+(.+):",
        }

        self.compiled_re: Dict[str, Pattern] = {}      #compiled_re: a dictionary of compiled regular expressions for different programming languages.
        self._compile()

    def calculate_from_results(self, results: Dict[str, AbstractResult]):
        self._calculate_local_metric_data(results)
        self._calculate_global_metric_data(results)

    def _compile(self):
        for name, pattern in self.regex_patters.items():
            self.compiled_re[name] = re.compile(pattern)


#Extracts the scanned tokens from each result. Uses the compiled regular expression for the corresponding programming language to find method declarations in the tokens. 
# Counts the number of method declarations found.
# Stores the count in the metrics dictionary of each result.
    def _calculate_local_metric_data(self, results: Dict[str, AbstractResult]):
        for _, result in results.items():
            LOGGER.debug(f'calculating metric {self.pretty_metric_name} for result {result.unique_name}')

            find_method_expression = self.__get_expression(result)

            LOGGER.debug(f'extracting methods from result {result.scanned_file_name}')
            full_string = " ".join(result.scanned_tokens)
            number_of_methods = len(find_method_expression.findall(full_string))

            if isinstance(result, AbstractFileResult):
                result.metrics[self.Keys.NUMBER_OF_METHODS_IN_FILE.value] = number_of_methods
                self.local_data[result.unique_name] = {self.Keys.NUMBER_OF_METHODS_IN_FILE.value: number_of_methods}

            if isinstance(result, AbstractEntityResult):
                result.metrics[self.Keys.NUMBER_OF_METHODS_IN_ENTITY.value] = number_of_methods
                self.local_data[result.unique_name] = {self.Keys.NUMBER_OF_METHODS_IN_ENTITY.value: number_of_methods}

            LOGGER.debug(f'calculation done, updated metric data of {result.unique_name}: {result.metrics=}')

#This method calculates the average number of methods per file and per entity in the codebase. It does the following: 
# Filters the results to only include file results and entity results.
# Calculates the total number of methods and the total number of files or entities.
# Calculates the average number of methods per file or entity.
# Stores the average in the overall_data dictionary.
    def _calculate_global_metric_data(self, results: Dict[str, AbstractResult]):
        LOGGER.debug(f'calculating average method count {self.metric_name}...')

        entity_results = {k: v for (k, v) in results.items() if isinstance(v, AbstractEntityResult)}
        file_results = {k: v for (k, v) in results.items() if isinstance(v, AbstractFileResult)}

        if len(file_results) > 0:
            total_method_count, total_files = 0, 0
            for _, file_result in file_results.items():
                total_files += 1
                total_method_count += file_result.metrics[self.Keys.NUMBER_OF_METHODS_IN_FILE.value]

            average_methods_in_file = total_method_count / total_files
            self.overall_data[self.Keys.AVG_NUMBER_OF_METHODS_IN_FILE.value] = average_methods_in_file
            LOGGER.debug(f'average method count per file: {average_methods_in_file}')

        if len(entity_results) > 0:
            total_method_count, total_entities = 0, 0
            for _, entity_result in entity_results.items():
                total_entities += 1
                total_method_count += entity_result.metrics[self.Keys.NUMBER_OF_METHODS_IN_ENTITY.value]

            average_methods_in_entity = total_method_count / total_entities
            self.overall_data[self.Keys.AVG_NUMBER_OF_METHODS_IN_ENTITY.value] = average_methods_in_entity
            LOGGER.debug(f'average method count per entity: {average_methods_in_entity}')

    def __get_expression(self, result: AbstractResult) -> Pattern:
        return self.compiled_re[result.scanned_language.name]
