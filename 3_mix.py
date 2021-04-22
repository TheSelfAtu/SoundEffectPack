from typing import List
from pydub import AudioSegment
from common import plotSoundData
from common import mixSounds

backing_gt_left :AudioSegment= AudioSegment.from_file("music/sm_backing_gt_left.wav")
backing_gt_right :AudioSegment= AudioSegment.from_file("music/sm_backing_gt_left.wav")
bass :AudioSegment= AudioSegment.from_file("music/sm_bass.wav")[5000:]
drum :AudioSegment= AudioSegment.from_file("music/sm_drum.wav")[3000:]
hs :AudioSegment= AudioSegment.from_file("music/sm_hs.wav")
lead_gt :AudioSegment= AudioSegment.from_file("music/sm_lead_gt.wav")
strings :AudioSegment= AudioSegment.from_file("music/sm_strings.wav")

sounds_list:List[AudioSegment] = []
sounds_list.append(backing_gt_left) 
sounds_list.append(bass) 
sounds_list.append(drum) 
sounds_list.append(hs) 
sounds_list.append(lead_gt) 
sounds_list.append(strings)

mixSounds(sounds_list,"3_Result/result.wav")

plotSoundData("3_Result/result.wav")


