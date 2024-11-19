import { getCurrentStop } from "./getCurrentStop";
import type { getTripData } from "./getTripData";

export const getInterpolatedCoordinates = (tripData: ReturnType<typeof getTripData>[0], elapsedTime: number) => {
    const stop = getCurrentStop(tripData, elapsedTime);
    if(stop.status === "On stop" || stop.status === "Trip completed") {
        return {
            lat: stop?.stop?.lat,
            lng: stop?.stop?.lon,
            done: stop.status === "Trip completed",
            stopName: stop?.stop?.stopName
        };
    }
    else {
        const stopRecalculate = stop as { from: typeof tripData.stops[0], to: typeof tripData.stops[0] };
        // interpolação linear
        const timeDiff = elapsedTime - (stopRecalculate.from.time + stopRecalculate.to.time);
        const timeTotal = stopRecalculate.to.time - stopRecalculate.from.time;
        const lat = stopRecalculate.from.lat + (stopRecalculate.to.lat - stopRecalculate.from.lat) * (timeDiff / timeTotal);
        const lon = stopRecalculate.from.lon + (stopRecalculate.to.lon - stopRecalculate.from.lon) * (timeDiff / timeTotal);
        return {
            lat: lat,
            lng: lon,
            done: false,
            stopName: stop?.stop?.stopName
        };
    }
}