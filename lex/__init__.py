#!/usr/bin/python
import yaml
import boto3
import os
import pprint
import time
import speech_recognition as sr
import uuid
import logging
from speaker.speaker import Speaker
from botocore.exceptions import ClientError


class LexSlotManager:
    def __init__(self, **kwargs):
        self.client = boto3.client('lex-models')
        self.config_path = kwargs.get('ConfigPath')

    def load(self):
        slots = {}
        for f in os.listdir(self.config_path):
            config_file = os.path.join(self.config_path, f)
            if not config_file.endswith('yaml') \
               and not config_file.endswith('yml'):
                continue
            with open(config_file, 'r') as stream:
                slots.update(yaml.load(stream))
        return slots

    def get_slot_type(self, **kwargs):
        try:
            s = self.client.get_slot_type(
                name=kwargs.get('Name'),
                version=kwargs.get('Version', '$LATEST'))
            return s

        except ClientError as e:
            if e.response and \
               e.response['Error']['Code'] == 'NotFoundException':
                return None
            else:
                raise

    def upsert(self, slot):
        args = {}
        for l in list(slot.keys()):
            args[l] = slot[l]
        print('Upserting slot: {}'.format(slot['name']))
        current_slot = self.get_slot_type(
            Name=slot['name'],
            Version='$LATEST'

        )
        if current_slot:
            args['checksum'] = current_slot['checksum']
        return self.client.put_slot_type(**args)

    def create_version(self, slot):
        current_slot = self.get_slot_type(
            Name=slot['name'],
            Version='$LATEST'
        )
        if current_slot:
            current_slot['checksum'] = current_slot['checksum']
        print('Creating new version of slot: {}'.format(slot['name']))
        resp = self.client.create_slot_type_version(
            name=slot['name'],
            checksum=slot['checksum']
        )
        slot['version'] = str(resp['version'])
        print('Slot version = {}'.format(slot['version']))
        return slot


class LexIntentManager:
    def __init__(self, **kwargs):
        self.client = boto3.client('lex-models')
        self.config_path = kwargs.get('ConfigPath')

    def load(self):
        intents = {}
        for f in os.listdir(self.config_path):
            config_file = os.path.join(self.config_path, f)
            if not config_file.endswith('yaml') \
               and not config_file.endswith('yml'):
                continue
            with open(config_file, 'r') as stream:
                intents.update(yaml.load(stream))
        return intents

    def get_intent(self, **kwargs):
        try:
            i = self.client.get_intent(
                name=kwargs.get('Name'),
                version=kwargs.get('Version'))
            return i

        except ClientError as e:
            if e.response and \
               e.response['Error']['Code'] == 'NotFoundException':
                return None
            else:
                raise

    def create_version(self, intent):
        current_intent = self.get_intent(
            intent['name'],
            '$LATEST'
        )
        if current_intent:
            current_intent['checksum'] = current_intent['checksum']
        print('Creating new version of intent: {}'.format(intent['name']))
        resp = self.client.create_intent_version(
            name=intent['name'],
            checksum=intent['checksum']
        )
        intent['version'] = str(resp['version'])
        print('Intent version = {}'.format(intent['version']))
        return intent

    def upsert(self, intent):
        args = {}
        for l in list(intent.keys()):
            args[l] = intent[l]
            if 'slots' in list(intent.keys()):
                for i in intent['slots']:
                    if i['slotType'].startswith('AMAZON.'):
                        continue
                    if 'slotTypeVersion' in list(i.keys()) and \
                            i['slotTypeVersion'] == '$LATEST':
                        print('Getting slot versions for ' + i['name'])
                        slots = self.client.get_slot_type_versions(
                            name=i['slotType'], maxResults=50)['slotTypes']
                        if len(slots) > 0:
                            latestVersion = slots[len(slots)-1]['version']
                            print('Latest slot version = {}' \
                                .format(latestVersion))
                            i['slotTypeVersion'] = latestVersion
        print('Upserting intent: {}'.format(intent['name']))
        current_intent = self.get_intent(
            Name=intent['name'],
            Version='$LATEST')
        if current_intent:
            args['checksum'] = current_intent['checksum']
        return self.client.put_intent(**args)


class LexBotManager:
    def __init__(self, **kwargs):
        self.client = boto3.client('lex-models')
        self.config_path = kwargs.get('ConfigPath')
        pass

    def get_alias(self, botName, aliasName):
        try:
            print('get_alias {}:{}'.format(botName, aliasName))
            resp = self.client.get_bot_alias(
                name=aliasName,
                botName=botName
            )
            if resp:
                print('get_alias checksum = {}'.format(resp['checksum']))
                return resp
        except ClientError as e:
            if e.response and \
               e.response['Error']['Code'] == 'NotFoundException':
                return None
            else:
                raise

    def get_bot(self, **kwargs):
        self.name = kwargs.get('Name')
        self.versionOrAlias = kwargs.get('VersionOrAlias', '$LATEST')
        print('Getting bot {}:{}'.format(self.name, self.versionOrAlias))
        try:
            client = boto3.client('lex-models')
            resp = client.get_bot(
                name=self.name,
                versionOrAlias=self.versionOrAlias
            )
            if resp:
                print('get_bot checksum = {}'.format(resp['checksum']))
                return resp
        except ClientError as e:
            if e.response and \
               e.response['Error']['Code'] == 'NotFoundException':
                return None
            else:
                raise

    def load_bots(self):
        bots = {}
        for f in os.listdir(self.config_path):
            config_file = os.path.join(self.config_path, f)
            if not config_file.endswith('yaml') \
               and not config_file.endswith('yml'):
                continue
            with open(config_file, 'r') as stream:
                bots.update(yaml.load(stream))
        return bots

    def upsert(self, bot):
        args = {}
        for l in list(bot.keys()):
            args[l] = bot[l]
        for i in bot['intents']:
            if i['intentVersion'] == '$LATEST':
                print(i['intentVersion'])
                intents = self.client.get_intent_versions(
                    name=i['intentName'], maxResults=50)['intents']
                print(intents)
                if len(intents) > 0:
                    latestVersion = intents[len(intents)-1]['version']
                    print('Latest intent version = {}'.format(latestVersion))
                    i['intentVersion'] = latestVersion
        print('Creating bot: {}'.format(bot['name']))
        current_bot = self.get_bot(
            Name=bot['name']
        )
        if current_bot:
            args['checksum'] = current_bot['checksum']
        resp = self.client.put_bot(**args)
        while resp['status'] == 'BUILDING':
            print('Bot is building . . .')
            time.sleep(10)
            resp = self.get_bot(Name=bot['name'])
        print('Status: {}'.format(resp['status']))
        if resp['status'] == 'FAILED':
            pprint.pprint(resp)
        return resp['status'], bot

    def create_version(self, bot):
        current_bot = self.get_bot(
            Name=bot['name']
        )
        if current_bot:
            bot['checksum'] = current_bot['checksum']
        print('Creating new version')
        resp = self.client.create_bot_version(
            name=bot['name'],
            checksum=bot['checksum']
        )
        bot['version'] = str(resp['version'])
        print('Version = {}'.format(bot['version']))
        time.sleep(2)
        return bot

    def update_alias(self, bot, **kwargs):
        alias = kwargs.get('Alias', 'LATEST')
        print('Updating alias {} for bot {}:{}' \
              .format(alias, bot['name'], bot['version']))
        current_bot = self.get_alias(bot['name'], alias)
        resp = {}
        if current_bot:
            print('Alias exists . . . updating.')
            print('name={}, version={}, checksum={}' \
                  .format(alias,
                          current_bot['botVersion'],
                          current_bot['checksum']))
            resp = self.client.put_bot_alias(
                checksum=current_bot['checksum'],
                name=alias,
                botName=current_bot['botName'],
                botVersion=current_bot['botVersion']
            )
        else:
            print('Alias does NOT exist . . . creating.')
            try:
                resp = self.client.put_bot_alias(
                   name=alias,
                   botName=bot['name'],
                   botVersion=bot['version']
                )
            except Exception as e:
                pprint.pprint(e)
                print("Error creating bot: {}".format(resp))
        print('Alias updated')

    def delete_bot(self, **kwargs):
        bot_name = kwargs.get('Name')
        aliases = self.client.get_bot_aliases(
            botName=bot_name)
        for a in aliases['BotAliases']:
            print('Deleting {}:{}'.format(bot_name, a))
            pprint.pprint(a)
            self.client.delete_bot_alias(
                botName=bot_name,
                name=a['name'])
            time.sleep(2)
        print('Deleting {}'.format(bot_name))
        try:
            self.client.delete_bot(name=bot_name)
            print('Deleted bot')
        except ClientError as e:
            if e.response and \
               e.response['Error']['Code'] == 'NotFoundException':
                print("Bot doesn't exist: {}".format(bot_name))
            else:
                raise


class LexBot(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get('Username')
        self.alias = kwargs.get('Alias')
        self.no_audio = kwargs.get('NoAudio')
        self.bot_name = kwargs.get('BotName')
        self.voice_id = kwargs.get('VoiceId', 'Joanna')
        self.last_response = {}
        self.client = boto3.client('lex-runtime')
        self.restart = False
        self.ice_breaker = kwargs.get('IceBreaker')
        self.load_bot()
        self.next_intent = ""
        self.log = logging.getLogger("LexBot-{}".format(self.bot_name))
        if os.environ.get('LOG_LEVEL') == 'DEBUG':
            self.log.setLevel(logging.DEBUG)

    def load_bot(self):
        try:
            m = __import__('lex.bots.{}'.format(self.bot_name),
                           fromlist=["*"])
            self.bot = getattr(m, self.bot_name)(self)
        except Exception as e:
            print("Error loading {} bot plugin".format(self.bot_name))
            print(e)
            m = __import__('lex.bots', fromlist=["BaseBot"])
            print(m)
            self.bot = getattr(m, 'BaseBot')()
            print(self.bot)
        self.bot.register()

    def send_response(self, data, **kwargs):
        text_mode = bool(kwargs.get('TextMode', False))
        if self.no_audio or text_mode:
            self.post_text(data)
        else:
            self.send_content(data)
        if self.is_fulfilled:
            self.bot.on_fulfilled()

        elif self.is_failed:
            self.bot.on_failed()

    def send_content(self, audio_file_path):
        f = open(audio_file_path, 'rb')
        self.last_response = self.client.post_content(
                botName=self.bot_name,
                botAlias=self.alias,
                userId=self.username,
                inputStream=f,
                accept='text/plain; charset=utf-8',
                contentType="audio/l16; rate=16000; channels=1")
        if self.needs_intent:
            self.bot.on_needs_intent()

    def post_text(self, text):
        self.last_response = self.client.post_text(botName=self.bot_name,
                                                   botAlias=self.alias,
                                                   userId=self.username,
                                                   inputText=text)
        self.bot.on_response()

    @property
    def slots(self):
        if self.last_response and \
                'slots' in list(self.last_response.keys()):
                    return self.last_response['slots']

    @property
    def resp_meta(self):
        if self.last_response and \
                'ResponseMetadata' in list(self.last_response.keys()):
                    return self.last_response['ResponseMetadata']

    @property
    def needs_slot(self):
        return 'dialogState' in list(self.last_response.keys()) and \
                self.last_response['dialogState'] == 'ElicitSlot'

    @property
    def needs_intent(self):
        return 'dialogState' in list(self.last_response.keys()) and \
                self.last_response['dialogState'] == 'ElicitIntent'

    @property
    def last_thing_said(self):
        if self.no_audio:
            return self.text_response
        elif self.last_response and \
                'inputTranscript' in list(self.last_response.keys()):
                    return self.last_response['inputTranscript']

    @property
    def is_done(self):
        return self.is_fulfilled or self.is_failed

    @property
    def is_failed(self):
        return self.last_state == 'Failed'

    @property
    def is_fulfilled(self):
        return self.last_state == 'ReadyForFulfillment'

    @property
    def last_state(self):
        if self.last_response and 'dialogState' in list(self.last_response.keys()):
            return self.last_response['dialogState']

    @property
    def last_intent(self):
        if self.last_response and 'intentName' in list(self.last_response.keys()):
            return self.last_response['intentName']

    def get_user_input(self):
        self.log.debug('Getting user_input for {}'.format(self.bot_name))
        self.log.debug('Bot restart={}'.format(self.restart))
        message = ""
        if self.restart:
            message = "How can I help you?"
            self.log.debug('Restarting bot, message={}'.format(message))
            if self.ice_breaker:
                self.log.debug('Ice breaker: "{}"'.format(self.ice_breaker))
                self.send_response(self.ice_breaker)
            self.log.debug('Disabling restart flag')
            self.restart = False
        elif self.last_response and 'message' in list(self.last_response.keys()):
            message = self.last_response['message']
            self.log.debug('Bot is running: {}'.format(message))
        elif self.last_response and \
                not self.is_fulfilled and not self.is_failed:
            self.log.debug('Something happened')
            message = "Something is wrong."
        self.output(Message=message)
        if self.no_audio:
            self.text_response = input('> ')
            self.log.debug('Sending: {}'.format(self.text_response))
            self.send_response(self.text_response)
        else:
            audio_file_path = self.listen()
            self.send_response(audio_file_path)
            os.remove(audio_file_path)
        self.last_message = message

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone(device_index=1,
                           sample_rate=16000, chunk_size=512) as source:
            # r.adjust_for_ambient_noice(source)
            print('Listening . . .')
            audio = r.listen(source)
            print('Done listening. Processing . . .')
            filename = os.path.join('/tmp', str(uuid.uuid4()))
            with open(filename, 'wb') as f:
                f.write(audio.get_wav_data())
            return filename

    def output(self, **kwargs):
        msg = kwargs.get('Message')
        if self.no_audio:
            self.write(Message=msg)
        else:
            self.speak(Message=msg)

    def write(self, **kwargs):
        msg = kwargs.get('Message')
        print('{}\n'.format(msg))

    def speak(self, **kwargs):
        msg = kwargs.get('Message')
        s = Speaker(VoiceId=self.voice_id)
        s.generate_audio(Message=msg, TextType='text')
        s.speak(IncludeChime=False)


class LexBotHistoryItem(object):
    def __init__(self, **kwargs):
        self.bot_name = kwargs.get('BotName')
        self.response = kwargs.get('Response')
        self.post_text = kwargs.get('PostText')


class LexPlayer(object):
    def __init__(self, **kwargs):
        self.bots = {}
        self.history = []
        self.ice_breaker = kwargs.get('IceBreaker', '')
        self.bot_names = kwargs.get('BotNames').split(',')
        self.start_bot_name = kwargs.get('StartBot', self.bot_names[0])
        self.active_bot_name = self.start_bot_name
        self.username = str(uuid.uuid4())
        self.alias = kwargs.get('Alias')
        self.no_audio = bool(kwargs.get('NoAudio', False))
        self.history = []
        self.voice_id = kwargs.get('VoiceId', 'Joanna')
        self.client = boto3.client('lex-runtime')
        introduction = kwargs.get('Introduction', '')
        if kwargs.get('BotsRequired'):
            self.bots_required = kwargs.get('BotsRequired').split(',')
        else:
            self.bots_required = []
        self.bot_stack = []
        self.load_bots()
        self.log = logging.getLogger("LexPlayer")
        if os.environ.get('LOG_LEVEL') == 'DEBUG':
            self.log.setLevel(logging.DEBUG)
        if introduction:
            self.active_bot.output(Message=introduction)
        if self.ice_breaker:
            self.send_response(self.ice_breaker, TextMode=True)

    def add_to_history(self, **kwargs):
        b = LexBotHistoryItem()
        b.bot_name = kwargs.get('BotName')
        b.response = kwargs.get('Response')
        b.post_text = kwargs.get('PostText')
        self.history.append(b)

    def load_bots(self):
        for b in self.bot_names:
            lb = LexBot(BotName=b,
                        NoAudio=self.no_audio,
                        Alias=self.alias,
                        VoiceId=self.voice_id,
                        Username=self.username)
            self.bots[b] = lb

    @property
    def is_done(self):
        if len(self.bots_required) > 0:
            for b in self.bots_required:
                bot = self.bots[b]
                if not bot.is_fulfilled and not bot.is_failed:
                    return False

        return True and not self.need_something_else

    @property
    def active_bot(self):
        return self.bots[self.active_bot_name]

    def send_response(self, data, **kwargs):
        self.active_bot.send_response(data, **kwargs)

    def switch_bot(self, **kwargs):
        restart = bool(kwargs.get('Restart', False))
        if self.active_bot_name:
            self.bot_stack.append(self.active_bot_name)
            self.bots[self.active_bot_name].bot.on_transition_out()
        self.active_bot_name = kwargs.get('BotName')
        self.bots[self.active_bot_name].bot.on_transition_in()
        self.bots[self.active_bot_name].restart = restart
        self.log.debug('Switching bot to {}, Restart={}'
                       .format(self.active_bot_name,
                               self.bots[self.active_bot_name].restart))

    @property
    def is_all_done(self):
        if not self.last_intent == 'PollexyAnythingElseIntent':
            return None
        if self.last_state == 'ReadyForFulfillment':
            return False
        return 'message' in list(self.last_response.keys()) and \
            self.last_response['message'] == "OK, we'll chat later." and \
            self.last_intent == 'PollexyAnythingElseIntent'

    @property
    def need_something_else(self):
        return self.last_state == 'ReadyForFulfillment' and \
            self.last_intent == 'PollexyAnythingElseIntent'

    @property
    def last_thing_said(self):
        return self.active_bot.last_thing_said

    @property
    def last_state(self):
        return self.active_bot.last_state

    @property
    def last_intent(self):
        return self.active_bot.last_intent

    @property
    def last_response(self):
        return self.active_bot.last_response

    def get_user_input(self):
        self.active_bot.get_user_input()
        if self.active_bot.is_failed or self.active_bot.needs_intent or \
                self.active_bot.needs_slot:
            self.log.debug('{} status is ElicitIntent or ElicitSlot: {}'
                           .format(self.active_bot_name, self.last_thing_said))
            self.log.debug('Checking other bots')
            for b in self.bots:
                if b == self.active_bot_name:
                    continue
                self.log.debug('Checking bot {}'.format(b))
                self.bots[b].send_response(self.last_thing_said, TextMode=True)
                if not self.bots[b].needs_intent:
                    self.log.debug('Found response from {}'
                                   .format(b))
                    if not self.bots[b].is_fulfilled:
                        self.log.debug('Switching to {}'.format(b))
                        self.switch_bot(BotName=b, Restart=False)
                    else:
                        self.log.debug('Bot {} fulfilled. Continuing with {}'
                                       .format(b, self.active_bot_name))
                        self.active_bot.bot.on_transition_in()
                    break
        elif self.active_bot.is_fulfilled or self.active_bot.is_failed:
            if self.active_bot.next_intent:
                self.send_response(self.active_bot.next_intent,
                                   TextMode=True)
            else:
                self.log.debug('{} fulfilled.'.format(self.active_bot_name))
                if len(self.bot_stack) > 0:
                    self.switch_bot(BotName=self.bot_stack.pop(), Restart=True)
                else:
                    done = True
                    if len(self.bots_required) > 0:
                        for b in self.bots_required:
                            if not self.bots[b].is_done:
                                done = False
                                self.switch_bot(BotName=b, Restart=True)
                                break
                    if done and self.need_something_else:
                        self.active_bot.output(Message='How can I help you?')
                    elif done and not self.is_all_done:
                        self.send_response('I may need something else',
                                           TextMode=True)
                    else:
                        self.active_bot.output(Message="OK, goodbye.")
