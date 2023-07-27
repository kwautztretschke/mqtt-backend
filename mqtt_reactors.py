from baseclasses import mqtt_reactor as reactor

class bedroom_floorlamp(reactor):
	type = "tasmota"
	location = "bedroom"
	name = "floorlamp"
	topic = "reactor/bedroom/floorlamp"

	states = {
		"bedroom/light/mode": "off"
	}

	def determine_preset(self):
		if self.states["bedroom/light/mode"] == "mood":
			self.client.publish("cmnd/tasmota_floorlamp/Power", "on", qos=1, retain=True)
		else:
			self.client.publish("cmnd/tasmota_floorlamp/Power", "off", qos=1, retain=True)


class bedroom_whiteboard(reactor):
	type = "monochrome_led_strip"
	location = "bedroom"
	name = "whiteboard"
	topic = "reactor/ESPwhiteboard"

	states = {
		"bedroom/light/mode": "off",
		"bedroom/music": "off",
	}

	presets = {
		"off": [
			("power", "off")
		],
		"daytime_light": [
			("power", "on"),
			("focus", "solidColor"),
			("color", "00FFFF"),
			("brightness", "128")
		],
		"evening_light": [
			("power", "on"),
			("focus", "solidColor"),
			("color", "FF00FF"),
			("brightness", "128")
		],
		"daytime_music": [
			("power", "on"),
			("focus", "syncedColor"),
			("color", "00FF00"),
			("brightness", "255")
		],
		"evening_music": [
			("power", "on"),
			("focus", "syncedColor"),
			("color", "FF00FF"),
			("brightness", "128")
		]
	}

	passthrough_states = {
		"bedroom/light/brightness": "brightness",
	}

	def determine_preset(self):
		# Implement the logic to determine and apply the appropriate preset based on the states
		if self.states["bedroom/light/mode"] == "off":
			self.apply_preset("off")
		elif self.states["bedroom/light/mode"] == "on":
			self.apply_preset("daytime_light")
		elif self.states["bedroom/light/mode"] == "mood":
			self.apply_preset("mood_light")
		elif self.states["bedroom/light/mode"] == "party":
			if self.states["bedroom/music"] == "off":
				self.apply_preset("silent_party")
			else:
				self.apply_preset("music_party")