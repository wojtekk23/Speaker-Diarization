import pandas as pd
import numpy as np
from pydub import AudioSegment
import argparse
import librosa
import os
import matplotlib.pyplot as plt
import datetime

colors = np.array(['tab:blue', 'tab:orange', 'tab:green',
                   'tab:red', 'tab:purple', 'tab:brown',
                   'tab:pink', 'tab:gray', 'tab:olive',
                   'tab:cyan'])

global args

def combined_waveplot(audio_path, rttm, output_path, figsize=(10, 3), tick_interval=2.5):
    signal, fs = librosa.load(audio_path, args.sr)
    
    plt.figure(figsize=figsize)
    for _, row in rttm.iterrows():
        start = int(row['tbeg']*fs/1000)
        end = int(start + row['tdur']*fs/1000)
        spk = row['name']
        print(start, end)
        speech = signal[start:end]
        color = colors[int(spk)]

        linelabel = 'Speaker {}'.format(spk)
        plt.plot(np.linspace(start, end, len(
            speech)), speech, color=color, label=linelabel)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='lower right')

    plt.xlabel('Time')
    plt.xlim([0, len(signal)])

    xticks = np.arange(0, len(signal), tick_interval*fs)
    xtick_labels = [str(datetime.timedelta(seconds=int(x/fs))) for x in xticks]
    plt.xticks(ticks=xticks, labels=xtick_labels)

    max_amp = np.max(np.abs([np.max(signal), np.min(signal)]))
    plt.ylim([-max_amp, max_amp])

    plt.tight_layout()
    plt.savefig(output_path)
    return plt.gcf()


def main(args):
    rttm = pd.read_csv(args.rttm_file, names=['Type', 'file', 'chnl', 'tbeg', 'tdur', 'ortho', 'stype', 'name', 'conf'], sep='\s+')
    assert len(rttm['file'].unique()) == 1, "The file should be transcription of only one audio file"
    filename = rttm['file'].unique()[0]
    
    audio_path = os.path.join(args.audio_dir, filename)
    output_path = os.path.join(args.output_dir, "{}.png".format(filename.rsplit('.', 1)[0]))
    combined_waveplot(audio_path, rttm, output_path)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rttm_file', help='Path to an rttm file describing exactly one audio file', required=True)
    parser.add_argument('--audio_dir', help='Path to the folder with audio (.wav) described in the rttm file', required=True)
    parser.add_argument('--output_dir', help='Path to an output folder', required=True)
    parser.add_argument('--sr', default=16_000, help='Sampling rate of the audio file')
    args = parser.parse_args()
    
    main(args)
