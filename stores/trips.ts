export const useTripsStore = defineStore("trips-store", () => {
  const {
    data: tripsData,
    status: tripsStatus,
    refresh: tripsRefresh,
  } = useFetch("/api/trips");
  return {
    tripsData,
    tripsStatus,
    tripsRefresh,
  };
});
