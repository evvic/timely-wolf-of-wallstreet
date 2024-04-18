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
          type: "solid",
          color: "#2B2B43",
        },
        lineColor: "#2B2B43",
        textColor: "white",
        fontWeight: "bold",
      },
      watermark: {
        color: "rgba(0, 0, 0, 0)",
      },
      crosshair: {
        color: "#758696",
      },
      grid: {
        vertLines: {
          color: "#2B2B43",
        },
        horzLines: {
          color: "#363C4E",
        },
      },
    },
    series: {
      topColor: "rgba(32, 226, 47, 0.56)",
      bottomColor: "rgba(32, 226, 47, 0.04)",
      lineColor: "rgba(32, 226, 47, 1)",
    },
  };

  const trackedSymbols = ["QQQ", "PANW", "TSLA", "AAPL", "MSFT", "NVDA"];

  const mockPoliticianData = [
    { symbol: "AAPL", tradeDate: "2024-04-18", type: "SELL", amount: 1000 },
    { symbol: "PANW", tradeDate: "2024-04-13", type: "BUY", amount: 5000 },
    { symbol: "NVDA", tradeDate: "2024-04-09", type: "BUY", amount: 25000 },
  ];

  async function fetchData() {
    graphData = [];
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

  let isDropdownOpen = false;

  const handleDropdownClick = () => {
    isDropdownOpen = !isDropdownOpen;
  };
  //figure out type of these 2 bitches
  const handleDropdownFocusLoss = ({
    relatedTarget,
    currentTarget,
  }: {
    relatedTarget: any;
    currentTarget: any;
  }) => {
    if (
      relatedTarget instanceof HTMLElement &&
      currentTarget.contains(relatedTarget)
    )
      return;
    isDropdownOpen = false;
  };
</script>

<main class="h-dvh w-screen bg-neutral-900 overflow-y-scroll">
  <div class="flex-col text-center mb-2">
    <h1
      class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white"
    >
      Nancy's Top 5 Stocks
    </h1>

    <div class="">
      <div class="" on:focusout={handleDropdownFocusLoss}>
        <button class="btn m-1" on:click={handleDropdownClick}>
          {#if isDropdownOpen}
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              class="inline-block h-8 w-8 stroke-current bg-slate-500 rounded-lg"
            >
              <title>Close Dropdown</title>
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          {:else}
            <div
              class="h-10 w-min bg-slate-500 rounded-xl p-2 font-bold text-white"
            >
              <p>{timeseries}🔽</p>
            </div>
          {/if}
        </button>
        <ul
          class="bg-slate-500 rounded-box w-min rounded-lg py-2 font-bold"
          style:visibility={isDropdownOpen ? "visible" : "hidden"}
        >
          <li class="hover:bg-slate-800 text-left">
            <button
              class="btn text-white p-1 w-full text-left"
              on:click={() => (timeseries = "DAILY")}
              on:click={handleDropdownClick}>DAILY</button
            >
          </li>
          <li class="hover:bg-slate-800">
            <button
              class="btn text-white p-1 w-full text-left"
              on:click={() => (timeseries = "WEEKLY")}
              on:click={handleDropdownClick}>WEEKLY</button
            >
          </li>
          <li class="hover:bg-slate-800">
            <button
              class="btn text-white p-1 w-full text-left"
              on:click={() => (timeseries = "MONTHLY")}
              on:click={handleDropdownClick}>MONTHLY</button
            >
          </li>
        </ul>
      </div>
    </div>
  </div>

  <div>
    {#key timeseries}
      {#await fetchData()}
        <div class="flex flex-col items-center text-white">
          <p>Loading...</p>
        </div>
      {:then chart}
        <div
          class="sm:grid sm:grid-rows-2 sm:grid-flow-col sm:gap-x-28 sm:gap-y-10 justify-center"
        >
          {#each trackedSymbols as graph}
            <div class="bg-slate-500 p-2 rounded-lg w-min">
              <p class="text-white font-bold text-xl">{graph}</p>
              <Ferdous
                width={520}
                height={420}
                theme={THEME}
                graphData={graphData.filter((item) => item.symbol == graph)}
              />
            </div>
          {/each}
        </div>
      {/await}
    {/key}
  </div>

  <div class="flex text-center flex-col items-center pb-8">
    <p class="text-white text-2xl font-bold mt-4">Nancy Pelosi Recent Trades</p>

    <table class="table-fixed bg-slate-800 rounded-xl w-9/12 ">
      <thead class="w-full border-b-2 border-slate-500 text-slate-200">
        <tr>
          <th class="">Symbol</th>
          <th class="">Trade Date</th>
          <th class="">Type</th>
          <th class="">Amount</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-slate-500 ">
        {#each mockPoliticianData as item}
        <!-- border-b-2 border-slate-500 -->
          <tr class="">
            <td class="text-blue-300 p-4">{item.symbol}</td>
            <td class="text-white">{item.tradeDate}</td>
            <td class="text-white">{item.type}</td>
            <td class="text-white">{item.amount}</td>

          </tr>
        {/each}
      </tbody>

      <!-- {#key timeseries} -->
      <!-- needed for when there is actual data coming from API -->
      <!-- {#await fetchData()} 
        <div class="flex flex-col items-center text-white">
          <p>Loading...</p>
        </div>
      {:then chart} -->

      <!-- {/await} -->
      <!-- {/key} -->
    </table>
  </div>
</main>

<style lang="postcss">
</style>
