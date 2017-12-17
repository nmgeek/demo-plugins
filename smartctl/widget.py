import subprocess
import re
import os
from jadi import component

from aj.plugins.dashboard.api import Widget


class SMARTSensor:
    id = 'smart'
    timeout = 5

    def get_variants(self):
        r = []
        for s in os.listdir('/dev'):
            if re.match('sd.$|hd.$|scd.$|fd.$|ad.+$', s):
                r.append(s)
        return sorted(r)


@component(Widget)
class SMARTWidget (Widget):
    id = 'smartctl'
    name = 'S.M.A.R.T.'

    # template of the widget
    template = '/smartctl:resources/partial/widget.html'

    # template of the configuration dialog
    config_template = '/smartctl:resources/partial/widget.config.html'

    def __init__(self, context):
        Widget.__init__(self, context)

    def get_value(self, config):
        """
        -1 = No SMART
        0  = DISK FAILING
        1  = PRE-FAIL
        2  = Unknown error
        3  = Errors in log
        4  = DISK OK
        """
        if 'device' not in config:
            return 'Not configured'
        r = subprocess.call(['smartctl', '-H', config['device']])
        ret = 2
        if r & 2:
            ret = -1
        if r & 8:
            ret = 0
        if r & 16:
            ret = 1
        if r & 64:
            ret = 3
        if r == 0:
            ret = 4

        v = {
            -1: _('No data'),
            0: _('FAILING'),
            1: _('PRE-FAIL'),
            2: _('Unknown error'),
            3: _('Errors in log'),
            4: 'OK'
        }[ret]
        return v
