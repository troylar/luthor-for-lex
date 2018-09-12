import click
from lex import LexBotManager, LexIntentManager, LexSlotManager, LexPlayer
from lex.fluent.intent import Intent
from lex.fluent.slot import Slot, EnumerationValue
import os

@click.group()
def cli():
    pass

@cli.group('bot')
def lex_bot():
    pass


@cli.group('intent')
def lex_intent():
    pass


@cli.group('slot')
def lex_slot_type():
    pass


@lex_bot.command('apply')
@click.argument('config_path')
def apply_bots(config_path):
    bm = LexBotManager(ConfigPath=config_path)
    bots = bm.load_bots()
    for k in list(bots.keys()):
        bot = bots[k]
        status, bot = bm.upsert(bot)
        if not status == 'FAILED':
            bot = bm.create_version(bot)
            bot = bm.update_alias(bot, Version='$LATEST')


@lex_intent.command('apply')
@click.argument('config_path')
def apply_intents(config_path):
    im = LexIntentManager(ConfigPath=config_path)
    intents = im.load()
    for i in list(intents.keys()):
        intent = intents[i]
        intent = im.upsert(intent)
        im.create_version(intent)

@lex_intent.command('get')
@click.argument('name')
@click.option('--version', default='$LATEST')
def get_intent(name, version):
    sm = LexIntentManager()
    intent_j = sm.get_intent(Name=name, Version=version)
    intent = Intent.from_json(intent_j)
    print(intent.to_json())


@lex_slot_type.command('apply')
@click.argument('config_path')
def apply_slots(config_path):
    sm = LexSlotManager(ConfigPath=config_path)
    slots = sm.load()
    for i in list(slots.keys()):
        slot = slots[i]
        slot = sm.upsert(slot)
        sm.create_version(slot)

@lex_slot_type.command('get')
@click.argument('name')
@click.option('--version', default='$LATEST')
def get_slot(name, version):
    sm = LexSlotManager()
    slot_type_j = sm.get_slot_type(Name=name, Version=version)
    slot_type = Slot.from_json(slot_type_j)
    print(slot_type)


@cli.command('play')
@click.argument('bot_names')
@click.option('--alias', default='$LATEST')
@click.option('--username', default='PollexyUser')
@click.option('--ice_breaker')
@click.option('--introduction')
@click.option('--voice_id', default='Joanna')
@click.option('--no_audio/--audio', default=False)
@click.option('--required_bots')
@click.option('--verbose/--no-verbose', default=False)
def lex_play(bot_names, alias, username, voice_id, no_audio, ice_breaker,
             verbose, required_bots, introduction):
    if verbose:
        os.environ['LOG_LEVEL'] = 'DEBUG'
    lp = LexPlayer(
        BotNames=bot_names,
        Alias=alias,
        Username=username,
        VoiceId=voice_id,
        IceBreaker=ice_breaker,
        Introduction=introduction,
        NoAudio=no_audio,
        BotsRequired=required_bots)
    while (not lp.is_done):
        lp.get_user_input()

if __name__ == '__main__':
    cli()
