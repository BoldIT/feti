<script setup lang="ts">
const tripStore = useTripsStore();
const {tripsRefresh} = tripStore;
const { tripsData, tripsStatus } = storeToRefs(tripStore);
let interval: string | number | NodeJS.Timeout | undefined;
onMounted(() => {
  interval = setInterval(() => {
    if(tripsStatus.value == 'success' || tripsStatus.value == 'error') {
      tripsRefresh();
    }
  }, 1000)
})
onUnmounted(() => {
  clearInterval(interval)
})
</script>

<template>
  <UContainer class="main-container" v-if="tripsData?.length && tripsData.length > 0">
    <div class="main-header">
      <img src="/logo.svg" style="height: 100%" />
    </div>
    <div class="map-container">
      <ClientOnly>
        <Map></Map>
      </ClientOnly>
    </div>
    <div class="trips">
      <UCard v-for="trip of tripsData">
        <div style="display: flex; align-items: center; gap: 50px">
          <UIcon
            name="i-material-symbols:directions-bus-sharp"
            class="w-9 h-9"
            style="width: 20px"
          />
          <div style="width: 80%">
            <h3>{{ trip?.tripName }}</h3>
          </div>
        </div>

        <div style="display: flex; align-items: center; gap: 50px">
          <UIcon
            name="i-material-symbols:file-map-rounded"
            class="w-9 h-9"
            style="width: 20px"
          />
          <div style="width: 80%">
            <h3>{{ trip?.stopName }}</h3>
          </div>
        </div>

        <div class="icon-container">
          <div class="icon-box">
            <UIcon name="mdi:sun-thermometer-outline" class="icon" />
            {{trip.temperature}}ºC
          </div>
          <div class="icon-box">
            <UIcon name="material-symbols:water-voc-rounded" class="icon" />
            {{trip.humidity}}%
          </div>
          <div class="icon-box">
            <UIcon name="material-symbols:group" class="icon" />
            {{trip.personsTotal}}
          </div>
        </div>
      </UCard>
    </div>
  </UContainer>
  <div v-else>
    Carregando...
  </div>
</template>

<style>
.main-container {
  max-width: 414px;
  background: gray;
  height: 100vh;
  background: #fff;
  overflow: hidden;
  padding: 10px;
  border-radius: 9px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.main-header {
  width: 100%;
  height: 50px;
  background: #fff;
  padding: 2px;
  display: flex;
  justify-content: center;
}
.trips {
  width: 100%;
  height: calc(50vh - 70px);
  background: #fff;
  overflow-x: hidden;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.map-container {
  width: 100%;
  height: 50vh;
  background: #ccc;
}
.icon-container {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-top: 30px;
}
.icon-box {
  display: flex;
  width: 100%;
  background: #f2f2f2;
  color: black;
  padding: 3px;
  border-radius: 18px;
  flex-direction: column;
  align-items: center;
}
.icon {
  font-size: 30px;
}
</style>
