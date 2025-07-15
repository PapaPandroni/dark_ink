"""
Base component class for ECS system
"""
from abc import ABC


class Component(ABC):
    """Base component class"""
    
    def __init__(self):
        self.entity = None