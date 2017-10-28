from .game_map import *
from .entity import Entity, Planet, Position, Ship
import logging

class Gen:
    """
        Class for general functions:
            -Returning the nearest planet to a ship
    """
    @staticmethod
    def nearest_free_planet_to_ship(entity, game_map):
        logging.info("nearest_free_planet_to_ship called")
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        nearest_planet = None
        if isinstance(entity, Ship):
            ship = entity
            entities_by_distance = game_map.nearby_planets_by_distance(ship)
            for distance in sorted(entities_by_distance):
                temp = next((nearest_entity for nearest_entity in entities_by_distance[distance]), None)
                if temp.is_owned():
                    # Skip this planet
                    continue
                nearest_planet = temp
                if nearest_planet != None:
                    break
        return nearest_planet

    @staticmethod
    def nearest_friendly_planet_to_ship(entity, game_map, me):
        logging.info("nearest_friendly_planet_to_ship called")
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        nearest_planet = None
        if isinstance(entity, Ship):
            ship = entity
            #calling nearby_planets to get a dict of the planets on the game map
            entities_by_distance = game_map.nearby_planets_by_distance(ship)
            for distance in sorted(entities_by_distance):
                temp = next((nearest_entity for nearest_entity in entities_by_distance[distance]), None)
                if temp.get_owner_id(temp) != me.get_id():
                    continue
                nearest_planet = temp
                if nearest_planet != None:
                    break
        return nearest_planet

    @staticmethod
    def mining_helper(entity, game_map, me):
        logging.info("mining_helper called")
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        nearest_planet = None
        if isinstance(entity, Ship):
            ship = entity
            entities_by_distance = game_map.nearby_planets_by_distance(ship)
            for distance in sorted(entities_by_distance):
                temp = next((nearest_entity for nearest_entity in entities_by_distance[distance]), None)
                if not temp.is_owned():
                    continue
                elif temp.get_owner_id(temp) != me.get_id():
                    continue
                if temp.is_full():
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
            planets_by_distance = game_map.nearby_planets_by_distance(ship)
            # post submission if statement
            if planets_by_distance == {}:
                return None
            for distance in sorted(planets_by_distance):
                temp = next((nearest_entity for nearest_entity in planets_by_distance[distance]), None)
                if isinstance(temp, Ship):
                    #we want planets not ships so skip this entity
                    continue
                if temp.get_owner_id(temp) == me.get_id():
                    continue
                nearest_planet = temp
                if nearest_planet != None:
                    break
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
            ships_by_distance = game_map.nearby_ships_by_distance(ship)
            if ships_by_distance == None:
                return None
            for distance in sorted(ships_by_distance):
                temp = next((nearest_entity for nearest_entity in ships_by_distance[distance]), None)
                if temp.docking_status == ship.DockingStatus.UNDOCKED:
                    continue
                if temp.get_owner_id(temp) == me.get_id():
                    # Don't want to attack myself
                    continue
                toReturn = temp
                if toReturn != None:
                    break
        return toReturn

    @staticmethod
    def nearest_enemy_ship(entity, game_map, me):
        logging.info("nearest_enemy_ship method started")
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        toReturn = None
        if isinstance(entity, Ship):
            ship = entity
            ships_by_distance = game_map.nearby_ships_by_distance(ship)
            if ships_by_distance == None:
                return None
            for distance in sorted(ships_by_distance):
                temp = next((nearest_entity for nearest_entity in ships_by_distance[distance]), None)
                if temp.get_owner_id(temp) == me.get_id():
                    # Don't want to attack myself
                    continue
                toReturn = temp
                if toReturn != None:
                    break
        return toReturn