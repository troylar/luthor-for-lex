# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not
# use this file except in compliance with the License. A copy of the
# License is located at:
#    http://aws.amazon.com/asl/
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, expressi
# or implied. See the License for the specific language governing permissions
# and limitations under the License.

import boto3
from contextlib import closing
import tempfile
import os
import logging
import sys
with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f

    import pygame

    # enable stdout
    sys.stdout = oldstdout


class Speaker(object):
    def __init__(self, **kwargs):
        self.voice = kwargs.pop("VoiceId", "Joanna")
        self.output_format = kwargs.pop("OutputFormat", "ogg_vorbis")
        self.chime_path = kwargs.pop("ChimePath",
                                     os.path.expanduser("~/.pollexy/.cache/chimes"))
        self.no_audio = kwargs.pop("NoAudio", False)
        self.is_audio_ready = False
        self.audio_file_path = ""

    def just_say(self, **kwargs):
        include_chime = kwargs.pop('IncludeChime', False)
        message = kwargs.pop('Message', '')
        voice_id = kwargs.pop('VoiceId', 'Joanna')
        self.generate_audio(Message=message, VoiceId=voice_id)
        self.speak(IncludeChime=include_chime)

    def generate_audio(self, **kwargs):
        message = kwargs.pop("Message", "")
        text_type = kwargs.pop("TextType", "text")
        voice = kwargs.pop("VoiceId", self.voice).capitalize()
        if not message:
            return
        if not self.no_audio:
            polly = boto3.client('polly')
            response = polly.synthesize_speech(
                Text=message,
                OutputFormat="ogg_vorbis",
                TextType=text_type,
                VoiceId=voice)

            fd, path = tempfile.mkstemp(suffix=".ogg")

            with closing(response["AudioStream"]) as stream:
                with open(path, 'wb') as file:
                    file.write(stream.read())

            self.audio_file_path = path
        self.message = message
        self.is_audio_ready = True

    def speak(self, **kwargs):
        include_chime = kwargs.get('IncludeChime', False)
        chime = kwargs.pop("Chime", "three_tone_chime")
        if not self.is_audio_ready:
            print("Nothing to say . . . call generate_audio() first")
            return
        if self.no_audio:
            print("No audio . . . speech would be:\n%s" % self.message)
            return "audio: %s"
        else:
            audio_file_to_play = kwargs.pop("AudioFilePath",
                                            self.audio_file_path)
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.init()
            pygame.mixer.init()
            if (include_chime):
                logging.info('chime={}/{}.wav'.format(self.chime_path, chime))
                pygame.mixer.music.load("%s/%s.wav" % (self.chime_path, chime))
                pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.load(audio_file_to_play)
            pygame.mixer.music.play(1)
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

    def cleanup(self):
        if (self.audio_file_path):
            os.unlink(self.audio_file_path)
            self.audio_file_path = ""
        self.message = ""
        self.is_audio_ready = False
