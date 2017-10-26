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
            ship = entity
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            for distance in sorted(entities_by_distance):
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
                logging
                if temp.get_owner_id() == me.get_id():
                    logging.info("I don't own")
                    nearest_planet = temp
                    if nearest_planet != None:
                        break
        logging.info(nearest_planet)
        return nearest_planet

    @staticmethod
    def nearest_docked_enemy(entity, game_map, me):
        logging.info("nearest_docked_enemy method started")
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        toReturn = None
        if isinstance(entity, Ship):
            ship = entity
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            if entities_by_distance == None:
                return None
            for distance in sorted(entities_by_distance):
                temp = next((nearest_entity for nearest_entity in entities_by_distance[distance]), None)
                if temp == None:
                    continue
                if isinstance(temp, Planet):
                    #we want planets not ships so skip this entity
                    continue
                if temp.docking_status == ship.DockingStatus.UNDOCKED:
                    continue
                if temp.get_owner_id() == me.get_id():
                    # Don't want to attack myself
                    logging.info("inside owner check")
                    continue
                logging.info(me)
                logging.info(temp)
                toReturn = temp
                if toReturn != None:
                    break
        return toReturn