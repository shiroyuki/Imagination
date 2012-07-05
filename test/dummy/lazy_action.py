class Conversation(object):
    logs = []

    @staticmethod
    def log(actor, context):
        Conversation.logs.append('%s: %s' % (actor.__class__.__name__, context))

class Alpha(object):
    def __init__(self, accompany):
        self.accompany = accompany

    def call_accompany(self):
        self.accompany.acknowledge()

        return self.accompany

    def order(self, item):
        Conversation.log(self, 'order "%s"' % item)
        return item

    def speak_to_accompany(self, context):
        Conversation.log(self, 'speak to %s, "%s"' % (self.accompany.__class__.__name__, context))

    def wash_hands(self):
        Conversation.log(self, 'wash hands')

    def speak(self, context):
        Conversation.log(self, 'say, %s' % context)

class Beta(object):
    def acknowledge(self):
        Conversation.log(self, 'acknowledge')

class Charlie(object):
    def cook(self):
        Conversation.log(self, 'cook')

    def serve(self):
        Conversation.log(self, 'serve')

    def respond(self, response):
        Conversation.log(self, 'repeat "%s" then "%s"' % (context, response))

    def repeat(self, feedback):
        Conversation.log(self, 'repeat "%s" then "%s"' % (context, response))