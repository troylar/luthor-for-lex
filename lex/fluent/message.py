class WithMessage:
    def __init__(self, **kwargs):
        self.key = 'N/A'
        self.group_number = kwargs.get('GroupNumber')
        self.max_attempts = kwargs.get('MaxAttempts')
        self.messages = []

    def _to_message(self, content_type, content, group_number):
        message_j = {'contentType': content_type,
                     'content': content}
        if group_number:
            message_j['groupNumber'] = group_number
        return message_j

    def _to_json(self):
        self.data[self.key]['messages'] = self.messages
        if self.max_attempts:
            self.data[self.key]['maxAttempts'] = self.max_attempts
        if self.group_number:
            self.data[self.key]['groupNumber'] = self.group_number
        return

    def with_message(self, content_type, content, group_number):
        self.messages.append(self._to_message(content_type, content, group_number))
        return self



