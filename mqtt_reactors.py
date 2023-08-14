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
		if self.states["bedroom/light/mode"] == "soft":
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
		"bright_cyan": [
			("power", "on"),
			("color", "00FFFF"),
			("brightness", "255")
		],
		"bright_green": [
			("power", "on"),
			("color", "00FF00"),
			("brightness", "255")
		],
		"soft_magenta": [
			("power", "on"),
			("color", "FF00FF"),
			("brightness", "128")
		],
		"dim_red": [
			("power", "on"),
			("color", "FF0000"),
			("brightness", "32")
		]
	}

	passthrough_states = {
		"bedroom/light/brightness": "brightness",
	}

	def determine_preset(self):
		# Apply some color presets depending on light state
		if self.states["bedroom/light/mode"] == "off":
			self.apply_preset("off")
		elif self.states["bedroom/light/mode"] == "on":
			self.apply_preset("bright_cyan")
		elif self.states["bedroom/light/mode"] == "soft":
			self.apply_preset("soft_magenta")
		elif self.states["bedroom/light/mode"] == "mood":
			self.apply_preset("dim_red")
		elif self.states["bedroom/light/mode"] == "party":
			self.apply_preset("bright_green")
		else:
			print("Error: state/bedroom/light/mode is fucked up")

		if self.states["bedroom/music"] == "off":
			self.publish_to_reactor("focus", "solidColor", retain=True)
		else:
			self.publish_to_reactor("focus", "simpleSync", retain=True)
		

class RatDerGeleerten(reactor):
	type = "adressable_rgb_strip"
	location = "bedroom"
	name = "RatDerGeleerten"
	topic = "reactor/RatDerGeleerten"

	states = {
		"bedroom/light/mode": "off",
		"bedroom/music": "off",
	}

	presets = {
		"off": [
			("power", "off")
		],
		"bright_orange": [
			("power", "on"),
			("color", "FF8800"),
			("brightness", "255")
		],
		"bright_green": [
			("power", "on"),
			("color", "00FF00"),
			("brightness", "255")
		],
		"bright_magenta": [
			("power", "on"),
			("color", "FF00FF"),
			("brightness", "255")
		],
		"soft_magenta": [
			("power", "on"),
			("color", "FF00FF"),
			("brightness", "128")
		],
		"dim_red": [
			("power", "on"),
			("color", "FF0000"),
			("brightness", "32")
		]
	}

	passthrough_states = {
		"bedroom/light/brightness": "brightness",
	}

	def determine_preset(self):
		# Apply some color presets depending on light state
		if self.states["bedroom/light/mode"] == "off":
			self.apply_preset("off")
		elif self.states["bedroom/light/mode"] == "on":
			self.apply_preset("bright_orange")
		elif self.states["bedroom/light/mode"] == "soft":
			self.apply_preset("soft_magenta")
		elif self.states["bedroom/light/mode"] == "mood":
			self.apply_preset("dim_red")
		elif self.states["bedroom/light/mode"] == "party":
			self.apply_preset("bright_magenta")
		else:
			print("Error: state/bedroom/light/mode is fucked up")

		if self.states["bedroom/music"] == "off":
			self.publish_to_reactor("focus", "solidColor", retain=True)
		else:
			self.publish_to_reactor("focus", "rippleSync", retain=True)
		