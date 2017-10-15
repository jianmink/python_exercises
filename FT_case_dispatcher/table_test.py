import tableprint
import numpy as np

data = np.random.randn(10,3)
headers = ['Column A', 'Column B', 'Column C']

tableprint.table(data, headers)
