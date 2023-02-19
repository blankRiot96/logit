import typing as _t

LogConfigDict: _t.TypeAlias = dict[str, str]
LogFormatCallable: _t.TypeAlias = _t.Callable[[], str]
LogFormatDict: _t.TypeAlias = dict[str, list[LogFormatCallable]]
