# python 3.6

from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883

class actor:
	def __init__(self, name):
		self.name = name
		self.type = self.__class__.__name__
		self.topic = "actor/" + self.type + "/" + self.name

		self.client = mqtt_client.Client(self.type + "_" + self.name)
		self.client.on_message = self.on_message
		self.client.connect(broker, port)
		self.client.subscribe(self.topic + "/#")
		self.client.loop_start()

	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			print("Connected to MQTT Broker!")
		else:
			print("Failed to connect, return code %d\n", rc)
	
	def on_message(self, client, userdata, msg):
		print(f"actor `{self.name}` ({self.type}) received `{msg.payload.decode()}` from `{msg.topic}` topic")
		commandstring = msg.topic.replace(self.topic + "/", '', 1)
		if commandstring:
			print(f"Received command `{commandstring}`, executing...")
			try:
				command = getattr(self, commandstring)
				print(command)
				command()
			except:
				print(f"Command `{commandstring}` not found!")



class lightswitch(actor):
	def bobo():
		print("Selber Bobo")


zimmer = lightswitch("zimmer")
kueche = lightswitch("kueche")

