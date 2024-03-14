# this app is used to read in an ICA object, exclude identified components
# and reconstruct the raw data before saving it.

import os
import mne
import json
import helper
from mne.preprocessing import ICA
import re

#workaround for -- _tkinter.TclError: invalid command name ".!canvas"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


with open('config.json') as config_json:
    config = helper.convert_parameters_to_None(json.load(config_json))
    
# turn config['exclude'] into a list of integers, parsing the separated string to a list
config['exclude'] = [int(x) for x in re.split("\\W+",config['exclude'])]


data_file = config['mne']
raw = mne.io.read_raw_fif(data_file, preload=True)

fname = config['ica']
ica = mne.preprocessing.read_ica(fname)

if config['EOG_chan']:
    eog_ch = config['EOG_chan']
    # turn comma separated string into a list of numbers
    eog_ch = [int(x) for x in re.split("\\W+",eog_ch)]
else:
    eog_ch = None
    
if config['ECG_chan']:
    ecg_ch = config['ECG_chan']
    ecg_ch = [int(x) for x in re.split("\\W+",ecg_ch)]
else:
    ecg_ch = None
    
if config['reject_EOG']:
    eog_idx, eog_scores = mne.preprocessing.ICA.find_bads_eog(ch_name=eog_ch, threshold=3.0, start=None, stop=None, l_freq=1, h_freq=10, reject_by_annotation=True, measure='zscore', verbose=None)
if config['reject_ECG']:
    ecg_idx, ecg_scores = mne.preprocessing.ICA.find_bads_ecg(ch_name=ecg_ch, threshold='auto', start=None, stop=None, l_freq=8, h_freq=16, method='ctps', reject_by_annotation=True, measure='zscore', verbose=None)


plt.figure(1)
ica.plot_overlay(raw)
plt.savefig(os.path.join('out_figs','plot_overlay.png'))


report = mne.Report(title='ICA')
report.add_ica(ica, 'ICA', inst = raw)
report.save('out_report/report_ica.html', overwrite=True)

ica.apply(raw)
raw.save(os.path.join('out_dir','meg.fif'),overwrite=True)

