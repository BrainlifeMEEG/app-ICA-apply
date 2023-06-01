# this app is used to read in an ICA object, exclude identified components
# and reconstruct the raw data before saving it.

import os
import mne
import json
import helper
from mne.preprocessing import ICA

#workaround for -- _tkinter.TclError: invalid command name ".!canvas"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


with open('config.json') as config_json:
    config = helper.convert_parameters_to_None(json.load(config_json))

data_file = config['mne']
raw = mne.io.read_raw_fif(data_file, preload=True)

fname = config['ica']
ica = mne.preprocessing.read_ica(fname)
ica_exclude = config['exclude'].split(',')
ica.exclude = [int(i) for i in ica_exclude]

plt.figure(1)
ica.plot_overlay(raw)
plt.savefig(os.path.join('out_figs','plot_overlay.png'))


report = mne.Report(title='ICA')
report.add_ica(ica, 'ICA', inst = raw)
report.save('out_report/report_ica.html', overwrite=True)

ica.apply(raw)
raw.save(os.path.join('out_dir','meg.fif'),overwrite=True)

