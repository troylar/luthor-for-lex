from lex.bots import BaseBot


class SetAlarmBot(BaseBot):
    def __init__(self, lexbot):
        self.bot_name = 'SetAlarmBot'
        self.lexbot = lexbot
        super().__init__()

    def on_fulfilled(self):
        if self.lexbot.last_intent == 'SetAlarmIntent':
            t = self.lexbot.slots['TimeSlot']
            self.lexbot.output(
                Message='Your alarm has been scheduled for {}.'.format(t))
        super().on_fulfilled()

    def on_failed(self):
        super().on_failed()

    def on_transition_in(self):
        self.lexbot.output(Message="OK, back to setting your alarm.")
        pass

    def on_transition_out(self):
        self.lexbot.output(Message="OK, let's hold off on setting your alarm.")
        pass

    def on_cancel(self):
        pass

    def on_needs_intent(self):
        pass

    def on_response(self):
        pass

    def register(self):
        super().register()
