<script lang="ts">
  // import "../app.css";

  const key: string = import.meta.env.VITE_PUBLIC_STOCK_API_KEY;

  interface stock {
    name: string | void;
    price: number | void;
    pChange: number | void;
  }

  const trackedNames = [
    "Nvidia",
    "Apple",
    "Microsoft",
    "Google",
    "AllianceBernstein Holding LP",
  ];

  const trackedSymbols = ["NVDA", "AAPL", "MSFT", "GOOGL", "AB"];

  let topList: stock[] = [];

  async function getStocks() {
    for (let i = 0; i < trackedSymbols.length; i++) {
      fetch(
        `https://finnhub.io/api/v1/quote?symbol=${trackedSymbols[i]}&token=${key}`,
      )
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          const cur: stock = {
            name: trackedSymbols[i],
            price: data.c,
            pChange: data.dp,
          };
          topList = [...topList, cur];
        })
        .catch((error) => {
          console.log(error);
          return [];
        });
    }
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
      type="button"
      class="rounded-xl bg-blue-500 hover:bg-green-500 p-1 max-h-8 max-w-32 font-bold"
      on:click={getStocks}
    >
      Get Stocks
    </button>
  </div>

  <div class="flex flex-col items-center">
    {#if topList}
      {#each topList as item}
        <div
          class="flex border-zinc-500 bg-zinc-400 font-bold border-2 min-w-64 rounded-xl p-1 mb-2 flex-row justify-between"
        >
          <div class="">
            <p>{item.name}</p>
          </div>

          <div>
            <p>Price: {item.price}</p>
            <p>Change: {item.pChange}%</p>
          </div>
        </div>
      {/each}
    {/if}
  </div>
</main>

<style lang="postcss">
</style>
