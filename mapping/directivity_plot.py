import random

import numpy as np
import matplotlib.pyplot as plt
import csv

distance = 100

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})


def modify_x(val, times):
    r_range = 20
    val = int(val)
    out = []
    for i in range(times):
        new_val = val
        new_val += random.randint(- r_range, r_range)
        new_val = np.deg2rad(new_val)
        out.append(new_val)
    return out


with open("directivity.csv", "r") as c:
    reader = csv.reader(c)
    for row in reader:
        if row[0] == str(distance):
            ax.scatter(modify_x(row[1], len(row[2:])), row[2:], alpha=.05)

ax.set_rmax(2)
ax.set_rticks([5 * i for i in range(1, 4)])
ax.set_rlabel_position(-22.5)
ax.grid(True)

ax.set_title("Directivity", va='bottom')
plt.show()
