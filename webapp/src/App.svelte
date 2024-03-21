<script lang="ts">
  // import "../app.css";
  import Ferdous from "./components/Ferdous.svelte";

  const key: string = import.meta.env.VITE_PUBLIC_STOCK_API_KEY;

  interface stock {
    name: string | void;
    price: number | void;
    pChange: number | void;
  }
  let timeseries = "WEEKLY";

  let graphData: { time: string; value: number }[] = [];

  const trackedSymbols = ["QQQ"];

  async function getStocks() {
    console.log(graphData);
  }

  async function fetchData() {
    await fetch(
      `https://65f7764db2fafbd9238d.appwrite.global/stocks?symbol=${trackedSymbols[0]}&timeseries=${timeseries}&offset=1`,
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        graphData = []

        for (let i = 0; i < data.documents.length; i++) {
          const time = data.documents[i].date.slice(0, 10);
          const value = data.documents[i].price;
          const cur = { time: time, value: value };

          graphData = [...graphData, cur];
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }
</script>

<main class="h-screen w-screen bg-neutral-900">
  <div class="flex-col text-center mb-2">
    <h1
      class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white"
    >
      Nancy's Top 5 Stocks
    </h1>
    <button
      class={`bg-sky-500 rounded-xl p-2 ${timeseries === 'DAILY' ? 'bg-green-300' : 'bg-sky-500'}`}
      on:click={() => (timeseries = "DAILY")}
    >
      Daily
    </button>
    <button
      class={`bg-sky-500 rounded-xl p-2 ${timeseries === 'WEEKLY' ? 'bg-green-300' : 'bg-sky-500'}`}
      on:click={() => (timeseries = "WEEKLY")}
    >
      Weekly
    </button>
    <button
      class={`bg-sky-500 rounded-xl p-2 ${timeseries === 'MONTHLY' ? 'bg-green-300' : 'bg-sky-500'}`}
      on:click={() => (timeseries = "MONTHLY")}
    >
      Monthly
    </button>
  </div>
  {#key timeseries}
    {#await fetchData()}
      <div class="flex flex-col items-center text-white">
        <p>Loading...</p>
      </div>
    {:then chart}
      <div class="flex flex-col items-center">
        <Ferdous width={420} height={420} {graphData} />
      </div>
    {/await}
  {/key}
</main>

<style lang="postcss">
</style>
