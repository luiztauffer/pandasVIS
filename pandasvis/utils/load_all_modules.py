from pandasvis.classes.profiling import PandasProfiling
from pandasvis.classes.scatter_matrix import ScatterMatrix
from pandasvis.classes.joyplot import Joyplot


def load_all_modules():
    modules_list = list()
    modules_list.append(PandasProfiling)
    modules_list.append(ScatterMatrix)
    modules_list.append(Joyplot)

    return modules_list
