import torch
import os
import re
import numpy as np
from pysndfx import AudioEffectsChain


class SileroModel:
    def __init__(self, filename, device='cpu', sample_rate=16000):
        self.device = device
        self.sample_rate = sample_rate
        self.model = torch.package.PackageImporter(
            filename).load_pickle("tts_models", "model")
        self.model.to(device)

        # post FX settings are BAYA_V2-SPECIFIC:
        self.postprocessor = (
            AudioEffectsChain()
            .compand(attack=0.005, decay=193, soft_knee=4.,
                     threshold=-20)  # compression to make the voice appear thicker
            # EQs are not crucial here actually
            .equalizer(210, q=1.2, db=1.55)
            .equalizer(534, q=3, db=3.5)
            .equalizer(6200, q=1, db=1.55)
            # scales the audio to be in [-1, 1]
            .normalize()
        )

    def apply_tts(self, text):
        preprocessed = self._preprocess(text)
        audio = self.model.apply_tts(preprocessed, self.sample_rate)[0]
        audio = audio.numpy()
        return self._postprocess(audio)

    def _preprocess(self, text):
        # BAYA_V2-SPECIFIC
        # because baya does not process ,! correctly
        return re.sub('\!|\,', '', text)

    def _postprocess(self, audio):
        return self.postprocessor(audio)
