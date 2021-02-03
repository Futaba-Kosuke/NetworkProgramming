from dataclasses import dataclass, InitVar, field
import json

@dataclass
class Message:
    message_json: InitVar[str]

    unique_id: str = field(default='')
    user_name: str = field(default='')
    date: str = field(default='')
    title: str = field(default='')
    letter: str = field(default='')
    # secret data
    user_ip: str = field(default='')
    password: str = field(default='')

    def __post_init__ (self, message):
        if type(message) == str:
            message_dict = json.loads(message)
        else:
            message_dict = message

        self.unique_id = message_dict['unique_id']
        self.user_name = message_dict['user_name']
        self.date = message_dict['date']
        self.title = message_dict['title']
        self.letter = message_dict['letter']
        # secret data
        self.user_ip = message_dict['user_ip']
        self.password = message_dict['password']
        
    def to_dict (self, is_have_secret=False):
        if is_have_secret:
            return vars(self)
        else:
            result = vars(self)
            result['password'] = ''
            result['user_ip'] = ''
            return result

    def to_json (self, is_have_secret=False):
        return json.dumps(self.to_dict(is_have_secret=is_have_secret))
