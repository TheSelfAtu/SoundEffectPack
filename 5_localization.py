from pydub import AudioSegment
import wave
import numpy as np
import struct
from common import createWav,mixSounds,extractOneEarSound

# 左耳の音と右耳の音を任意のボリュームで結合する
def combineLeftAndRightSounds(left_sound,right_sound,left_vol_ratio:float,right_vol_ratio:float):
    combined_sound = np.zeros(len(left_sound)+len(right_sound))
    for i in range(len(right_sound)+len(left_sound)):
        if i % 2 == 0:
            # 左耳の音の音量を調整
            combined_sound[i] = left_sound[i//2] * left_vol_ratio
        else:
             # 右耳の音の音量を調整
            combined_sound[i] = right_sound[i//2] * right_vol_ratio
    return combined_sound

# backing_gt_left
wf:wave.Wave_read = wave.open("4_Result/backing_gt_left.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = combineLeftAndRightSounds(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,0.3)
combined_sound = np.floor(combined_sound).astype(np.int64)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"5_Result/adjusted_backing_gt_left.wav")
wf.close()


# backing_gt_right
wf:wave.Wave_read = wave.open("4_Result/backing_gt_right.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = combineLeftAndRightSounds(extractOneEarSound(buf,0),extractOneEarSound(buf,1),0.3,1)
combined_sound = np.floor(combined_sound).astype(np.int64)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"5_Result/adjusted_backing_gt_right.wav")
wf.close()

# bass
wf:wave.Wave_read = wave.open("4_Result/bass.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = combineLeftAndRightSounds(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,1)
combined_sound = np.floor(combined_sound).astype(np.int64)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"5_Result/adjusted_bass.wav")
wf.close()

# drum
wf:wave.Wave_read = wave.open("4_Result/drum.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = combineLeftAndRightSounds(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,1)
combined_sound = np.floor(combined_sound).astype(np.int64)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"5_Result/adjusted_drum.wav")
wf.close()

# hs
wf:wave.Wave_read = wave.open("4_Result/hs.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = combineLeftAndRightSounds(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,1)
combined_sound = np.floor(combined_sound).astype(np.int64)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"5_Result/adjusted_hs.wav")
wf.close()

#lead_gt
wf:wave.Wave_read = wave.open("4_Result/lead_gt.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = combineLeftAndRightSounds(extractOneEarSound(buf,0),extractOneEarSound(buf,1),0.7,1)
combined_sound = np.floor(combined_sound).astype(np.int64)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"5_Result/adjusted_lead_gt.wav")
wf.close()

# strings
wf:wave.Wave_read = wave.open("4_Result/strings.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = combineLeftAndRightSounds(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,0.7)
combined_sound = np.floor(combined_sound).astype(np.int64)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"5_Result/adjusted_strings.wav")
wf.close()


backing_gt_left = AudioSegment.from_file("5_Result/adjusted_backing_gt_left.wav")
backing_gt_right = AudioSegment.from_file("5_Result/adjusted_backing_gt_left.wav")
bass = AudioSegment.from_file("5_Result/adjusted_bass.wav")[5000:]
drum = AudioSegment.from_file("5_Result/adjusted_drum.wav")[3000:]
hs = AudioSegment.from_file("5_Result/adjusted_hs.wav")
lead_gt = AudioSegment.from_file("5_Result/adjusted_lead_gt.wav")
strings = AudioSegment.from_file("5_Result/adjusted_strings.wav")

sounds_list:list = []
sounds_list.append(backing_gt_left) 
sounds_list.append(bass) 
sounds_list.append(drum) 
sounds_list.append(hs) 
sounds_list.append(lead_gt) 
sounds_list.append(strings)


mixSounds(sounds_list,"5_Result/result.wav")
