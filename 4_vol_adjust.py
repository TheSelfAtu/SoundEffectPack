from pydub import AudioSegment
from common import createWav,mixSounds,plotSoundData,soundLevelRegulation

sound_data:bytes =soundLevelRegulation("music/sm_backing_gt_left.wav")
createWav(sound_data,"4_Result/backing_gt_left.wav")

sound_data:bytes =soundLevelRegulation("music/sm_bass.wav")
createWav(sound_data,"4_Result/bass.wav")
sound_data:bytes =soundLevelRegulation("music/sm_backing_gt_right.wav")
createWav(sound_data,"4_Result/backing_gt_right.wav")
sound_data:bytes =soundLevelRegulation("music/sm_drum.wav")
createWav(sound_data,"4_Result/drum.wav")
sound_data:bytes =soundLevelRegulation("music/sm_hs.wav")
createWav(sound_data,"4_Result/hs.wav")
sound_data:bytes =soundLevelRegulation("music/sm_lead_gt.wav")
createWav(sound_data,"4_Result/lead_gt.wav")
sound_data:bytes =soundLevelRegulation("music/sm_strings.wav")
createWav(sound_data,"4_Result/strings.wav")

backing_gt_left = AudioSegment.from_file("4_Result/backing_gt_left.wav")
backing_gt_right = AudioSegment.from_file("4_Result/backing_gt_left.wav")
bass = AudioSegment.from_file("4_Result/bass.wav")[5000:]
drum = AudioSegment.from_file("4_Result/drum.wav")[3000:]
hs = AudioSegment.from_file("4_Result/hs.wav")
lead_gt = AudioSegment.from_file("4_Result/lead_gt.wav")
strings = AudioSegment.from_file("4_Result/strings.wav")

sounds_list:list = []
sounds_list.append(backing_gt_left) 
sounds_list.append(bass) 
sounds_list.append(drum) 
sounds_list.append(hs) 
sounds_list.append(lead_gt) 
sounds_list.append(strings)


mixSounds(sounds_list,"4_Result/result.wav")

plotSoundData("4_Result/result.wav")