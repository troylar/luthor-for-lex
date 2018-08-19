from lex.bots import BaseBot
import time


class PollexyHygieneBot(BaseBot):
    def __init__(self, lexbot):
        self.bot_name = 'PollexyHygieneBot'
        self.lexbot = lexbot
        super(PollexyHygieneBot, self).__init__()

    def on_fulfilled(self):
        print(self.lexbot.last_intent)
        if self.lexbot.last_intent == 'PollexyBrushTeethIntent':
            self.lexbot.output(
                Message="Great! Let's go! Pick up your toothbrush." +
                        "Put some toothpaste on the toothbrush.")
            self.lexbot.next_intent = \
                'I want to put toothbrush on my toothpaste'

        if self.lexbot.last_intent == 'PollexyPutToothpasteIntent':
            self.lexbot.output(
                Message="Great! Let's go! Pick up your toothbrush.")
            self.lexbot.next_intent = \
                'brush my top teeth'

        if self.lexbot.last_intent == 'PollexyBrushTopTeethIntent':
            self.lexbot.output(
                Message="Awesome. Start brushing your top teeth. I'll " +
                        "tell you when to switch. Start brushing your top " +
                        "teeth now.")
            time.sleep(10)
            self.lexbot.output(
                Message="OK, let's switch to your bottom teeth. Start " +
                        "brushing your bottom teeth now.")
            time.sleep(10)
            self.lexbot.output(
                Message="Great, you're all done brushing your teeth!")
            self.lexbot.next_intent = ""

        super(PollexyHygieneBot, self).on_fulfilled()

    def on_failed(self):
        intent = self.lexbot.last_response['intentName']
        if intent == 'PollexyBrushTeethIntent':
            self.lexbot.next_intent = 'I want to brush my teeth'
            self.lexbot.output(Message="OK, I'll wait a moment for you.")
            time.sleep(5)
        super(PollexyHygieneBot, self).on_failed()

    def on_transition_in(self):
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
        super(PollexyHygieneBot, self).register()
