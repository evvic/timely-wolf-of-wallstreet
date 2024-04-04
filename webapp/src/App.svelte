<script lang="ts">
  // import "../app.css";
  import Ferdous from "./components/Ferdous.svelte";

  let timeseries = "WEEKLY";

  let graphData: { time: string; value: number; symbol: string }[] = [];

  // Define the theme object here
  const THEME = {
    chart: {
        layout: {
          background: {
            type: 'solid',
            color: '#2B2B43',
          },
          lineColor: '#2B2B43',
          textColor: 'white',
          fontWeight: 'bold',
        },
        watermark: {
          color: 'rgba(0, 0, 0, 0)',
        },
        crosshair: {
          color: '#758696',
        },
        grid: {
          vertLines: {
            color: '#2B2B43',
          },
          horzLines: {
            color: '#363C4E',
          },
        },
      },
      series: {
        topColor: 'rgba(32, 226, 47, 0.56)',
        bottomColor: 'rgba(32, 226, 47, 0.04)',
        lineColor: 'rgba(32, 226, 47, 1)',
      },
      
  };

  const trackedSymbols = ["QQQ", "PANW", "TSLA", "AAPL", "MSFT", "NVDA"];

  // function getStocks() {
  //   console.log(graphData);
  // }

  async function fetchData() {
    graphData = []
    for (let i = 0; i < trackedSymbols.length; i++) {
      await fetch(
        `https://65f7764db2fafbd9238d.appwrite.global/stocks?symbol=${trackedSymbols[i]}&timeseries=${timeseries}&offset=1`,
      )
        .then((response) => response.json())
        .then((data) => {
          for (let j = 0; j < data.documents.length; j++) {
            const time = data.documents[j].date.slice(0, 10);
            const value = data.documents[j].price;
            const cur = { time: time, value: value, symbol: trackedSymbols[i] };

            graphData = [...graphData, cur];
          }
          console.log(graphData);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }
</script>

<main class="h-dvh w-screen bg-neutral-900 overflow-y-scroll">
  <div class="flex-col text-center mb-2">
    <h1
      class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white"
    >
      Nancy's Top 5 Stocks
    </h1>
    <button
      class={`bg-sky-500 rounded-xl p-2 ${timeseries === "DAILY" ? "bg-green-400" : "bg-sky-500"}`}
      on:click={() => (timeseries = "DAILY")}
    >
      Daily
    </button>
    <button
      class={`bg-sky-500 rounded-xl p-2 ${timeseries === "WEEKLY" ? "bg-green-400" : "bg-sky-500"}`}
      on:click={() => (timeseries = "WEEKLY")}
    >
      Weekly
    </button>
    <button
      class={`bg-sky-500 rounded-xl p-2 ${timeseries === "MONTHLY" ? "bg-green-400" : "bg-sky-500"}`}
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
        <Ferdous width={420} height={420} {graphData} theme={THEME} />
      </div>
    {/await}
  {/key}
</main>

<style lang="postcss">
</style>
