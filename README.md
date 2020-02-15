# PandasVIS
Tabular data exploration GUI, with Data Science and Machine Learning tools.

Powered by: [Pandas](https://pandas.pydata.org/), [PySide2](https://wiki.qt.io/Qt_for_Python), [Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling), [Plotly](https://plot.ly/), [QtConsole](https://ipython.org/ipython-doc/dev/interactive/qtconsole.html)

### Installation
To install PandasVIS directly in an existing environment:

```bash
pip install git+https://github.com/luiztauffer/pandasVIS
```

### Usage

PandasVIS module can be imported and the GUI initialized with:
```python
from pandasvis.main import main as pdvis

app = pdvis()
```

Save this convenience script, e.g. `run_pandas_vis.py`, in any directory and run in terminal:
```bash
$ python run_pandas_vis.py
```

### Examples
![](media/gif_1.gif)
