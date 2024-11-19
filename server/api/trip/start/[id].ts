export default defineEventHandler(async (event) => {
  const tripId = getRouterParam(event, "id");
  if (!tripId) {
    throw new Error("ID não encontrado");
  }
  const trip = getTripData().find((trip) => {
    return String(trip.tripId) === String(tripId);
  });
  if (!trip) {
    throw new Error("Trip não foi encontrada");
  }

  const channelId = `trip${tripId}`;
  const MqttTopicGps = `${channelId}/gps`;
  const MqttTopicStopName = `${channelId}/stop_name`;

  const mqttClient = await getMqttClient();
  let totalTimePassed = 0;
  setInterval(() => {
    const coordinates = getInterpolatedCoordinates(trip, totalTimePassed);
    totalTimePassed += 1;
    const dataToSend = {
      latitude: coordinates.lat,
      longitude: coordinates.lng,
    };
    mqttClient.publish(
      MqttTopicGps,
      JSON.stringify({
        data: dataToSend,
        write: true,
      })
    );
    mqttClient.publish(
      MqttTopicStopName,
      JSON.stringify({
        data: coordinates.stopName,
        write: true,
      })
    );
  }, 1000);
  return getInterpolatedCoordinates(trip, totalTimePassed);
});
