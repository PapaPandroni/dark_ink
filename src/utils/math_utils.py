"""
Math utility functions
"""
import pygame
import math


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp value between min and max"""
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation"""
    return start + (end - start) * t


def distance(pos1: pygame.Vector2, pos2: pygame.Vector2) -> float:
    """Calculate distance between two points"""
    return (pos2 - pos1).length()


def angle_between(vec1: pygame.Vector2, vec2: pygame.Vector2) -> float:
    """Calculate angle between two vectors in radians"""
    return math.atan2(vec2.y - vec1.y, vec2.x - vec1.x)


def normalize_angle(angle: float) -> float:
    """Normalize angle to -π to π range"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle