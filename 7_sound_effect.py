from typing import Union
import wave
import numpy as np
from common import createWav, soundLevelRegulation


def distortSoundData(input_data:Union[str,bytes,np.ndarray], level: int)->bytes:
    """音を歪ませる

    Args:
        input_data (Union[str,bytes,np.ndarray]): [音ファイルのパス、バイトデータ、ndarray[int16]のいずれか]
        level (int): [歪ませる大きさ　値が小さくなるほど歪が大きくなる]

    Returns:
        [bytes]: [音のバイトデータを返す]
    """    

    if type(input_data) == str:
        wf = wave.open(input_data , "rb" )
        buf = wf.readframes(wf.getnframes())
        data:np.ndarray[np.int16] = np.frombuffer(buf, dtype="int16")
    if type(input_data) == bytes:
        data:np.ndarray[np.int16] = np.frombuffer(buf, dtype="int16")
    if type(input_data) == np.ndarray:
        data = input_data

    distorted_data: np.ndarray[np.int16] = np.zeros(len(data), dtype=np.int16)
    for i, frame in enumerate(data):
        if frame >= level:
            distorted_data[i] = level
        elif frame <= -level:
            distorted_data[i] = -level
        else:
            distorted_data[i] = data[i]

    distorted_bytes_data: bytes = soundLevelRegulation(distorted_data)
    return distorted_bytes_data


distorted_data = distortSoundData("4_Result/backing_gt_left.wav", 10000)

createWav(distorted_data, "7_Result/backing_gt_left.wav")
