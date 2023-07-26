# python3.6

import mqtt_actors as actors
import mqtt_reactors as reactors
broker = 'localhost'
port = 1883


def run():
	cronjob = actors.cronjob()
	lightswitch_bedroom = actors.lightswitch_bedroom()
	while (1):
		pass


if __name__ == '__main__':
	run()
