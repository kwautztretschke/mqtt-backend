# python 3.6

from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883


class actor:
	name = "undefined_actor"
	def __init__(self):
		# self.name = "undefined_actor" # maybe do something like assert(name)
		self.type = self.__class__.__name__
		self.topic = "actor/" + self.type + "/" + self.name

		self.client = mqtt_client.Client(self.type + "_" + self.name)
		self.client.on_message = self.on_message
		try:
			self.client.connect(broker, port)
			self.client.subscribe(self.topic + "/#")
			self.subscribe_states()
			print(f"Actor {self.name}({self.type}) connected successfully")
			self.client.loop_start()
		except:
			print("Connection error!")

	def on_message(self, client, userdata, msg):
		# print(f"actor `{self.name}` ({self.type}) received `{msg.payload.decode()}` from `{msg.topic}` topic")

		# command to be executed
		if msg.topic.startswith("actor/"):
			self.invoke_action(msg.topic,  msg.payload)

		# state to be updated
		if msg.topic.startswith("state/"):
			self.update_states(msg.topic, msg.payload)

	def publish(self, topic, payload):
		self.client.publish(topic, payload, qos=1, retain=True)

	def invoke_action(self, topic, payload):
		commandstring = topic.replace(self.topic + "/", '', 1)
		self.actions.get(commandstring, lambda: 'invalid')(self, payload)
		
	states_internal = {
		"state/test": 0,
		"state/test2": 0
	}

	def test(self, payload):
		print("test: " + payload)

	actions = {
		"test": test
	}

	def subscribe_states(self):
		for key in self.states_internal.keys():
			print("actor " + self.name + " subscribing to " + key)
			self.client.subscribe(key)

	def update_states(self, topic, payload):
		self.states_internal[topic] = payload.decode()
		print(self.states_internal)

	def publish_states(self, dict):
		for key in dict.keys():
			self.publish(key, dict[key])

##################################################

class lightswitch(actor):
	def turn_on(self, payload):
		pass

	def turn_off(self, payload):
		pass

	def toggle(self, payload):
		pass


class lightswitch_zimmer(lightswitch):
	name = "zimmer"

	states_internal = {
		"state/time/hour": 0,
		"state/bernie/light/mode": 0
	}
	states_on_day = {
		"state/bernie/light/mode": 1,
		"state/bernie/ceiling_light/power": 1,
		"state/bernie/floor_light/power": 0,
		"state/bernie/starprojector/power": 0
	}
	states_on_evening = {
		"state/bernie/light/mode": 2, 
		"state/bernie/ceiling_light/power": 0,
		"state/bernie/floor_light/power": 1,
		"state/bernie/starprojector/power": 1
	}
	states_off = {
		"state/bernie/light/mode": 0,
		"state/bernie/ceiling_light/power": 0,
		"state/bernie/floor_light/power": 0,
		"state/bernie/starprojector/power": 0
	}

	def turn_on(self, payload):
		if int(self.states_internal["state/time/hour"]) < 20:
			self.publish_states(self.states_on_day)
		else:
			self.publish_states(self.states_on_evening)

	def turn_off(self, payload):
		self.publish_states(self.states_off)

	def toggle(self, payload):
		if self.states_internal["state/bernie/light/mode"]:
			self.turn_off('')
		else:
			self.turn_on('')

	actions = {
		"turn_on": turn_on,
		"turn_off": turn_off
	}


instance_lightswitch_zimmer = lightswitch_zimmer()