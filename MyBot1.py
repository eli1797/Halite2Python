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
game = hlt.Game("Settler")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")
counter = 0

while True:
    counter += 1
    # myTurnsCount = myTurnsCount + 1
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()
    logging.info("updated gaming map " + str(counter))
    me = game_map.get_me()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        nearestPlanet = None
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        logging.info("about to nearest")
        nearestPlanet = hlt.Gen.nearest_free_planet_to_ship(ship, game_map)
        # nearestFriendlyPlanet = hlt.Gen.nearest_friendly_planet(ship, game_map)
        logging.info("nearestPlanet instantiated")

        #what is all planets are owned
        # if (nearestPlanet == None):
        #     nearestPlanet = hlt.Gen.nearest_enemy_planet(ship, game_map, me)

        # # For each planet in the game (only non-destroyed planets are included)
        # for planet in game_map.all_planets():
        #     # If the planet is owned
        #     if planet.is_owned():
        #         # Skip this planet
        #         continue
        logging.info("Check ship actions")
        # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
        if nearestPlanet != None and ship.can_dock(nearestPlanet):
            logging.info("About to attempt a docking move")
            # We add the command by appending it to the command_queue
            command_queue.append(ship.dock(nearestPlanet))

        elif nearestPlanet == None:
            #after all the planets are taken ships need to make thrustmoves to attack
            #lets try attacking docked enemy ships
            enemyShip = hlt.Gen.nearest_docked_enemy(ship, game_map, me)
            logging.info(enemyShip)
            if enemyShip != None:
                logging.info("found an enemy ship!")
                # logging.info("num obstacles between" + game_map.obstacles_between(game_map, ship, enemyShip, entity.Ship))
                # if len(game_map.obstacles_between(game_map, ship, enemyShip, entity.Ship)) == 0:
                #     logging.info("no obstacles between me and enemy")
                #     myThrustAngle = ship.calculate_angle_between(enemyShip)
                #     navigate_command = ship.thrust(hlt.constants.MAX_SPEED, myThrustAngle)

                # else:
                # logging.info("There were obstacles between me and enemy")
                navigate_command = ship.navigate(enemyShip, game_map, speed=hlt.constants.MAX_SPEED, ignore_ships=True)

            if navigate_command:
                logging.info("I am now trying to blow up enemy")
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
            logging.info(nearestPlanet)
            navigate_command = ship.navigate(ship.closest_point_to(nearestPlanet), game_map, speed=hlt.constants.MAX_SPEED, ignore_ships=False)
            # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
            # or we are trapped (or we reached our destination!), navigate_command will return null;
            # don't fret though, we can run the command again the next turn)
            if navigate_command:
                logging.info("I am now trying to get near a planet")
                command_queue.append(navigate_command)
        break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    logging.info("sent command_queue")
    # TURN END
# GAME END
