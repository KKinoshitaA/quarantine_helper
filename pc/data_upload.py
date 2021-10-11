import csv
from datetime import datetime as dt
import sys
import threading
import re

import boto3
import matplotlib.pyplot as plt
import serial

SERIAL_DEVICE_NAME = "/dev/tty.usbmodem1141301"
class Plotter():
    def __init__(self, label, samples):
        self.initial_flag = True
        self.exit_flag = False
        self.label = label
        self.samples = samples

    def run(self):
        fig, ax = plt.subplots()

        arr = [0] * self.samples
        x = range(0, self.samples)

        ser = serial.Serial(SERIAL_DEVICE_NAME, 115200, timeout=None)

        while True:
            while True:
                line = ser.readline().decode().replace('\r', '').replace('\n', '')
                if not line.startswith("[DATA]"):
                    continue

                # extract emg data
                emg = re.search(r'cnt:(\d+)', line)
                cnt = int(emg.group(1))
                emg = re.search(r'emg:([\d\.]+)', line)
                val = float(emg.group(1))

                # write csv header
                if self.initial_flag:
                    if cnt != 0:
                        continue

                    line = line.lstrip('[DATA]')
                    header_str = re.sub(r'[^a-zA-Z\_\,]', '', line)
                    header_arr = header_str.split(',')
                    header_arr.append("label")
                    with open('/tmp/data.csv', 'w') as f:
                        writer = csv.writer(f)
                        writer.writerow(header_arr)
                    self.initial_flag = False

                # write csv row
                data_arr = re.findall(r'[\d\.]+', line)
                data_arr.append(label)
                with open('/tmp/data.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(data_arr)

                arr[cnt] = val
                if cnt == self.samples-1:
                    break

            # plot
            ax.set_xlim(0, self.samples)
#            ax.set_ylim(400, 1024)
            line, = ax.plot(x, arr, color='blue')
            plt.pause(0.1)
            line.remove()

            if self.exit_flag:
                break

        # upload to S3
        print("uploading to S3 ...")
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('sensor-data-keisuke-nakata')

        tdatetime = dt.now()
        daystr = tdatetime.strftime('%Y/%m/%d')
        secstr = tdatetime.strftime('%H-%M-%S')
        key_name = 'sample=' + str(self.samples) + '/label=' + self.label + '/dt=' + daystr + '/' + secstr + '.csv'
        bucket.upload_file('/tmp/data.csv', key_name)
        print("done")
        ser.close()

    def check_stdin(self):
        while True:
            ch = input()
            if ch == 'q':
                self.exit_flag = True
                break

if __name__ == '__main__':
    if len(sys.argv) == 2:
        label = sys.argv[1]
        samples = 256
    elif len(sys.argv) == 3:
        label = sys.argv[1]
        samples = int(sys.argv[2])
    else:
        print("usage: sudo python data_plot.py label (samples)")
        exit(0)
    print("Press q and ENTER to stop")

    pl = Plotter(label, samples)
    # start plot and creating csv, then upload to S3
    th = threading.Thread(target=pl.check_stdin)
    th.start()
    try:
        pl.run()
    except KeyboardInterrupt:
        print("Press q and ENTER to stop")
