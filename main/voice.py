#coding: gbk
###################################################################################
#作者：周故意太湖给他
#简介：一款接入了EdgeGPT(newbing)和MockingBird实时语音克隆模型的丁真风味聊天机器人。
#鸣谢：acheong08、babysor
###################################################################################
from pathlib import Path
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder.hifigan import inference as gan_vocoder
import numpy as np
import re
import sounddevice as sd

VOICE_PATH = "./voice/dz.wav"
SYNTHESIZER_PATH = "./synthesizer/saved_models/dingzhen.pt"
VOCODER_PATH = "./vocoder/saved_models/pretrained/g_hifigan.pt"
ENCODER_PATH = "./encoder/saved_models/pretrained.pt"

class DingZhen:
    def __init__(self):
        self.synthesizer = None
        self.vocoder = None
        self.init_synthesizer()
        self.init_vocoder()
        self.init_encoder()
        self.init_wav()
        self.init_device(Synthesizer.sample_rate)
    def init_synthesizer(self):
        self.synthesizer = Synthesizer(Path(SYNTHESIZER_PATH))
    def init_encoder(self):
        encoder.load_model(Path(ENCODER_PATH))
    def init_vocoder(self):
        self.vocoder = gan_vocoder
        model_config_fpaths = list(Path(VOCODER_PATH).parent.rglob("*.json"))
        model_config_fpath = None
        if len(model_config_fpaths) > 0:
            model_config_fpath = model_config_fpaths[0]
        self.vocoder.load_model(Path(VOCODER_PATH), model_config_fpath)
    def init_device(self,sample_rate):
        '''f'''
        output_devices = []
        for device in sd.query_devices():
           try:
               sd.check_output_settings(device=device["name"], samplerate=sample_rate)
               output_devices.append(device["name"])
           except Exception as e:
               print(e)
        if len(output_devices) == 0:
           print("warning: there is no output device avaliable.")
           output_devices.append(None)
        sd.default.device = (None, output_devices[0])
    def init_wav(self):
        self.wav = Synthesizer.load_preprocess_wav(VOICE_PATH)
        print("Done!")
    def synthesize_vocode(self, prompt):
        #TODO 
        if not encoder.is_loaded():
            self.init_encoder()
        encoder_wav = encoder.preprocess_wav(self.wav)
        embed = encoder.embed_utterance(encoder_wav, return_partials=True)[0]
        texts = prompt.split("\n")
        punctuation = '！，。、,：？' 
        processed_texts = []
        for text in texts:
          for processed_text in re.sub(r'[{}]+'.format(punctuation), '\n', text).split('\n'): #把每一段话的标点符号用正则表达式替换为换行符，再通过换行符分割存储到texts列表
            if processed_text:
                processed_texts.append(processed_text.strip())
        texts = processed_texts
        #处理embed
        embeds = [embed] * len(texts)
        #生成频谱
        if not self.synthesizer.is_loaded():
            self.init_synthesizer()
        specs = self.synthesizer.synthesize_spectrograms(texts, embeds, style_idx=-1, min_stop_token=5, steps=9*200) #style, accurency, length
        breaks = [spec.shape[1] for spec in specs]
        spec = np.concatenate(specs, axis=1)
        if not self.vocoder.is_loaded():
            self.init_vocoder()
        def vocoder_progress(i, seq_len, b_size, gen_rate):
            real_time_factor = (gen_rate / Synthesizer.sample_rate) * 1000
            line = "Waveform generation: %d/%d (batch size: %d, rate: %.1fkHz - %.2fx real time)" \
                   % (i * b_size, seq_len * b_size, b_size, gen_rate, real_time_factor)
        wav, self.sample_rate = self.vocoder.infer_waveform(spec, progress_callback=vocoder_progress)
        b_ends = np.cumsum(np.array(breaks) * Synthesizer.hparams.hop_size)
        b_starts = np.concatenate(([0], b_ends[:-1]))
        wavs = [wav[start:end] for start, end, in zip(b_starts, b_ends)]
        breaks = [np.zeros(int(0.15 * self.sample_rate))] * len(breaks)
        wav = encoder.preprocess_wav(np.concatenate([i for w, b in zip(wavs, breaks) for i in (w, b)]))
        self.wave = wav / np.abs(wav).max() * 0.97
    def speak(self):
        try:
            sd.play(self.wave, self.sample_rate)
            sd.wait()
        except Exception as e:
            print(e)

