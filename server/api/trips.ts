import getField from "~/server/utils/getField";

export default defineEventHandler(async (event) => {
  let tripsData = getTripData();
  let trips: Array<{
    tripId: number;
    tripName: string;
    totalTime: number;
    channelToken: string;
    temperature: number,
    humidity: number,
    gps: {
      latitude: number;
      longitude: number;
    };
    personsIn: number;
    personsOut: number;
    personsTotal: number;
    stopName: string;
    stops: typeof tripsData[0]["stops"]
  }> = [];
  for (let trip of tripsData) {
    const { tripId, tripName, totalTime, channelToken, stops } = trip;
    trips.push({
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
      stops
    });
  }
  return trips;
});
