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
game = hlt.Game("Mining")
# Then we print our start message to the logs
logging.info("Starting my Planet bot!")
turn_count = 0
allCapturedFlag = False

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()
    logging.info("updated gaming map")
    me = game_map.get_me()
    logging.info(me)
    if turn_count == 0:
        players = game_map.all_players()
        logging.info(players)
        twoPlayers = len(players) < 3

    turn_count += 1

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # if ship.docking_status == ship.DockingStatus.DOCKED:
            #     # if the planet is fully mined / full undock the ship
            #     logging.info("Found a docked ship")
            continue

        if not allCapturedFlag:

            nearestPlanet = hlt.Gen.nearest_free_planet_to_ship(ship, game_map)
            # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
            if nearestPlanet != None and ship.can_dock(nearestPlanet) and not nearestPlanet.is_full():
                logging.info("About to attempt a docking move")
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(nearestPlanet))

            elif nearestPlanet == None:
                #after all the planets are taken ships need to make thrustmoves to attack
                #lets try attacking docked enemy ships
                allCapturedFlag = True
                navigate_command = ship.thrust(0, 0)
                if navigate_command:
                    command_queue.append(navigate_command)


            else:
                # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                # We run this navigate command each turn until we arrive to get the latest move.
                # Here we move at half our maximum speed to better control the ships
                # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                # This will mean that you have a higher probability of crashing into ships, but it also means you will
                # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                # wish to turn that option off.
                navigate_command = ship.navigate(ship.closest_point_to(nearestPlanet), game_map, speed=hlt.constants.MAX_SPEED, ignore_ships=False)
                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
                if navigate_command:
                    command_queue.append(navigate_command)
                if turn_count < 5:
                    break            

        # else:
        #     for planet in game_map.get_me().all_planets():  
        #         if planet.get_owner_id(planet) != me.get_id():
        #             continue

        #         #get all the ships assigned to that planet
        #         group = planet.all_docked_ships()

        #         #place them in a fleet
        #         for ship in group:
        #             logging.info(ship.get_fleet())


        else:
            my_nearest_planet = hlt.Gen.mining_helper(ship, game_map, me)

            if my_nearest_planet is None or my_nearest_planet.is_full():
                logging.info("defense")

            elif ship.can_dock(my_nearest_planet):
                logging.info("About to attempt a docking move")
                # We add the command by appending it to the command_queue
                command_queue.append(ship.dock(my_nearest_planet))



            else:
                # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                # We run this navigate command each turn until we arrive to get the latest move.
                # Here we move at half our maximum speed to better control the ships
                # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                # This will mean that you have a higher probability of crashing into ships, but it also means you will
                # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                # wish to turn that option off.
                logging.info("just moving")
                navigate_command = ship.navigate(ship.closest_point_to(my_nearest_planet), game_map, speed=hlt.constants.MAX_SPEED, ignore_ships=False)
                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
                if navigate_command:
                    command_queue.append(navigate_command)  

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
