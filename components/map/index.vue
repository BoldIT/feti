<script setup lang="ts">
import { GoogleMap, CustomMarker } from "vue3-google-map";
const tripsStore = useTripsStore();
const {tripsRefresh} = tripsStore;
const { tripsData } = storeToRefs(tripsStore);
const center = computed(() => {
  return {
    lat: tripsData.value?.[0].gps.latitude,
    lng: tripsData.value?.[0].gps.longitude,
  };
});
let interval: string | number | NodeJS.Timeout | undefined;
onMounted(() => {
  console.log("refreshing...")
  interval = setInterval(() => {
    tripsRefresh();
  }, 8000);
});
onUnmounted(() => {
  if(interval) {
    clearInterval(interval);
  }
})
</script>
<template>
  <GoogleMap
    api-key="AIzaSyAxZG8HgntTJzBsSXF3oW_sThwP-fyL9P4"
    style="width: 100%; height: 100%"
    :center="center"
    :zoom="11"
  >
    <CustomMarker
      v-for="trip of tripsData"
      :key="trip.tripId"
      :options="{
        position: {
          lat: trip.gps.latitude,
          lng: trip.gps.longitude,
        },
      }"
    >
      <img style="width: 80px" src="/bus.png" />
    </CustomMarker>
  </GoogleMap>
</template>
