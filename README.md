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
```
CLUTTER | test.py:3 | Test message!
ERROR | test.py:6 | Error error!
```

## 🛠️ Setup and Install
- Install from `pip`
```
pip install logit-axis
```
OR

- Clone the repository, and install from directory
```
git clone https://github.com/blankRiot96/logit
cd logit
pip install .
```

OR

- Or simply use the `git+` syntax,
```
pip install git+https://github.com/blankRiot96/logit
```

## 🍉 Credits
- @blankRiot96 - Lead maintainer
