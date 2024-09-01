from typing import Dict
import logging

import coloredlogs

from vartika.languages.abstractparser import AbstractParser
from vartika.languages.javaparser import JavaParser # type: ignore
from vartika.languages.cparser import CParser # type: ignore
from vartika.languages.cppparser import CPPParser
from vartika.languages.javascriptparser import JavaScriptParser
from vartika.languages.objcparser import ObjCParser
from vartika.languages.pyparser import PythonParser


from vartika.config import Configuration
from vartika.analyzer import Analyzer
from vartika.abstractresult import AbstractResult
from vartika.log import Logger, LogLevel

LOGGER = Logger(logging.getLogger('vartika'))
coloredlogs.install(level='E', logger=LOGGER.logger(), fmt=Logger.log_format)

__version__ = '2.0.0'
__updated__ = '2024-08-31'


class Graphcodemapper:
    _version: str = f'{__version__}'
    config = Configuration(_version)

    def __init__(self):
        """Initialize all collected results, available parsers and set the log level.
        """
        self._results: Dict[str, AbstractResult] = {}
        self._parsers: Dict[str, AbstractParser] = {
            JavaParser.parser_name(): JavaParser(),
            CParser.parser_name(): CParser(),
            CPPParser.parser_name(): CPPParser(),
            JavaScriptParser.parser_name(): JavaScriptParser(),
            ObjCParser.parser_name(): ObjCParser(),
            PythonParser.parser_name(): PythonParser(),
        }

        self.config.supported_languages = [x.language_type() for x in self._parsers.values()]
        self.config.setup_commang_line_arguments()
        self.set_log_level(LogLevel.ERROR)

    def parse_args(self):
        self.config.parse_args()

    def load_config(self, path):
        self.config.load_config_from_yaml_file(path)

    def print_config(self):
        self.config.print_config_as_yaml()
        self.config.print_config_dict()

    def get_config(self) -> Dict:
        return self.config.get_config_as_dict()

    def print_version(self):
        LOGGER.info(f'Graph Code Mapper version: {self.get_version()}')

    def start(self):
        """Starts Graph Code Mapper by parsing arguments/configuration and starting the analysis from an analyzer instance. 
        """

        self.parse_args()

        if self.config.has_valid_config_path():
            self.load_config(self.config.yaml_config_path)
            if self.config.valid:
                self.start_analyzing()
            else:
                LOGGER.error('will not start with any analysis due to configuration errors')
                return

    def start_with_log_level(self, level: LogLevel):
        """Sets a custom log level and starts graph code mapper.""" 

        Logger.set_log_level(level)
        self.start()

    def set_log_level(self, level: LogLevel):
        Logger.set_log_level(level)

    def start_analyzing(self):
       
        analyzer = Analyzer(self.config, self._parsers)
        analyzer.start_analyzing()

    @staticmethod
    def get_version() -> str:
        return Graphcodemapper._version
