class WithMessage:
    def __init__(self, **kwargs):
        self.group_number = kwargs.get('GroupNumber')
        self.max_attempts = kwargs.get('MaxAttempts')
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



