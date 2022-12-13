# python3.6

import mqtt_actors as actors
broker = 'localhost'
port = 1883


def run():
	instance_lightswitch_zimmer = actors.lightswitch_bernie_shelly()
	instance_cronjob = actors.cronjob()
	while (1):
		pass


if __name__ == '__main__':
	run()
