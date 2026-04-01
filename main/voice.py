# coding: gbk
import math
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip
from scipy.io.wavfile import write
import parselmouth

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
        self.wave = None
        self.sample_rate = 0.0
        self.wav = None
        self.synthesizer_path = SYNTHESIZER_PATH
        self.init_synthesizer()
        self.init_vocoder()
        self.init_encoder()
        self.init_wav()
        self.init_device(Synthesizer.sample_rate)

    def init_synthesizer(self):
        self.synthesizer = Synthesizer(Path(self.synthesizer_path))

    def init_encoder(self):
        encoder.load_model(Path(ENCODER_PATH))

    def init_vocoder(self):
        self.vocoder = gan_vocoder
        model_config_fpaths = list(Path(VOCODER_PATH).parent.rglob("*.json"))
        model_config_fpath = None
        if len(model_config_fpaths) > 0:
            model_config_fpath = model_config_fpaths[0]
        self.vocoder.load_model(Path(VOCODER_PATH), model_config_fpath)

    def init_device(self, sample_rate):
        output_devices = []
        for device in sd.query_devices():
            try:
                sd.check_output_settings(device=device["name"], samplerate=sample_rate)
                output_devices.append(device["name"])
            except Exception as e:
                print(e)
        if len(output_devices) == 0:
            # print("warning: there is no output device avaliable.")
            output_devices.append(None)
        sd.default.device = (None, output_devices[0])

    def init_wav(self):
        self.wav = Synthesizer.load_preprocess_wav(VOICE_PATH)
        # print("Done!")

    def synthesize_vocode(self, prompt):
        # TODO
        if not encoder.is_loaded():
            self.init_encoder()
        encoder_wav = encoder.preprocess_wav(self.wav)
        embed = encoder.embed_utterance(encoder_wav, return_partials=True)[0]
        texts = prompt.split("\n")
        punctuation = '！，。、,：？…,!:?~——'
        processed_texts = []
        for text in texts:
            for processed_text in re.sub(r'[{}]+'.format(punctuation), '\n', text).split(
                    '\n'):  # 把每一段话的标点符号用正则表达式替换为换行符，再通过换行符分割存储到texts列表
                if processed_text:
                    processed_texts.append(processed_text.strip())
        texts = processed_texts
        # 处理embed
        embeds = [embed] * len(texts)
        # 生成频谱
        if not self.synthesizer.is_loaded():
            self.init_synthesizer()
        specs = self.synthesizer.synthesize_spectrograms(texts, embeds, style_idx=-1, min_stop_token=5,
                                                         steps=9 * 200)  # style, accurency, length
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

    def synthesize_video(self):
        write("output.wav", Synthesizer.sample_rate, self.wave)
        sound = parselmouth.Sound(self.wave)
        pitch = sound.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        time_points = pitch.xs()
        start_bounds = []
        end_bounds = []
        is_in = True
        j = 0
        # print(len(pitch_values))
        for i in pitch_values:
            j += 1
            if i == 0 and not is_in:
                end_bounds.append(j / 100)
                is_in = True
            elif i != 0:
                if is_in:
                    start_bounds.append(j / 100)
                is_in = False
            print(i)
        print(len(start_bounds))
        bounds = zip(start_bounds, end_bounds)
        audio = AudioFileClip("output.wav")
        print("ready!")
        time = sound.duration
        origin_video = VideoFileClip("video/silence.mp4")
        duration = origin_video.duration
        n = math.ceil(time / duration)
        videos = [origin_video for i in range(n)]
        temp_video = concatenate_videoclips(videos)
        temp_video = temp_video.subclip(0, time)
        last_end = 0
        final_videos = []
        for start, end in bounds:
            # print(start,end)
            clip_video = temp_video.subclip(last_end, start)
            last_end = end
            final_videos.append(clip_video)

            new_video = (VideoFileClip("video/mouth.mp4")
                         .fx(vfx.speedx, 0.28 / (end - start)))
            new_video.set_fps(clip_video.fps)
            final_videos.append(new_video)
        final_video = concatenate_videoclips(final_videos)
        final_video = final_video.set_audio(audio)
        # final_video.preview()
        final_video.write_videofile("final.mp4")
        print("ok")

    def speak(self):
        try:
            sd.play(self.wave, self.sample_rate)
            sd.wait()
        except Exception as e:
            print(e)
