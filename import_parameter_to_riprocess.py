import re
import numpy as np
import time
from pynput import mouse
import pyautogui as pg
import pyperclip

from processing.read_properties import Project


class Report:
    def __init__(self):
        self.create_params()

    def create_params(self):
        self.project = Project()
        self.num_param, self.array_parameters = self.clean_report(self.project.report, self.project.parameters)

    def clean_report(self, input, output):
        with open(input, 'r') as f:
            detect_params = 0
            list_corrections = []
            for line in f.readlines():
                if self.my_replace(line, ' ').split(' ')[0] == 'Flightline':
                    detect_params += 1
                    list_param = self.my_replace(line, ' ').replace(' shift', '').strip().split(' ')
                    num_param = len(list_param) - 1
                    if num_param == 6:
                        list_param = [list_param[0] ,list_param[5], list_param[6], list_param[4], *list_param[1:4]]
                if detect_params == 2:
                    break
                if detect_params and line[0].isdigit():
                    params = self.my_replace(line, ' ').rstrip().split(' ')
                    if num_param == 6:
                        params = [params[0] ,params[5], params[6], params[4], *params[1:4]]
                    list_corrections.append(params)

            array_parameters = np.array(list_corrections, dtype=float)
            np.savetxt(output, array_parameters, delimiter=',', fmt="%d," + ("%.3f," * num_param)[:-1],
                       header=','.join(list_param))

        return num_param, array_parameters

    def my_replace(self, s, character=', '):
        '''Replace all runs of whitespace with a single dash'''

        s = re.sub("\s+", character, s)
        return s


class Import(Report):
    def __init__(self, lines):
        Report.__init__(self)

        self.lines = lines
        x_fl, y_fl, x_epv, y_epv, x_fp, y_fp, x_ac, y_ac, x_cepv, y_cepv = self.listener_mouse()

        self.click_loop(x_fl, y_fl, x_epv, y_epv, x_fp, y_fp, x_ac, y_ac, x_cepv, y_cepv)

    def _listener_mouse(self, button='left'):
        with mouse.Events() as events:

            for event in events:
                try:
                    if button == 'left':
                        if event.button == mouse.Button.left and event.pressed:
                            return event.x, event.y
                            break
                    if button == 'right':
                        if event.button == mouse.Button.right and event.pressed:
                            return event.x, event.y
                            break

                except AttributeError as e:
                    pass

    def listener_mouse(self):

        # Loop for extraction coordinate to clicks
        for i in range(5):
            if i == 0:
                print('Kliknij prawym klawiszem na pierwsza linie')
                x_fl, y_fl = self._listener_mouse('right')
                print(f'x = {x_fl}, y = {y_fl}')
            elif i == 1:
                print('Kliknij lewym klawiszem na "edit parameter value"')
                x_epv, y_epv = self._listener_mouse()
                print(f'x = {x_epv}, y = {y_epv}')
            elif i == 2:
                print('Kliknij lewym klawiszem na pole pierwszego parametru')
                x_fp, y_fp = self._listener_mouse()
                print(f'x = {x_fp}, y = {y_fp}')
            elif i == 3:
                print('Kliknij lewym klawiszem na "apply changes"')
                x_ac, y_ac = self._listener_mouse()
                print(f'x = {x_ac}, y = {y_ac}')
            elif i == 4:
                print('Kliknij lewym klawiszem na "close edit parameter value"')
                x_cepv, y_cepv = self._listener_mouse()
                print(f'x = {x_cepv}, y = {y_cepv}')
        print('Nie ruszaj myszka')
        time.sleep(5)

        return x_fl, y_fl, x_epv, y_epv, x_fp, y_fp, x_ac, y_ac, x_cepv, y_cepv

    def click_loop(self, x_fl, y_fl, x_epv, y_epv, x_fp, y_fp, x_ac, y_ac, x_cepv, y_cepv, dy_l=17, dy_p=25,
                   t=0.05):
        dy_l_epv = y_epv - y_fl
        count = 0
        for line in self.array_parameters:
            # klik prawy
            pg.rightClick(x_fl, y_fl + dy_l * count)
            time.sleep(t * 2)

            # klik edit parameter values
            pg.leftClick(x_epv, y_fl + (dy_l * count + dy_l_epv))
            time.sleep(t * 2 + 0.05)

            # wklejenie parametrow
            count_param = -1
            for param in line:
                if count_param == -1:
                    count_param += 1
                    print(f'LINIA: {int(param)}')
                    continue
                else:
                    # kopia wartości
                    pyperclip.copy(param)
                    time.sleep(t)

                    # klik parameter
                    pg.leftClick(x_fp, y_fp + count_param * dy_p)
                    time.sleep(t)
                    pg.leftClick(x_fp, y_fp + count_param * dy_p)
                    time.sleep(t)

                    # ctrl a, v
                    pg.hotkey('ctrl', 'a')
                    time.sleep(t)
                    pg.hotkey('ctrl', 'v')

                    count_param += 1

                    print(f'Wklejono: {param}')
                    time.sleep(t)

            pg.leftClick(x_ac, y_ac)
            time.sleep(t)
            pg.leftClick(x_cepv, y_cepv)
            time.sleep(t)

            count += 1

            if (int(line[0])) % self.lines == 0:
                x_fl, y_fl, x_epv, y_epv, x_fp, y_fp, x_ac, y_ac, x_cepv, y_cepv = self.listener_mouse()
                count = 0
                dy_l_epv = y_epv - y_fl


if __name__ == '__main__':
    Import(3)
