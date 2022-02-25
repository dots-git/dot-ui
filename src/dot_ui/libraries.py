import os

UI_MODULE_PATH = os.path.dirname(__file__)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import numpy as np
from pygame import Vector2, Surface
from math import sqrt, log, exp
import random
import time
from .utils.color import Color
from .utils.animations import *
