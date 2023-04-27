### MQTT Signal Flow Example
1. Wall Lightswitch is pressed
- Mqtt command is sent to topic "actor/lightswitch/toggle"
- message may or may not contain payload (no payload for this example)
2. Corresponding python actor "lightswitch which is subscribed to all actor/lightswitch/# topics receives message
- logic is triggered depending on current states (e.g. daytime==evening)
- new state is published as retained message (e.g. state/bernie/light/mode, payload "moodlight")
3. All python reactors subscribed to the respective states receive new state
- hardware specific command(s) get(s) sent via mqtt (also retained message, just cause)
- in our case reactor::table publishes payload "0xFF0000" to reactor/table/color
4. ESP with device name "table" receives message
- acts accordingly depending on what topic and payload were received
- since esp is subscribed to "reactor/table/#", all commands get received and topic can be parsed
