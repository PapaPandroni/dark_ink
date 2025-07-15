"""
Base entity class for the ECS system
"""
import pygame
from typing import Dict, Any, Type
from src.components.component import Component


class Entity:
    """Base entity class for ECS architecture"""
    
    def __init__(self, entity_id: int):
        self.id = entity_id
        self.components: Dict[Type[Component], Component] = {}
        self.active = True
    
    def add_component(self, component: Component):
        """Add a component to this entity"""
        self.components[type(component)] = component
        component.entity = self
    
    def remove_component(self, component_type: Type[Component]):
        """Remove a component from this entity"""
        if component_type in self.components:
            del self.components[component_type]
    
    def get_component(self, component_type: Type[Component]) -> Component:
        """Get a component from this entity"""
        return self.components.get(component_type)
    
    def has_component(self, component_type: Type[Component]) -> bool:
        """Check if entity has a component"""
        return component_type in self.components
    
    def destroy(self):
        """Mark entity for destruction"""
        self.active = False