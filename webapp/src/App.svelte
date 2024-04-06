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

    <div class="flex justify-center ">
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
            <div class="h-10 w-min bg-slate-500 rounded-xl p-2 font-bold">
              <p>{timeseries}🔽</p>
            </div>
          {/if}
        </button>
        <ul
          class="bg-slate-500 rounded-box w-min rounded-lg py-2"
          style:visibility={isDropdownOpen ? "visible" : "hidden"}
        >
          <li class="hover:bg-slate-800 text-left">
            <button
              class="btn text-white p-1 w-full text-left"
              on:click={() => timeseries = "DAILY"} on:click={handleDropdownClick}>DAILY</button
            >
          </li>
          <li class="hover:bg-slate-800">
            <button
              class="btn text-white p-1 w-full text-left"
              on:click={() => timeseries = "WEEKLY"} on:click={handleDropdownClick}>WEEKLY</button
            >
          </li>
          <li class="hover:bg-slate-800">
            <button
              class="btn text-white p-1 w-full text-left"
              on:click={() => timeseries = "MONTHLY"} on:click={handleDropdownClick}>MONTHLY</button
            >
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="">
    {#key timeseries}
      {#await fetchData()}
        <div class="flex flex-col items-center text-white">
          <p>Loading...</p>
        </div>
      {:then chart}
        <div class="sm:grid sm:grid-rows-3 sm:grid-flow-col sm:gap-3">
          <div class="flex flex-col items-center">
            <p class="text-white">QQQ</p>
            <Ferdous
              width={420}
              height={420}
              theme={THEME}
              graphData={graphData.filter((item) => item.symbol == "QQQ")}
            />
          </div>

          <div class="flex flex-col items-center">
            <p class="text-white">PANW</p>
            <Ferdous
              width={420}
              height={420}
              theme={THEME}
              graphData={graphData.filter((item) => item.symbol == "PANW")}
            />
          </div>

          <div class="flex flex-col items-center">
            <p class="text-white">TSLA</p>
            <Ferdous
              width={420}
              height={420}
              theme={THEME}
              graphData={graphData.filter((item) => item.symbol == "TSLA")}
            />
          </div>

          <div class="flex flex-col items-center">
            <p class="text-white">AAPL</p>
            <Ferdous
              width={420}
              height={420}
              theme={THEME}
              graphData={graphData.filter((item) => item.symbol == "AAPL")}
            />
          </div>

          <div class="flex flex-col items-center">
            <p class="text-white">MSFT</p>
            <Ferdous
              width={420}
              height={420}
              theme={THEME}
              graphData={graphData.filter((item) => item.symbol == "MSFT")}
            />
          </div>

          <div class="flex flex-col items-center">
            <p class="text-white">NVDA</p>
            <Ferdous
              width={420}
              height={420}
              theme={THEME}
              graphData={graphData.filter((item) => item.symbol == "NVDA")}
            />
          </div>
        </div>
      {/await}
    {/key}
  </div>
</main>

<style lang="postcss">
</style>
