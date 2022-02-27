from .key import *
from .mouse import *


class Input:
    actions = {}

    @staticmethod
    def init():
        Key.init()
        Mouse.init()

    @staticmethod
    def tick():
        Key.tick()
        Mouse.tick()

    @staticmethod
    def action_pressed(action):
        if action in Input.actions.keys():
            for k in Input.actions[action]:
                if Key.pressed[k]:
                    return True
            return False
        raise ValueError('Action "' + action + '" does not exist')

    @staticmethod
    def add_action(action_name):
        Input.actions[action_name] = []

    @staticmethod
    def remove_action(action_name):
        try:
            Input.actions.pop(action_name)
        except KeyError:
            raise ValueError('Action "' + action_name + '" does not exist')

    @staticmethod
    def add_key_to(action_name, key):
        try:
            Input.actions[action_name].append(key)
        except KeyError:
            raise ValueError('Action "' + action_name + '" does not exist')

    @staticmethod
    def remove_key_from(action_name, key):
        try:
            Input.actions[action_name].remove(key)
        except KeyError:
            raise ValueError('Action "' + action_name + '" does not exist')
