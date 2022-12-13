from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883


class mqtt_actor:
	# variables to be redefined by derived classes
	location = "nowhere"
	type = "nothing"
	name = "nobody"
	topic = "actor/undefined"
	# execute actions by sending a mqtt message to the topic
 	# "actor/location/type/name/command"

	def __init__(self):
		# self.topic = "actor/" + self.location + "/" + self.type + "/" + self.name
		self.client = mqtt_client.Client(self.type + "_" + self.name)
		self.client.on_message = self.on_message
		try:
			self.client.connect(broker, port)
			self.client.subscribe(self.topic + "/#")
			self.subscribe_states()
			print(f"Actor {self.name} ({self.topic}) connected successfully")
			self.client.loop_start()
		except:
			print("Connection error!")

	# callback to be executed by mqtt client on message received
	def on_message(self, client, userdata, msg):
		# command to be executed
		if msg.topic.startswith("actor/"):
			self.invoke_action(msg.topic, msg.payload.decode())

		# state to be updated
		if msg.topic.startswith("state/"):
			self.update_states(msg.topic, msg.payload.decode())

	# publish a state as a retained message
	def publish_state(self, topic, payload):
		self.client.publish(topic, payload, qos=1, retain=True)

	# publish a mqtt message to another actor
	def publish_command(self, topic, payload):
		self.client.publish(topic, payload)

	# run a command which is requested via mqtt
	invoke_action_verbose = True
	def invoke_action(self, topic, payload):
		commandstring = topic.replace(self.topic + "/", '', 1)
		try:
			self.actions[commandstring](self, payload)
			if self.invoke_action_verbose:
				print(f"Actor {self.name} ({self.topic}) invoked action \"{commandstring}\"")
		except:
			print("invalid command '" + commandstring + "' for actor '" + self.name + "'")
			
	# subscribe the mqtt client to all topics in the states_internal dict
	def subscribe_states(self):
		for key in self.states_internal.keys():
			self.client.subscribe(key)

	# update the internal variable (dict entry) if a state changes
	def update_states(self, topic, payload):
		self.states_internal[topic] = payload

	# update multiple states at once, given a dict where the keys are topics
	def publish_multiple_states(self, dict):
		for key in dict.keys():
			self.publish_state(key, dict[key])
		
	# a dict containing states' values, to be used in logic, which gets updated
	states_internal = {
		"state/test": 0,
		"state/test2": 0
	}

	def test(self, payload):
		print("test: " + payload)

	# a dict containing pairs of command names and the functions to be executed
	actions = {
		"test": test
	}