from baseclasses import mqtt_actor as actor

class cronjob(actor):
	type = "cronjob"
	location = "internal"
	name = "cronjob" 
	topic = "actor/cronjob"

	# dont print every action, avoid spam pls
	invoke_action_verbose = False

	states_internal = {
		"state/time/hour": 0,
		"state/time/minute": 0,
		"state/time/daytime": "day",
		"state/bernie/light/mode": "off" # to switch between day and evening
	}

	# called every minute
	def minute(self, payload):
		self.publish_state("state/time/minute", payload)

	# called every hour
	def hour(self, payload):
		self.publish_state("state/time/hour", payload)
		# adjust daytime
		if int(payload) == 7:
			self.daytime("day")
		elif int(payload) == 20:
			self.daytime("evening")
		elif int(payload) == 1:
			self.daytime("night")

	# called when daytime is changing
	def daytime(self, payload):
		self.publish_state("state/time/daytime", payload)
		# switch to a nicer lighting in the evening
		if self.states_internal["state/bernie/light/mode"] == "on" \
			and payload != "day":
			self.publish_state("state/bernie/light/mode", "mood")
		elif self.states_internal["state/bernie/light/mode"] == "mood" \
			and payload == "day":
			self.publish_state("state/bernie/light/mode", "on")

	actions = {
		"minute": minute,
		"hour": hour,
		"daytime": daytime
	}




class lightswitch_bernie_shelly(actor):
	type = "lightswitch"
	location = "bernie"
	name = "shelly"
	topic = "actor/bernie/lightswitch/shelly"

	states_internal = {
		"state/time/daytime": "day",
		"state/bernie/light/mode": "off"
	}

	def turn_on(self, payload):
		if self.states_internal["state/time/daytime"] == "day":
			self.publish_state("state/bernie/light/mode", "on")
		else:
			self.publish_state("state/bernie/light/mode", "mood")

	def turn_off(self, payload):
		self.publish_state("state/bernie/light/mode", "off")

	def toggle(self, payload):
		if int(self.states_internal["state/bernie/light/mode"]) > 0:
			self.turn_off('')
		else:
			self.turn_on('')

	actions = {
		"turn_on": turn_on,
		"turn_off": turn_off,
		"toggle": toggle
	}