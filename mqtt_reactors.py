from baseclasses import mqtt_reactor as reactor

class bedroom_whiteboard(reactor):
    type = "monochrome_led_strip"
    location = "bedroom"
    name = "whiteboard"
    topic = "reactor/bedroom/whiteboard"

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
            ("program", "solidColor"),
            ("color", "00FFFF"),
            ("brightness", "128")
        ],
        "mood_light": [
            ("power", "on"),
            ("program", "solidColor"),
            ("color", "FF0000"),
            ("brightness", "64")
        ],
        "silent_party": [
            ("power", "on"),
            ("program", "solidColor"),
            ("color", "00FF00"),
            ("brightness", "255")
        ],
        "music_party": [
            ("power", "on"),
            ("program", "syncedColor"),
            ("color", "00FF00"),
            ("brightness", "255")
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