# PandasVIS
Tabular data exploration GUI, with Data Science and Machine Learning tools.

Powered by: [Pandas](https://pandas.pydata.org/), [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro), [Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling), [Plotly](https://plot.ly/)

### Installation
To clone the repository and set up a conda environment, do:

```bash
$ git clone https://github.com/luiztauffer/pandasVIS
$ conda env create -f pandasVIS/make_env.yml
$ source activate pandas_vis
```

Alternatively, to install PandasVIS directly in an existing environment:

```bash
pip install git+https://github.com/luiztauffer/pandasVIS
```

### Usage

PandasVIS module can be imported and the GUI initialized with:
```python
from pandasvis.main import main as pdvis

app = pdvis()
```

Save this convenience script, e.g. `call_pandas_vis.py`, in any directory and run in terminal:
```bash
$ python call_pandas_vis.py
```

### Examples
![](media/gif_1.gif)
