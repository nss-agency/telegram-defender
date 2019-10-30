import json


class Groups:
    # Default settings for new chats
    default_mode = 0
    default_mute = 0
    default_bias = 0
    dictionary = {}

    def __init__(self, file_name):
        self.file_name = file_name
        self.dictionary = json.load(open(self.file_name, 'r', errors='ignore'))

    def __update_file__(self):
        # Private function for JSON update
        open(self.file_name, 'w').write(json.dumps(self.dictionary, indent=4))

    def new_chat(self, chat_id, **kwargs):
        # Function for creating new chat
        self.dictionary[str(chat_id)] = {'mode': kwargs.get('mode', self.default_mode),
                                         'mute': kwargs.get('mute', self.default_mute),
                                         'bias': kwargs.get('bias', self.default_bias)}
        self.__update_file__()

    def update_chat(self, chat_id, **kwargs):
        # Function for updating chat
        self.dictionary[str(chat_id)] = {'mode': kwargs.get('mode', self.get_chat_mode(chat_id)),
                                         'mute': kwargs.get('mute', self.get_chat_mute(chat_id)),
                                         'bias': kwargs.get('bias', self.get_chat_bias(chat_id))}
        self.__update_file__()

    # Getter\Setter function for chats and their settings
    def get_chat_by_id(self, chat_id):
        return self.dictionary.get(str(chat_id), None)

    def get_chat_mode(self, chat_id):
        return self.get_chat_by_id(chat_id)['mode']

    def get_chat_mute(self, chat_id):
        return self.dictionary[str(chat_id)]['mute']

    def get_chat_bias(self, chat_id):
        return self.dictionary[str(chat_id)]['bias']

    def get_chat_setting_by_name(self, chat_id, setting):
        if setting == 'short':
            setting = 'mode'
        return self.get_chat_by_id(chat_id)[setting]

    def set_chat_setting_by_name(self, chat_id, setting, new_value):
        if setting == 'short':
            setting = 'mode'
        self.get_chat_by_id(chat_id)[setting] = new_value
        self.__update_file__()

    def set_chat_mode(self, chat_id, mode):
        self.update_chat(chat_id, mode=mode)
        self.__update_file__()

    def set_chat_mute(self, chat_id, mute):
        self.update_chat(chat_id, mute=mute)
        self.__update_file__()

    def set_chat_bias(self, chat_id, bias):
        self.update_chat(chat_id, bias=bias)
        self.__update_file__()

    # To string function
    def __str__(self):
        return f'GroupsObject for "{self.file_name}"'