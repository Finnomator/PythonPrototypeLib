from time import sleep_ms

from machine import Pin, PWM
from uasyncio import sleep_ms as sleep_ms_async

from ..abstract import notes_and_freqs as naf

from . import base_module


class Piezo(base_module.BaseModule):
    def __init__(self):
        self.piezo = PWM(Pin(22, Pin.OUT))
        self.piezo.freq(440)
        self.mute()

    def play_tone(self, tone: "Tone"):
        self.piezo.duty_u16(512)
        self.piezo.freq(tone.freq)
        sleep_ms(tone.duration_ms)
        self.mute()

    def play_tones(self, tones: list["Tone"]):
        for tone in tones:
            self.piezo.duty_u16(512)
            self.piezo.freq(tone.freq)
            sleep_ms(tone.duration_ms)
        self.mute()

    async def play_tone_async(self, tone: "Tone"):
        self.piezo.duty_u16(512)
        self.piezo.freq(tone.freq)
        await sleep_ms_async(tone.duration_ms)
        self.mute()

    async def play_tones_async(self, tones: list["Tone"]):
        self.piezo.duty_u16(512)
        for tone in tones:
            self.piezo.freq(tone.freq)
            await sleep_ms_async(tone.duration_ms)
        self.mute()

    def mute(self):
        self.piezo.duty_u16(0)

    def deinit(self):
        self.piezo.duty_u16(0)
        self.piezo.deinit()


class Tone:
    def __init__(self, note: str, freq: int, duration_ms: int = 200):
        """
        Create a tone
        freq: Frequency
        """
        self.note, self.freq, self.duration_ms = note, freq, duration_ms


class SampleTones:
    tones = sorted(
        [Tone(n, int(f)) for n, f in naf.tones.items()], key=lambda x: x.freq
    )

    @staticmethod
    def get_tone(note: str) -> Tone:
        return Tone(note, int(naf.tones[note]))
