from typing import List, Union
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt
from pydub.audio_segment import AudioSegment


def plotSoundData(input_data: Union[str, bytes, np.ndarray]):
    """音データをプロットする

    Args:
        input_data (Union[str,bytes,np.ndarray]): 音データのファイル、バイトデータ、ndarray[int16]を入力とする
    """
    if type(input_data) == str:
        wf = wave.open(input_data, "rb")
        buf = wf.readframes(wf.getnframes())
        data: np.ndarray[np.int16] = np.frombuffer(buf, dtype="int16")
    if type(input_data) == bytes:
        data: np.ndarray[np.int16] = np.frombuffer(buf, dtype="int16")
    if type(input_data) == np.ndarray:
        data = input_data

    # グラフ化
    plt.plot(data)
    plt.grid()
    plt.show()


def createWav(input_data: Union[bytes,np.ndarray], file_name: str, stereo: bool = True, sampling_rate=44100):
    """Waveファイルを生成する

    Args:
        input_data (Union[bytes,np.ndarray]): bytesデータ、ndarray[int16]のいずれか
        file_name (str): 保存するパス/ファイル名
        stereo (bool, optional): [ステレオの場合はTrue ]. Defaults to True.
        sampling_rate (int, optional): [サンプリング周波数]. Defaults to 44100.
    """
    if type(input_data) == bytes:
        data = input_data
    if type(input_data) == np.ndarray:
        data = struct.pack("h" * len(input_data), *input_data)

    w = wave.Wave_write(file_name)
    channel: int = 2 if stereo == True else 1
    p = (channel, 2, sampling_rate, len(input_data), 'NONE', 'not compressed')
    w.setparams(p)
    w.writeframes(input_data)
    w.close()


def mixSounds(sounds_list: List[AudioSegment], save_path: str):
    """
    引数に与えたリストに含まれる音をミックスする
    """
    mixed_sound = sounds_list[0]
    for sound in sounds_list[1:]:
        mixed_sound = mixed_sound.overlay(sound)

    mixed_sound.export(save_path, format='wav')


def extractOneEarSound(sound_data: bytes, direction: int):
    """ステレオの音データから片耳の音を抽出する

    Args:
        sound_data (bytes): [description]
        direction (int): [description]

    Returns:
        [type]: [description]
    """
    data: np.ndarray[np.int16] = np.frombuffer(sound_data, dtype='int16')
    if direction == 0:
        # 左側のサウンドを抽出
        int16data = data[::2]
    else:
        # 右側のサウンドを抽出
        int16data = data[1::2]
    return int16data


def soundLevelRegulation(input_data: Union[str, bytes, np.ndarray], range: int = 32767) -> bytes:
    """音データを正規化する

    Args:
        input_data (Union[str, bytes, np.ndarray]): ファイルパス、バイトデータ、ndarray[int16]のいずれかを入力とする
        range (int, optional): 音データの大きさの最大値を設定. Defaults to 32767.

    Returns:
        bytes: [description]
    """
    if type(input_data) == str:  # sound_data がファイルまでのパスの場合
        wf: wave.Wave_read = wave.open(input_data, mode='rb')
        buf: bytes = wf.readframes(-1)
        data: np.ndarray[np.int16] = np.frombuffer(buf, dtype='int16')

    if type(input_data) == bytes:
        data: np.ndarray[np.int16] = np.frombuffer(input_data, dtype='int16')

    if type(input_data) == np.ndarray:
        data: np.ndarray[np.int16] = input_data
    max_vol: np.int16 = np.amax(data)
    min_vol: np.int16 = np.amin(data)

    if abs(max_vol) >= abs(min_vol):
        multiple: float = range/max_vol
    else:
        multiple: float = range/abs(min_vol)
    data = np.floor(data*multiple).astype(np.int16)
    return struct.pack("h" * len(data), *data)


def createReverbSound(sound_file_path: str, attenuation_rate: float, delay_time: int, repeat_time: int):
    """リバーブをかけるエフェクト　未完成

    Args:
        sound_file_path (str): [description]
        attenuation_rate (float): [description]
        delay_time (int): [description]
        repeat_time (int): [description]

    Returns:
        [type]: [description]
    """
    wf = wave.open(sound_file_path, "rb")

    fs = wf.getframerate()      # サンプリング周波数
    length = wf.getnframes()    # 総フレーム数
    data: np.ndarray[np.int16] = np.frombuffer(
        wf.readframes(-1), dtype="int16")  # -1 - +1に正規化
    # # a:float = 0.6      # 減衰率
    # d:int = 20000    # 遅延時間（単位：サンプル）
    # repeat_time:int = 6   # リピート回数
    # return data
    combined_sound = np.zeros(len(data))
    for n in range(len(data)):
        combined_sound[n] = data[n]
        # 元のデータに残響を加える
        for i in range(1, repeat_time+1):
            m = int(n - i * delay_time*2)
            if m >= 0:
                # i*dだけ前のデータを減衰させた振幅を加える
                combined_sound[n] += (attenuation_rate ** i) * data[m]
    max_vol: np.float64 = np.amax(combined_sound)
    min_vol: np.float64 = np.amin(combined_sound)
    if abs(max_vol) >= abs(min_vol):
        multiple: float = (2**15-1)/max_vol
    else:
        multiple: float = (2**15-1)/abs(min_vol)
    regulated_data = np.floor(data*multiple).astype(np.int16)
    return regulated_data
