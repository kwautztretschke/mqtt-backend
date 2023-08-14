from baseclasses import mqtt_actor as actor

class cronjob(actor):
	type = "cronjob"
	location = "internal"
	name = "cronjob" 
	topic = "actor/cronjob"

	# dont print every action, avoid spam pls
	invoke_command_verbose = False

	states = {
		"time/hour": 0,
		"time/minute": 0,
		"time/daytime": "day",
		"bedroom/light/mode": "off" # to switch between day and evening
	}

	# called every minute
	def minute(self, payload):
		self.publish_state("time/minute", payload)

	# called every hour
	def hour(self, payload):
		self.publish_state("time/hour", payload)
		# adjust daytime
		if int(payload) == 7:
			self.daytime("day")
		elif int(payload) == 20:
			self.daytime("evening")
		elif int(payload) == 1:
			self.daytime("night")

	# called when daytime is changing
	def daytime(self, payload):
		self.publish_state("time/daytime", payload)

		# switch lighting if it's on
		if self.states["bedroom/light/mode"] != "off":
			if payload == "day":
				self.publish_state("bedroom/light/mode", "on")
			elif payload == "evening":
				self.publish_state("bedroom/light/mode", "soft")
			elif payload == "night":
				self.publish_state("bedroom/light/mode", "mood")

	commands = {
		"minute": minute,
		"hour": hour,
		"daytime": daytime
	}


class lightswitch_bedroom(actor):
	type = "shelly"
	location = "bedroom"
	name = "lightswitch"
	topic = "actor/bedroom/lightswitch"

	states = {
		"time/daytime": "day",
		"bedroom/light/mode": "off"
	}

	def turn_on(self, payload):
		if self.states["time/daytime"] == "day":
			self.publish_state("bedroom/light/mode", "on")
		elif self.states["time/daytime"] == "evening":
			self.publish_state("bedroom/light/mode", "soft")
		elif self.states["time/daytime"] == "night":
			self.publish_state("bedroom/light/mode", "mood")
		else: 
			print("Error: state/time/daytime is fucked up")

	def turn_off(self, payload):
		self.publish_state("bedroom/light/mode", "off")

	def toggle(self, payload):
		if self.states["bedroom/light/mode"] != "off":
			self.turn_off('')
		else:
			self.turn_on('')

	commands = {
		"turn_on": turn_on,
		"turn_off": turn_off,
		"toggle": toggle
	}
