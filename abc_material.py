from abc import ABC, abstractmethod

from ray import Ray
from world import World
from hit import Hit

import numpy as np

class Material(ABC):
    @abstractmethod
    def eval(self, world:World, hit:Hit, ray:Ray):
        pass