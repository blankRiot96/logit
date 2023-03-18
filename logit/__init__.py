from ._enums import Level, OutputFormat
from ._logger import Logger as _Logger
from ._logger import StructualLogger
from ._cli import CLI as _CLI


def _cli():
    _CLI()


log = _Logger()
