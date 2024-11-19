import { getInterpolatedCoordinates } from "../utils/getInterpolatedCoordinates";
import { getTripData } from "../utils/getTripData";
import { getMqttClient } from "../utils/getMqttClient";

const CHANNEL_ID = "trip13601";
const MQTT_TOPIC_SUBSCRIBE = `${CHANNEL_ID}/gps`;

export default defineEventHandler(async (event) => {
  const trips = getTripData();
  const mqttClient = await getMqttClient();
  let totalTimePassed = 0;
  setInterval(() => {
    const coordinates = getInterpolatedCoordinates(trips[0], totalTimePassed);
    totalTimePassed += 1;
    const dataToSend = {
      latitude: coordinates.lat,
      longitude: coordinates.lng,
    };
    const info = mqttClient.publish(
      MQTT_TOPIC_SUBSCRIBE,
      JSON.stringify({
        data: dataToSend,
        write: true,
      })
    );
    console.log({message: "Coordinates sent to MQTT Broker", info, dataToSend});
  }, 1000);
  return getInterpolatedCoordinates(trips[0], totalTimePassed);
});
