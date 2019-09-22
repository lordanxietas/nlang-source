import traceback
import os
import sys
import json
import time
import urllib
import subprocess
import requests

from nobject import *
pymods = ["traceback", "os", "sys", "json", "time", "urllib", "subprocess", "threading", "requests"]

mods = []

from modules import *


def modules(vm):
    for mod in pymods:
        exec(f"vm['{mod}'] = NObject(__import__('{mod}'))")
    for mod in mods:
        vm = eval(mod)(vm)
    return vm