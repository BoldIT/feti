// import getMqttClient from "~/server/utils/getMqttClient";


// const CHANNEL_ID = "dht22";
// const MQTT_TOPIC_SUBSCRIBE_1 = `${CHANNEL_ID}/temperature`;
// const MQTT_TOPIC_SUBSCRIBE_2 = `${CHANNEL_ID}/humidity`;
// const client = getMqttClient();
// client.on("error", (error) => {
//   console.log("Error:", error);
// });
// client.on("connect", () => {
//   console.log("Connected!");
//   client.subscribe(MQTT_TOPIC_SUBSCRIBE_1, (err) => {
//     if (err) {
//       console.log("Error:", err);
//       return;
//     }
//     console.log("Subscribed to:", MQTT_TOPIC_SUBSCRIBE_1);
//   });
// });

// client.on("message", (topic, message) => {
//   console.log({
//     topic,
//     message
//   });
// });
export default defineNuxtPlugin((nuxtApp) => {});
