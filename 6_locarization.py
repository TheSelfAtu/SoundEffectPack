from typing import Any
from pydub import AudioSegment
import wave,array
import numpy as np
import struct
from common import createWav,mixSounds,extractOneEarSound

def delayOneSound(left_sound,right_sound,direction:int,delay_frame:int):
    """右耳もしくは左耳の音を遅らせることによりPANを振る

    Args:
        left_sound ([type]): [左耳の音]
        right_sound ([type]): [右耳の音]
        direction (int): [左耳の音を遅らせる場合は０、右耳の音を遅らせる場合は１]
        delay_frame (int): [遅らせるフレーム数]

    """
    combined_sound = np.zeros(len(left_sound)+len(right_sound)+delay_frame*2)
    if direction == 0:
        # 左耳の音を遅らせる
        for i in range(len(left_sound)):
            combined_sound[i*2] = left_sound[i]
        for i in range(len(right_sound)):
            combined_sound[i*2+1+delay_frame*2] = right_sound[i]
    else:
        # 右耳の音を遅らせる
        for i in range(len(left_sound)):
            combined_sound[i*2+delay_frame*2] = left_sound[i]
        for i in range(len(right_sound)):
            combined_sound[i*2+1] = right_sound[i]
    return combined_sound

# backing_gt_left
wf:wave.Wave_read = wave.open("4_Result/backing_gt_left.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = delayOneSound(extractOneEarSound(buf,0),extractOneEarSound(buf,1),0,40)
combined_sound = np.floor(combined_sound).astype(np.int16)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"6_Result/adjusted_backing_gt_left.wav")


# backing_gt_right
wf:wave.Wave_read = wave.open("4_Result/backing_gt_right.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = delayOneSound(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,40)
combined_sound = np.floor(combined_sound).astype(np.int16)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"6_Result/adjusted_backing_gt_right.wav")
wf.close()

# bass
wf:wave.Wave_read = wave.open("4_Result/bass.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = delayOneSound(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,0)
combined_sound = np.floor(combined_sound).astype(np.int16)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"6_Result/adjusted_bass.wav")
wf.close()

# drum
wf:wave.Wave_read = wave.open("4_Result/drum.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = delayOneSound(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,0)
combined_sound = np.floor(combined_sound).astype(np.int16)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"6_Result/adjusted_drum.wav")
wf.close()

# hs
wf:wave.Wave_read = wave.open("4_Result/hs.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = delayOneSound(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,0)
combined_sound = np.floor(combined_sound).astype(np.int16)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"6_Result/adjusted_hs.wav")
wf.close()

#lead_gt
wf:wave.Wave_read = wave.open("4_Result/lead_gt.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = delayOneSound(extractOneEarSound(buf,0),extractOneEarSound(buf,1),1,10)
combined_sound = np.floor(combined_sound).astype(np.int16)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"6_Result/adjusted_lead_gt.wav")
wf.close()

# strings
wf:wave.Wave_read = wave.open("4_Result/strings.wav",'rb')
buf:bytes = wf.readframes(-1)
combined_sound = delayOneSound(extractOneEarSound(buf,0),extractOneEarSound(buf,1),0,10)
combined_sound = np.floor(combined_sound).astype(np.int16)
createWav(struct.pack("h" * len(combined_sound), *combined_sound),"6_Result/adjusted_strings.wav")
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


mixSounds(sounds_list,"6_Result/result.wav")
