import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
import pandas as pd
import pandas_profiling

app = QApplication(sys.argv)

fpath = r'C:\Users\Luiz\Desktop\example1.csv'
#df = pd.read_csv(fpath)
#df_profile = df.profile_report(style={'full_width':True}, )
#html = df_profile.html

web = QWebEngineView()
url = QUrl.fromLocalFile(r"C:\Users\Luiz\Desktop\my_report.html")
web.load(url)
web.show()

sys.exit(app.exec_())
