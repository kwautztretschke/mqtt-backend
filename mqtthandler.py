# python3.6

import mqtt_actors as actors
import mqtt_reactors as reactors
broker = 'localhost'
port = 1883


def run():
	# actors
	cronjob = actors.cronjob()
	bedroom_lightswitch = actors.lightswitch_bedroom()

	# reactors
	bedroom_whiteboard = reactors.bedroom_whiteboard()
	bedroom_floorlamp = reactors.bedroom_floorlamp()
	while (1):
		pass


if __name__ == '__main__':
	run()
