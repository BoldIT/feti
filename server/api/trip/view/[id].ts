import getField from "~/server/utils/getField";

export default defineEventHandler(async (event) => {
  const tripId = getRouterParam(event, "id");
  if(!tripId) {
    throw new Error("ID não encontrado");
  }
  const trip = getTripData().find((trip) => {
    return String(trip.tripId) === String(tripId);
  });
  if(!trip) {
    throw new Error("Trip não foi encontrada");
  }
  const {tripName, totalTime, channelToken, stops} = trip;
  return {
    tripId,
    tripName,
    totalTime,
    channelToken,
    temperature: await getField(tripId, "temperature"),
    humidity: await getField(tripId, "humidity"),
    gps: await getField(tripId, "gps"),
    personsIn: await getField(tripId, "persons_in"),
    personsOut: await getField(tripId, "persons_in"),
    personsTotal: await getField(tripId, "persons_total"),
    stopName: await getField(tripId, "stop_name"),
    stops,
  }
});
