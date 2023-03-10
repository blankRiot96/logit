<div align="center">
    <img src="assets/title_logo.png" width=500>
</div>

## 📝 Usage
```py
from logit import log, Level

log.clutter("Test message!")

log.config(level=Level.ERROR)

log.clutter("Wont appear no more")
log.error("Error error!")
```

output:
```log
[CLUTTER] | test.py:3 | Test message!
[ERROR] | test.py:8 | Error error!
```

## 🛠️ Setup and Install
- Install from `pip`
```
pip install logit-axis
```

## Features
- [x] *Structured logs*- allows consistent output to different formats that can be easily searched or queried. Formats such as:
  - JSON
  - XML
  - CSV

This is done by using the `OutputFormat` enum to create a new structural logger.
This is added to the `log`, by using the `add_structural_logger` method.
As suggested, this supports multiple structural loggers.
```py
from logit import log, OutputFormat

log.add_structural_logger(OutputFormat.JSON)

log.debug("Application running at Port:5050")
```

Output JSON file:
```json
[
  {
    "msg": "Application running at Port:5050",
    "level": "[DEBUG]",
    "line_number": "_logger.py:137",
    "local_time": "13:18:35"
  }
]
```

Or, in the example of CSV:
```py
from logit import log, OutputFormat

log.add_structural_logger(OutputFormat.CSV)

log.clutter("Stuffs!")
log.info("Application started")
log.debug("Application running at Port")
log.warning("I wouldn't do that")
log.error("Errors")
log.critical("Out of memory.")
```

Output CSV:
| msg                         | level     | line_number    | local_time |
|-----------------------------|-----------|----------------|------------|
| Stuffs!                     | [CLUTTER] | _logger.py:182 | 17:56:37   |
| Application started         | [INFO]    | _logger.py:182 | 17:56:37   |
| Application running at Port | [DEBUG]   | _logger.py:182 | 17:56:37   |
| I wouldn't do that          | [WARNING] | _logger.py:182 | 17:56:37   |
| Errors                      | [ERROR]   | _logger.py:182 | 17:56:37   |
| Out of memory.              | [CRITICAL]| _logger.py:182 | 17:56:37   |


- [x] *Custom log format* - users can customize the sequence, color, or even information which is showed in logs.
This is done by specifing the various prefix and suffix strings that are displayed before and after the log message.
Example:
```py
from logit import log
from logit.output import (
    level,
    local_time,
    line_number,
)


def get_mood() -> str:
    return "happy"


log.format = {
    "msg-prefix": [level, get_mood],
    "msg-suffix": [local_time, line_number],
}

log.debug("Test message")
```

Output:
```
[DEBUG] | happy | Test message | 11:30:4 | test.py:18
```

**The callable provided as elements in the list, must accept no arguments and
return a string.**

- [x] *Accessible types* - All useful types used in the `logit` module can be accessed
through the `logit.types_` module, which saves users from having to specify their own type aliases when using the module.

- [x] *Time based rotation* - Log files can be cleared and archived after every N days, weeks, months or years.
```py
from logit import log

# Rotates log file after every 5
# days.
log.config(rotation_time="5d")
```

- [x] *Space based rotation* - Log files can be cleared or archives after it takes up a certain number of kilobytes, megabytes, gigabytes or terabytes.
```py
from logit import log

# Rotates log file after it
# consumes 20 mb
log.config(rotation_space="20mb")
```

- [ ] *Archives* - **Log files are never deleted but simply rotated.** All archives are saved in the AppData directory of the respective Operating System and can always be retrieved. They can also be cleared with
```
logit clear-archives project-directory/
```


## 🍉 Credits
- @blankRiot96 - Lead maintainer
