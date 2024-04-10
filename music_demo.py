import argparse
import base64
import requests
import numpy as np
from scipy.io import wavfile


api_address = "http://api.mthreads.com/mtaudiolab/api/v1/generate"


def decode_and_save(sample_rate, bytes, filename):
    ''' Decode the returned waveform and save it to a file
    '''
    audio_data = np.frombuffer(base64.b64decode(bytes), dtype=np.int16)
    wavfile.write(filename, sample_rate, audio_data)


def music_generate(token, text, dur, output_file):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    request_payload = {
        "task": "musicgen",
        "text": [text],
        "duration": dur,
    }
    resp = requests.post(api_address, json=request_payload, headers=headers)
    assert resp.status_code == 200
    resp = resp.json()
    res = resp['results'][0]
    decode_and_save(res[0], res[1], output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", type=str, required=True, help="the authorization token")
    parser.add_argument("--text", type=str, required=True, help="the music description")
    parser.add_argument("--dur", type=str, default=5, help="the target duration")
    parser.add_argument("--output_file", type=str, required=True, help="the output filename")
    args = parser.parse_args()
    music_generate(args.token, args.text, args.dur, args.output_file)


if __name__ == '__main__':
    main()
