from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883


class mqtt_actor:
    ############################### variables to be redefined by derived classes
	# information about the reactor
	location = "nowhere"
	type = "nothing"
	name = "nobody"
	topic = "actor/undefined"

	# a dict containing states' values, to be used in logic, which gets updated
	states = {
		"foo": 0,
		"bar": 0
	}

	# a dict containing pairs of command names and the functions to be executed
	commands = {
		"test": helloworld
	}

	################################ general mqtt related utilities
	# constructor, initializes the mqtt client
	def __init__(self):
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
			self.invoke_command(msg.topic, msg.payload.decode())

		# state to be updated
		if msg.topic.startswith("state/"):
			self.update_state(msg.topic, msg.payload.decode())

	# subscribe the mqtt client to all topics in the states dict
	def subscribe_states(self):
		for key in self.states.keys():
			self.client.subscribe("state/" + key)

	# update the internal variable (dict entry) if a state changes
	def update_state(self, topic, payload):
		state = topic.replace("state/", '', 1)
		self.states[state] = payload

	# publish a mqtt message to another actor
	def publish_command(self, topic, payload):
		self.client.publish(topic, payload)

	# publish a state as a retained message
	def publish_state(self, state, payload):
		self.client.publish("state/" + state, payload, qos=1, retain=True)

	# update multiple states at once, given a dict where the keys are topics
	def publish_multiple_states(self, dict):
		for key in dict.keys():
			self.publish_state(key, dict[key])
		
	########################################## actor funtionality specific functions
	# run a command which is requested via mqtt
	# possible commands are defined in the commands dict with their respective methods
	invoke_command_verbose = True
	def invoke_command(self, topic, payload):
		commandstring = topic.replace(self.topic + "/", '', 1)
		try:
			self.commands[commandstring](self, payload)
			if self.invoke_command_verbose:
				print(f"Actor {self.name} ({self.topic}) invoked command \"{commandstring}\"")
		except:
			print("invalid command '" + commandstring + "' for actor '" + self.name + "'")

	# a demo command that will be executed when "actor/undefined/test" is received
	def helloworld(self, payload):
		print("Hello World, payload: " + payload)


 
 class mqtt_reactor:
    ############################### variables to be redefined by derived classes
	# information about the reactor
    location = "nowhere"
    type = "nothing"
    name = "nobody"
	topic = "reactor/undefined"

    # a dict containing states' values, to be used in logic, which gets updated
    states = {
        "foo": 0,
        "bar": 0
    }
	
	# a dict containing the states that should just be passed through to the reactor
	passthrough_states = {
        # the payload for state/foo will be sent to reactor/undefined/wallah
        "foo": "wallah",
    }
 
	# a dict containing presets and the respective set of commands
	presets = {
        "A": [("wallah", "42")],
        "B": [
            ("wallah", "187"),
            ("billah", "207")
        ],
    }

	################################ general mqtt related utilities
	# constructor, initializes the mqtt client
    def __init__(self):
        self.client = mqtt_client.Client(self.type + "_" + self.name)
        self.client.on_message = self.on_message
        try:
            self.client.connect(broker, port)
            self.subscribe_states()
            print(f"Reactor {self.name} connected successfully")
            self.client.loop_start()
        except:
            print("Connection error!")

    # callback to be executed by mqtt client on message received
	def on_message(self, client, userdata, msg):
		self.update_states(msg.topic, msg.payload.decode())

		if not self.passthrough_state(msg.topic, msg.payload.decode()):
			self.determine_preset()  # Call the derived class's determine_preset function

    # subscribe the mqtt client to all topics in the states dict
    def subscribe_states(self):
        for key in self.states.keys():
            self.client.subscribe("state/" + key)

    # update the internal variable (dict entry) if a state changes
    def update_state(self, topic, payload):
		state = topic.replace("state/", '', 1)
		self.states[state] = payload

	# publish a mqtt message to the hardware equivalent of the reactor
	def publish_to_reactor(self, command, payload, retain=False):
		self.client.publish(topic + "/" + command, payload, qos=1, retain)

	################################# reactor functionality specific functions
	# Check if the received message matches any of the passthrough topics
	def passthrough_state(self, topic, payload):
		state = topic.replace("state/", '', 1)
        passthrough = self.passthrough_states.get(state)
        if passthrough:
            self.publish_to_reactor(passthrough, payload, True)
            return True  # Return True if the state was found in the passthrough dict
        return False  # Return False if not

	# depending on the states, apply a preset of commands
    def determine_preset(self):
        pass  # Derived classes will implement this method to determine and apply presets

	# Apply the preset by sending the corresponding topic/payload tuples to the hardware
    def apply_preset(self, preset_name):
        for command, payload in self.presets[preset_name]:
            self.publish_to_reactor(topic, payload, True)

