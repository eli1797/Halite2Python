"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Planet Bot")
# Then we print our start message to the logs
logging.info("Starting my Planet bot!")
turn_count = 0
planetMode = False
dock_count = 0

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()
    logging.info("updated gaming map")
    me = game_map.get_me()
    # logging.info(me)

    turn_count += 1

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []

    if not planetMode:
        # For every ship that I control
        for ship in game_map.get_me().all_ships():
            nearestPlanet = None
            # If the ship is docked
            if ship.docking_status == ship.DockingStatus.UNDOCKED:
                # if ship.docking_status == ship.DockingStatus.DOCKED:
                #     # if the planet is fully mined / full undock the ship
                #     logging.info("Found a docked ship")

                
                nearestPlanet = hlt.Gen.nearest_free_planet_to_ship(ship, game_map, ignore_ownership = True)
                if nearestPlanet == None:
                    navigate_command = ship.thrust(0,0)
                    if navigate_command:
                        command_queue.append(navigate_command)
                    continue
                elif nearestPlanet.is_full():
                     nearestPlanet = hlt.Gen.nearest_free_planet_to_ship(ship, game_map)

                # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
                if nearestPlanet != None and ship.can_dock(nearestPlanet) and not nearestPlanet.is_full():
                    logging.info("About to attempt a docking move")
                    # We add the command by appending it to the command_queue
                    dock_count += 1
                    command_queue.append(ship.dock(nearestPlanet))

                elif nearestPlanet == None:

                    #after all the planets are taken ships need to make thrustmoves to attack
                    #lets try attacking docked enemy ships
                    planetMode = True

                # elif nearestPlanet.is_full():
                #     nearestPlanet = nearest_friendly_planet_to_ship
                else:
                    logging.info("just moving")
                    navigate_command = ship.navigate(ship.closest_point_to(nearestPlanet), game_map, speed=hlt.constants.MAX_SPEED, ignore_ships=False)
                    if navigate_command:
                        command_queue.append(navigate_command)
                    if turn_count < 4:
                        break            
            if ship.docking_status != ship.DockingStatus.UNDOCKED:
                logging.info(ship.docking_status)
    else:
        logging.info("entered planet mode")
# Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
