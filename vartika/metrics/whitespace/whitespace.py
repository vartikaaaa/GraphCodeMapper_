#This is a Python class that implements a whitespace metric to measure the complexity of whitespace usage in source code
from typing import Dict
from enum import auto

import re
import logging
import coloredlogs # type: ignore

# interfaces for inputs
from vartika.analysis import Analysis
from vartika.abstractresult import AbstractResult
from vartika.log import Logger

# enums and interface/type of the given metric
from vartika.metrics.abstractmetric import EnumLowerCase
from vartika.metrics.metrics import CodeMetric

LOGGER = Logger(logging.getLogger('metrics'))
coloredlogs.install(level='E', logger=LOGGER.logger(), fmt=Logger.log_format)

class WhitespaceMetric(CodeMetric):
    """Provides a code metric based on counting whitespace characters."""

    class Keys(EnumLowerCase):
        WS_COMPLEXITY_IN_FILE = auto()

    def __init__(self, analysis: Analysis):
        super().__init__(analysis)

        self.leading_tabs_expr = re.compile(r'^(\t+)')
        self.leading_spaces_expr = re.compile(r'^( +)')
        self.empty_line_expr = re.compile(r'^\s*$')

    @property
    def pretty_metric_name(self) -> str:
        return 'whitespace metric'
    
    def calculate_from_results(self, results: Dict[str, AbstractResult]):
        for _, result in results.items():
            ws_complexity = sum(self.calculate_complexity_in(result.source))
            result.metrics[self.Keys.WS_COMPLEXITY_IN_FILE.value] = ws_complexity
            self.local_data[result.unique_name] = {self.Keys.WS_COMPLEXITY_IN_FILE.value: ws_complexity}

    def calulate_from_source(self, source: str) -> float:
        return sum(self.calculate_complexity_in(source))

    

    def n_log_tabs(self, line):
        pattern = re.compile(r' +')
        wo_spaces = re.sub(pattern, '', line)
        match = self.leading_tabs_expr.search(wo_spaces)
        if match:
            tabs = match.group()
            return len(tabs)
        return 0
    
    def n_log_spaces(self, line):
        pattern = re.compile(r'\t+')
        wo_tabs = re.sub(pattern, '', line)
        match = self.leading_spaces_expr.search(wo_tabs)
        if match:
            spaces = match.group()
            return len(spaces)
        return 0
    
    def contains_code(self, line):
        return not self.empty_line_expr.match(line)
		
    def complexity_of(self, line):
        return self.n_log_tabs(line) + (self.n_log_spaces(line) / 4) # hardcoded indentation

    def calculate_complexity_in(self, source):
        return [self.complexity_of(line) for line in source.split("\n") if self.contains_code(line)]
