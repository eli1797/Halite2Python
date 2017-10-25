from . import game_map
from .entity import Entity

class Gen:
    """
        Class for general functions:
            -Returning the nearest planet to a ship
    """
    @staticmethod
    def nearest_planet_to_ship(entity, game_map):
        """
        :param ent: The source entity (hopefully a ship)
        :return: Entity of type planet that is closest to the ship
        :rtype: entity
        """
        nearest_planet = None
        if isinstance(entity, hlt.entity.Ship):
            ship = entity
            entities_by_distance = game_map.nearby_entities_by_distance(ship)
            for distance in sorted(entities_by_distance):
                temp = next((nearest_entity for nearest_entity in entities_by_distance[distance] if isinstance(nearest_entity, hlt.entity.Planet)), None)
                if temp.is_owned():
                    # Skip this planet
                    continue
                nearest_planet = temp
                if nearest_planet != None:
                    break
        return nearest_planet


