from abc import ABC, abstractmethod
from typing import Any, Dict
from enum import Enum, unique, auto

from vartika.abstractresult import AbstractResult


class EnumLowerCase(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):  # pylint: disable=unused-argument
        return str(name).lower().replace('_', '-')


@unique
class MetricKeys(EnumLowerCase):

    # keys for metric names
    NUMBER_OF_METHODS = auto()
    SOURCE_LINES_OF_CODE = auto()
    FAN_IN_OUT = auto()


@unique
class MetricResultFilter(Enum):
    FILE_RESULTS = auto()
    ENTITY_RESULTS = auto()


class AbstractMetric(ABC): #base abstract class that defines the interface for all metrics.

    @property
    @abstractmethod
    def metric_name(self):
        ...

    @property
    @abstractmethod
    def pretty_metric_name(self):   #returns a human-readable name of the metric.
        ...

    @property
    @abstractmethod
    def analysis(self):
        ...

    @property
    @abstractmethod
    def local_data(self):
        ...

    @property
    @abstractmethod
    def overall_data(self):
        ...

    @abstractmethod
    def calculate_from_results(self, results: Dict[str, AbstractResult]):
        ...


class AbstractGraphMetric(AbstractMetric):

    @property
    @abstractmethod
    def dependency_graph_representation(self) -> Any:
        ...
    
    @dependency_graph_representation.setter
    def dependency_graph_representation(self, value): # pylint: disable=unused-argument
        ...

    @property
    @abstractmethod
    def inheritance_graph_representation(self) -> Any:
        ...

    @inheritance_graph_representation.setter
    def inheritance_graph_representation(self, value): # pylint: disable=unused-argument
        ...

    @property
    @abstractmethod
    def complete_graph_representation(self) -> Any:
        ...
    
    @complete_graph_representation.setter
    def complete_graph_representation(self, value): # pylint: disable=unused-argument
        ...


    @abstractmethod
    def calculate_from_results(self, results: Dict[str, AbstractResult]):
        ...


class AbstractCodeMetric(AbstractMetric):

    @abstractmethod
    def calculate_from_results(self, results: Dict[str, AbstractResult]):
        ...
