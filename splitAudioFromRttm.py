import pandas as pd
import numpy as np
from pydub import AudioSegment
import argparse
import os


def main(args):
    rttm = pd.read_csv(args.rttm_file, names=['Type', 'file', 'chnl', 'tbeg', 'tdur', 'ortho', 'stype', 'name', 'conf'], sep='\s+')
    assert len(rttm['file'].unique()) == 1, "The file should be transcription of only one audio file"
    filename = rttm['file'].unique()[0]
    
    audio = AudioSegment.from_file(os.path.join(args.audio_dir, filename), format='wav')
    
    speakers = {}
    for _, row in rttm.iterrows():
        spk = row['name']
        tbeg = row['tbeg']
        tdur = row['tdur']
        tend = tbeg+tdur
        
        if spk not in speakers:
            speakers[spk] = audio[tbeg:tend]
        else:
            speakers[spk] += audio[tbeg:tend]
            
    for spk, spk_audio in speakers.items():
        print('Processing speaker: {}'.format(spk))
        out_path = os.path.join(args.output_dir, '{}_speaker_{}.wav'.format(filename.rsplit('.', 1)[0], spk))
        spk_audio.export(out_path, format='wav')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rttm_file', help='Path to an rttm file describing exactly one audio file', required=True)
    parser.add_argument('--audio_dir', help='Path to the folder with audio (.wav) described in the rttm file', required=True)
    parser.add_argument('--output_dir', help='Path to an output folder', required=True)
    args = parser.parse_args()
    
    main(args)