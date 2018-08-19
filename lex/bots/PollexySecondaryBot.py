from lex.bots import BaseBot
import arrow


class PollexySecondaryBot(BaseBot):
    def __init__(self, lexbot):
        self.bot_name = 'PollexySecondaryBot'
        self.lexbot = lexbot
        super(PollexySecondaryBot, self).__init__()

    def on_fulfilled(self):
        if self.lexbot.last_intent == 'PollexyWhatTimeIsItIntent':
            now_local = arrow.utcnow().to('local')
            self.lexbot.output(Message='The time is {}. Today is {}.'
                               .format(now_local.format('hh:mm'),
                                       now_local.format('dddd, MM-DD-YYYY')))

        if self.lexbot.last_intent == 'PollexyEmergencyIntent':
            contact = self.lexbot.slots['PollexyEmergencyContactSlot']
            self.lexbot.output(
                Message="I'm immediately sending a message to {}"
                        .format(contact))
        super(PollexySecondaryBot, self).on_fulfilled()

    def on_failed(self):
        super(PollexySecondaryBot, self).on_failed()

    def on_transition_in(self):
        if self.lexbot.last_intent == 'PollexyEmergencyIntent':
            self.lexbot.output(Message="Let's get you some help")
        pass

    def on_transition_out(self):
        pass

    def on_cancel(self):
        pass

    def on_needs_intent(self):
        pass

    def on_response(self):
        pass

    def register(self):
        super(PollexySecondaryBot, self).register()
