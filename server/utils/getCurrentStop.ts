import { getTripData } from "./getTripData";
export function getCurrentStop(tripData: ReturnType<typeof getTripData>[0], elapsedTime: number) {
    let totalTimePassed = 0;
    for (let i = 0; i < tripData.stops.length; i++) {
        // Adiciona o tempo da parada atual ao tempo total acumulado
        totalTimePassed += tripData.stops[i].time;

        // Se o tempo passado já ultrapassa ou iguala o elapsedTime
        if (totalTimePassed >= elapsedTime) {
            // Verifica se o ônibus está exatamente em uma parada ou entre duas paradas
            if (totalTimePassed === elapsedTime) {
                return {
                    status: "On stop",
                    stop: tripData.stops[i]
                };
            } else {
                return {
                    status: "Between stops",
                    from: tripData.stops[i - 1],
                    to: tripData.stops[i]
                };
            }
        }
    }

    // Caso o tempo ultrapasse o último ponto da viagem, considera a viagem concluída
    return {
        status: "Trip completed",
        stop: tripData.stops[tripData.stops.length - 1]
    }
}