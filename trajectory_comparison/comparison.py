import re
import matplotlib.pyplot as plt


with open('gmapping_trajectory.txt') as gmap_file:
    help_x = 0
    number_x = 0
    number_y = 0
    axe_x =[]
    help_y = 0
    axe_y = []
    sim_time = []
    for row in gmap_file:
        try:
            if row[10] is 'x':
                if help_x == 0:
                    help_x = (help_x+1) % 2
                    axe_x.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                    number_x += 1
                else:
                    help_x = (help_x+1) % 2
            if row[10] is 'y':
                if help_y == 0:
                    help_y = (help_y + 1) % 2
                    axe_y.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                    number_y += 1
                else:
                    help_y = (help_y + 1) % 2
            if row[10] is 's' and row[11] is 'e':
                sim_time.append(int(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
        except Exception:
            pass

start_time = sim_time[0]
processed_time = []
for time_stamp in sim_time:
    time_stamp -= start_time
    processed_time.append(time_stamp)
print axe_x
print axe_y
print processed_time
print len(axe_x), len(axe_x), len(processed_time)

plt.plot(axe_x, axe_y)
plt.show()

with open('hector_trajectory.txt') as gmap_file:
    help_x = 0
    number_x = 0
    number_y = 0
    axe_x =[]
    help_y = 0
    axe_y = []
    sim_time = []
    for row in gmap_file:
        try:
            if row[4] is 'x':
                if help_x == 0:
                    help_x = (help_x+1) % 2
                    axe_x.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                    number_x += 1
                else:
                    help_x = (help_x+1) % 2
            if row[4] is 'y':
                if help_y == 0:
                    help_y = (help_y + 1) % 2
                    axe_y.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                    number_y += 1
                else:
                    help_y = (help_y + 1) % 2
            if row[4] is 's':
                sim_time.append(int(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
        except Exception:
            pass

start_time = sim_time[0]
processed_time = []
for time_stamp in sim_time:
    time_stamp -= start_time
    processed_time.append(time_stamp)
print axe_x
print axe_y
print processed_time
print len(axe_x), len(axe_x), len(processed_time)

plt.plot(axe_x, axe_y)
plt.show()

with open('odom.txt') as gmap_file:
    help_x = 0
    number_x = 0
    number_y = 0
    axe_x =[]
    help_y = 0
    axe_y = []
    sim_time = []
    for row in gmap_file:
        try:
            if row[6] is 'x':
                if help_x == 0:
                    help_x = (help_x+1) % 4
                    axe_x.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                    number_x += 1
                else:
                    help_x = (help_x+1) % 4
            if row[6] is 'y':
                if help_y == 0:
                    help_y = (help_y + 1) % 4
                    axe_y.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                    number_y += 1
                else:
                    help_y = (help_y + 1) % 4
            if row[4] is 's':
                sim_time.append(int(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
        except Exception:
            pass

start_time = sim_time[0]
processed_time = []
for time_stamp in sim_time:
    time_stamp -= start_time
    processed_time.append(time_stamp)
print axe_x
print axe_y
print processed_time
print len(axe_x), len(axe_x), len(processed_time)

plt.plot(axe_x, axe_y)
plt.show()
