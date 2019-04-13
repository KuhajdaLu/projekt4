import re
import matplotlib.pyplot as plt
import math
from numpy import linalg as la

class LidarMethodsComparing():

    def __init__(self):
        self.gmapping_data = self.load_gmapping()
        self.hector_data = self.load_hector()
        self.ground_truth = self.load_ground_truth()
        self.cartographer_data = self.load_cartographer()
        self.comparison()

    def comparison(self):
        self.compare_methods(self.cartographer_data)
        self.plot_method(self.cartographer_data, self.ground_truth, self.gmapping_data, self.hector_data)
        pass

    def plot_method(self, data1, data2, data3, data4):
        #print len(data1[2])
        #print len(data2[2])
        #print len(data3[2])
        #print len(data4[2])
        #print data1[2]
        #print data2[2]
        #print data3[2]
        #print data4[2]
        plt.plot(data1[0], data1[1])
        plt.plot(data2[0], data2[1])
        plt.plot(data3[0], data3[1])
        plt.plot(data4[0], data4[1])
        plt.show()

    def compare_methods(self, met):
        index2 = 0
        position_diff = []
        rotation_diff = []
        for i in range(len(met[0])-1):
            index1 = index2
            for j in range(len(self.ground_truth[2])):
                if self.ground_truth[2][j] == met[2][i+1]:
                    index2 = j
                    break
            rot_diff_met = abs(met[4][i+1] - met[4][i])
            rot_diff_ground_truth = abs(self.ground_truth[4][index2] - self.ground_truth[4][index1])
            min_val_met = min([2*math.pi-rot_diff_met, rot_diff_met])
            min_val_ground_truth = min([2*math.pi-rot_diff_ground_truth, rot_diff_ground_truth])
            rotation_diff.append(abs(min_val_ground_truth-min_val_met))

            x = [(met[0][i + 1] - met[0][i]) - (self.ground_truth[0][index2] - self.ground_truth[0][index1]),
                    (met[1][i + 1] - met[1][i]) - (self.ground_truth[1][index2] - self.ground_truth[1][index1])]
            norm_x = la.norm(x)
            position_diff.append(norm_x)
        print rotation_diff
        print position_diff




    def angle_transform(self, data):
        angles = []
        for i in data:
            angles.append(i*(-2*math.pi)+math.pi)
        return angles

    def load_cartographer(self):
        with open('cart_traj_launch.txt') as cart_file:
            axe_x = []
            axe_y = []
            processed_time = []
            orientation_z = []
            orientation_w = []
            for row in cart_file:
                values = row.split(',')
                axe_x.append(float(values[5]))
                axe_y.append(float(values[6]))
                processed_time.append(float(values[0])/1000000000)
                orientation_z.append(float(values[10]))
                orientation_w.append(float(values[11]))
            start_time = processed_time[0]
            for i in range(len(processed_time)):
                processed_time[i] -= start_time + 0.05
                processed_time[i] = float(int(processed_time[i]*10))/10

            axe_x_0 = axe_x[0]
            axe_y_0 = axe_y[0]
            rot_diff = 1 - orientation_w[0]
            for i in range(len(axe_x)):
                axe_x[i] -= axe_x_0
                axe_y[i] -= axe_y_0
                orientation_w[i] += rot_diff
            orientation_w = self.angle_transform(orientation_w)
            data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
            return data

    def load_gmapping(self):
        with open('gmapping_traj_ground.txt') as gmap_file:
            help_x = 0
            number_x = 0
            number_y = 0
            axe_x = []
            help_y = 0
            axe_y = []
            sim_time = []
            time_of_stamp = ''
            orientation_z = []
            orientation_w = []
            help_z = 0
            number_z = 0
            number_w = 0
            for row in gmap_file:
                try:
                    if row[10] is 'x':
                        if help_x == 0:
                            help_x = (help_x + 1) % 2
                            x_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[26] is 'e' or row[27] is 'e':
                                    x_value = x_value / 100000
                            except Exception:
                                pass
                            axe_x.append(x_value)
                            number_x += 1
                        else:
                            help_x = (help_x + 1) % 2
                    if row[10] is 'y':
                        if help_y == 0:
                            help_y = (help_y + 1) % 2
                            y_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[26] is 'e' or row[27] is 'e':
                                    y_value = y_value / 100000
                            except Exception:
                                pass
                            axe_y.append(y_value)
                            number_y += 1
                        else:
                            help_y = (help_y + 1) % 2
                    if row[10] is 's':
                        time_of_stamp = ''
                        time_of_stamp = re.findall(r"\d+", row)[0] + '.'
                    if row[10] is 'n':
                        time_of_stamp = time_of_stamp + re.findall(r"\d+", row)[0]
                        time_of_stamp = int(float(time_of_stamp)*10)
                        sim_time.append(time_of_stamp)
                    if row[10] is 'z':
                        if help_z == 1:
                            help_z = (help_z + 1) % 2
                            z_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    z_value = z_value / 100000
                            except Exception:
                                pass
                            orientation_z.append(z_value)
                            number_z += 1
                        else:
                            help_z = (help_z + 1) % 2
                    if row[10] is 'w':
                        w_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                        try:
                            if row[20] is 'e' or row[21] is 'e':
                                w_value = w_value / 100000
                        except Exception:
                            pass
                        orientation_w.append(w_value)
                        number_w += 1
                except Exception:
                    pass

        axe_x_0 = axe_x[0]
        axe_y_0 = axe_y[0]
        for i in range(len(axe_x)):
            axe_x[i] -= axe_x_0
            axe_y[i] -= axe_y_0

        start_time = sim_time[0]
        processed_time = []
        for time_stamp in sim_time:
            time_stamp -= start_time
            time_stamp = float(time_stamp) / 10
            processed_time.append(time_stamp)
        orientation_w = self.angle_transform(orientation_w)
        data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
        return data

    def load_hector(self):
        with open('hector_traj_ground.txt') as gmap_file:
            help_x = 0
            number_x = 0
            number_y = 0
            axe_x = []
            help_y = 0
            axe_y = []
            sim_time = []
            time_of_stamp = ''
            orientation_z = []
            orientation_w = []
            help_z = 0
            number_z = 0
            number_w = 0
            for row in gmap_file:
                try:
                    if row[4] is 'x':
                        if help_x == 0:
                            help_x = (help_x + 1) % 2
                            x_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    x_value = x_value / 100000
                            except Exception:
                                pass
                            axe_x.append(x_value)
                            number_x += 1
                        else:
                            help_x = (help_x + 1) % 2
                    if row[4] is 'y':
                        if help_y == 0:
                            help_y = (help_y + 1) % 2
                            y_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    y_value = y_value / 100000
                            except Exception:
                                pass
                            axe_y.append(y_value)
                            number_y += 1
                        else:
                            help_y = (help_y + 1) % 2
                    if row[4] is 's':
                        time_of_stamp = ''
                        time_of_stamp = re.findall(r"\d+", row)[0] + '.'
                    if row[4] is 'n':
                        time_of_stamp = time_of_stamp + re.findall(r"\d+", row)[0]
                        time_of_stamp = int(float(time_of_stamp) * 10)
                        sim_time.append(time_of_stamp)
                    if row[4] is 'z':
                        if help_z == 1:
                            help_z = (help_z + 1) % 2
                            z_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            try:
                                if row[20] is 'e' or row[21] is 'e':
                                    z_value = z_value / 100000
                            except Exception:
                                pass
                            orientation_z.append(z_value)
                            number_z += 1
                        else:
                            help_z = (help_z + 1) % 2
                    if row[4] is 'w':
                        w_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                        try:
                            if row[20] is 'e' or row[21] is 'e':
                                w_value = w_value / 100000
                        except Exception:
                            pass
                        orientation_w.append(w_value)
                        number_w += 1
                except Exception:
                    pass

        axe_x_0 = axe_x[0]
        axe_y_0 = axe_y[0]
        for i in range(len(axe_x)):
            axe_x[i] -= axe_x_0
            axe_y[i] -= axe_y_0

        start_time = sim_time[0]
        processed_time = []
        for time_stamp in sim_time:
            time_stamp -= start_time
            time_stamp = float(time_stamp) / 10
            processed_time.append(time_stamp)
        orientation_w = self.angle_transform(orientation_w)
        data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
        return data

    def load_ground_truth(self):
        with open('ground_truth.txt') as gmap_file:
            help_x = 0
            number_x = 0
            number_y = 0
            axe_x = []
            help_y = 0
            axe_y = []
            sim_time = []
            time_of_stamp = ''
            orientation_z = []
            orientation_w = []
            help_z = 0
            number_z = 0
            number_w = 0
            for row in gmap_file:
                try:
                    if row[6] is 'x':
                        if help_x == 0:
                            help_x = (help_x + 1) % 4
                            axe_x.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                            number_x += 1
                        else:
                            help_x = (help_x + 1) % 4
                    if row[6] is 'y':
                        if help_y == 0:
                            help_y = (help_y + 1) % 4
                            axe_y.append(float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0]))
                            number_y += 1
                        else:
                            help_y = (help_y + 1) % 4
                    if row[4] is 's':
                        time_of_stamp = ''
                        time_of_stamp = re.findall(r"\d+", row)[0] + '.'
                    if row[4] is 'n':
                        time_of_stamp = time_of_stamp + re.findall(r"\d+", row)[0]
                        time_of_stamp = int(float(time_of_stamp)*10)
                        sim_time.append(time_of_stamp)
                    if row[6] is 'z':
                        if help_z == 1:
                            help_z = (help_z + 1) % 4
                            z_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                            orientation_z.append(z_value)
                            number_z += 1
                        else:
                            help_z = (help_z + 1) % 4
                    if row[6] is 'w':
                        w_value = float(re.findall(r"[-+]?\d*\.\d+|\d+", row)[0])
                        orientation_w.append(w_value)
                        number_w += 1
                except Exception:
                    pass

        axe_x_0 = axe_x[0]
        axe_y_0 = axe_y[0]
        for i in range(len(axe_x)):
            axe_x[i] -= axe_x_0
            axe_y[i] -= axe_y_0

        start_time = sim_time[0]
        processed_time = []
        for time_stamp in sim_time:
            time_stamp -= start_time
            time_stamp = float(time_stamp)/10
            processed_time.append(time_stamp)
        orientation_w = self.angle_transform(orientation_w)
        data = [axe_x, axe_y, processed_time, orientation_z, orientation_w]
        return data


def main():
    LidarMethodsComparing()


if __name__ == '__main__':
    main()
