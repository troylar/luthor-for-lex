class WithMessage:
    def __init__(self, **kwargs):
        self.group_number = kwargs.get('GroupNumber')
        self.max_attempts = kwargs.get('MaxAttempts')
        self.response_card = kwargs.get('ResponseCard')
        self.messages = kwargs.get('Messages', [])

    def _to_message(self, content_type, content, group_number):
        message_j = {'contentType': content_type,
                     'content': content}
        if group_number:
            message_j['groupNumber'] = group_number
        return message_j

    def to_dict(self):
        data = {}
        data['messages'] = self.messages
        if self.max_attempts:
            data['maxAttempts'] = self.max_attempts
        if self.response_card:
            data['responseCard'] = self.response_card
        return data

    def with_max_attempts(self, max_attempts):
        self.max_attempts = max_attempts
        return self

    def with_response_card(self, response_card):
        self.response_card = response_card
        return self

    def with_message(self, content_type, content, group_number=None):
        self.messages.append(self._to_message(content_type, content, group_number))
        return self

    @staticmethod
    def from_json(message_j):
        w = WithMessage()
        if 'maxAttempts' in message_j.keys():
            w.with_max_attempts(message_j['maxAttempts'])
        if 'responseCard' in message_j.keys():
            w.with_response_card(message_j['responseCard'])
        if 'messages' in message_j.keys():
            for msg in message_j['messages']:
                w.with_message(msg['contentType'], msg['content'], msg['groupNumber'])
        return w
