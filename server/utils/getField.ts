export default async (tripId: number | string, field: string) => {
  try {
    const url = `https://api.beebotte.com/v1/data/read/trip${tripId}/${field}?limit=1`;
    const data = await $fetch(url, {
      headers: {
        accept: "application/json, text/javascript, */*; q=0.01",
        "X-Auth-Token": getTripData().find(e => String(e.tripId) == String(tripId))?.channelToken || "",
        "content-type": "application/json; charset=UTF-8",
      },
      body: null,
      method: "GET",
    });
    return (data as any[])?.[0]?.data;
  } catch (err) {
    console.log(err);
    return 0;
  }
};
