from .key import *
from .mouse import *
from ..utils.general import iterable_to_array
from typing import Iterable

class KeyCombination:
    def __init__(self, *args):
        self.keys = args
    
    def __eq__(self, other: 'KeyCombination'):
        for key in self.keys:
            if not key in other.keys:
                return False
        return True
    
    def __ne__(self, other: 'KeyCombination'):
        return not self.__eq__(other)

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
    
    def events(event):
        Key.events(event)
        Mouse.events(event)

    @staticmethod
    def action_pressed(action):
        if action in Input.actions.keys():
            for k in Input.actions[action]:
                if isinstance(k, KeyCombination):
                    if all([Key.pressed[m_key] for m_key in k.keys]):
                        return True
                elif Key.pressed[k]:
                    return True
            return False
        raise ValueError('Action "' + action + '" does not exist')
        
    @staticmethod
    def action_just_pressed(action):
        if action in Input.actions.keys():
            for k in Input.actions[action]:
                if isinstance(k, KeyCombination):
                    if all([Key.pressed[m_key] for m_key in k.keys]) and any([not Key._pressed_last_tick[m_key] for m_key in k.keys]):
                        return True
                elif Key.just_pressed[k]:
                    return True
            return False
        raise ValueError('Action "' + action + '" does not exist')
        
    @staticmethod
    def action_just_released(action):
        if action in Input.actions.keys():
            for k in Input.actions[action]:
                if isinstance(k, KeyCombination):
                    if all([Key._pressed_last_tick[m_key] for m_key in k.keys]) and any([not Key.pressed[m_key] for m_key in k.keys]):
                        return True
                elif Key.just_released[k]:
                    return True
            return False
        raise ValueError('Action "' + action + '" does not exist')

    @staticmethod
    def add_action(action_name, *args):
        Input.actions[action_name] = []
        if args is not None:
            Input.add_key_to(action_name, *args)

    @staticmethod
    def remove_action(action_name):
        try:
            Input.actions.pop(action_name)
        except KeyError:
            raise ValueError('Action "' + action_name + '" does not exist')

    @staticmethod
    def add_key_to(action_name, *args):
        try:
            for k in args:
                Input.actions[action_name].append(k)
        except KeyError:
            raise ValueError('Action "' + action_name + '" does not exist')

    @staticmethod
    def remove_key_from(action_name, key):
        try:
            Input.actions[action_name].remove(key)
        except KeyError:
            raise ValueError('Action "' + action_name + '" does not exist')
