class Conversation(object):
    def __init__(self):
        self.logs = []

    def log(self, actor, context):
        self.logs.append('%s: %s' % (actor.name, context))

class Alpha(object):
    def __init__(self, conversation, accompany):
        self.conversation = conversation
        self.accompany    = accompany
        self.name         = self.__class__.__name__

    def order(self):
        self.conversation.log(self, 'orders "egg"')

        return 'egg'

    def say_thank(self, server_name = None):
        self.conversation.log(self, 'says "Thank you" to {}'.format(server_name))

class Beta(object):
    def __init__(self, conversation):
        self.conversation = conversation
        self.name         = self.__class__.__name__

    def acknowledge(self, receipt):
        self.conversation.log(self, 'acknowledge "{}"'.format(receipt))

    def say_thank(self, server_name = None):
        self.conversation.log(self, 'says "Merci" to {}'.format(server_name))

class Charlie(object):
    def __init__(self, conversation):
        self.conversation = conversation
        self.name         = self.__class__.__name__

    def cook(self):
        self.conversation.log(self, 'cook')

    def serve(self):
        self.conversation.log(self, 'serve')

        return self.name
