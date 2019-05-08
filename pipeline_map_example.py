"""
magi tell
guillem frisach
"""

import pywren_ibm_cloud as pywren

iteration_data = [1, 2, 3, 4]


def my_map_function(x):
    return x + 5


pw = pywren.ibm_cf_executor()
pw.map(my_map_function, iterdata)
print(pw.get_result())
