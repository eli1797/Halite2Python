from .game_map import *
from .entity import Entity, Planet, Position, Ship
import logging

class Gen:
    """
        Class for general functions:
            -Returning the nearest planet to a ship
    """
    @staticmethod
    def nearest_planet_to_ship(entity, game_map):
        logging.info("nearest_planet_to_ship called")
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        nearest_planet = None
        if isinstance(entity, Ship):
            logging.info("entity is a ship")
            ship = entity
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            for distance in sorted(entities_by_distance):
                logging.info("inside for loop")
                temp = next((nearest_entity for nearest_entity in entities_by_distance[distance]), None)
                if isinstance(temp, Ship):
                    #we want planets not ships so skip this entity
                    continue
                if temp.is_owned():
                    # Skip this planet
                    continue
                nearest_planet = temp
                if nearest_planet != None:
                    break
        return nearest_planet

    @staticmethod
    def nearest_enemy_planet(entity, game_map, me):
        logging.info("nearest_enemy_planet method started")
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        nearest_planet = None
        if isinstance(entity, Ship):
            ship = entity
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            for distance in sorted(entities_by_distance):
                temp = next((nearest_entity for nearest_entity in entities_by_distance[distance]), None)
                if isinstance(temp, Ship):
                    #we want planets not ships so skip this entity
                    continue
                if temp.get_owner_id() == me.get_id():
                    # Skip this planet
                    continue
                nearest_planet = temp
                if nearest_planet != None:
                    break
        return nearest_planet
