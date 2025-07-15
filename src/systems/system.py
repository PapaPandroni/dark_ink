"""
Base system class for ECS architecture
"""
from abc import ABC, abstractmethod
from typing import List
from src.entities.entity import Entity


class System(ABC):
    """Base system class"""
    
    def __init__(self):
        self.entities: List[Entity] = []
    
    @abstractmethod
    def update(self, dt: float):
        """Update system logic"""
        pass
    
    def add_entity(self, entity: Entity):
        """Add entity to system"""
        if entity not in self.entities:
            self.entities.append(entity)
    
    def remove_entity(self, entity: Entity):
        """Remove entity from system"""
        if entity in self.entities:
            self.entities.remove(entity)