from typing import Any, List
import numpy as np
import random
from common import createWav,soundLevelRegulation

def createWhiteNoise(num_data:int,mean:float,std:float):
    """ホワイトノイズを生成する

    Args:
        num_data (int): [44100*2　で１秒のホワイトノイズとなる]
        mean (float): [平均値]
        std (float): [分散]
    """
# data_len:int = 200000 #ノイズデータのデータ長
# mean:float = 0.0  #ノイズの平均値
# std:float  = 1.0  #ノイズの分散
    whitenoise_data:np.ndarray[np.float64] = np.array( [random.gauss(mean, std) for i in range(num_data)] )
    vol_adjusted_whitenoise:bytes = soundLevelRegulation(whitenoise_data)
    createWav(vol_adjusted_whitenoise,"8_Result/whitenoise.wav")

def createSineWave (A:float, f0:int, fs:int, length:int):
    """[sin波を生成する]

    Args:
        A (float): [sin波の振幅]
        f0 (int): [基本周波数]
        fs (int): [サンプリング周波数]
        length (int): [サイン波の長さ（秒）]
    """
    data_list:List[float] = []
    # [-1.0, 1.0]の小数値が入った波を作成
    for n in range(length * fs):  # nはサンプルインデックス
        # breakpoint()
        s = A * np.sin(2 * np.pi * f0 * n / fs)
        # 振幅が大きい時はクリッピング
        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data_list.append(s)
    vol_adjusted_sine = soundLevelRegulation(np.array(data_list))
    createWav(vol_adjusted_sine,"8_Result/sine.wav")


createWhiteNoise(44100*4,0,1.0)
createSineWave(1.0,100,44100,10)
