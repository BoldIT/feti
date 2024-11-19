import mqtt from "mqtt";
export const getMqttClient = () => {
  return new Promise<mqtt.MqttClient>((resolve, reject) => {
    const MQTT_CLIENT_ID = "ofdrsXZPBNw6xF7acIfmlmQq4sGNKwNC";
    const MQTT_BROKER = "mqtts://mqtt.beebotte.com";
    const MQTT_USER = "ofdrsXZPBNw6xF7acIfmlmQq4sGNKwNC";
    const MQTT_PASSWORD = "ofdrsXZPBNw6xF7acIfmlmQq4sGNKwNC";
    const MQTT_PORT = 8883;
    const client = mqtt.connect(MQTT_BROKER, {
      clientId: MQTT_CLIENT_ID,
      username: MQTT_USER,
      password: MQTT_PASSWORD,
      port: MQTT_PORT,
    });
    client.on("connect", () => {
      console.log("Connected to MQTT Broker");
      resolve(client);
    });
    client.on("error", (error) => {
      console.log("Error:", error);
      reject(error);
    });
  });
};
export default getMqttClient;
