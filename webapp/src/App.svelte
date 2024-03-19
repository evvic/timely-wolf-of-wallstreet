<script lang="ts">
  // import "../app.css";
  import Ferdous from "./components/Ferdous.svelte"
  const key: string = import.meta.env.VITE_PUBLIC_STOCK_API_KEY;

  interface stock {
    name: string | void;
    price: number | void;
    pChange: number | void;
  }

  const data = [
        { time: '2019-04-11', value: 80.01 },
        { time: '2019-04-12', value: 96.63 },
        { time: '2019-04-13', value: 76.64 },
        { time: '2019-04-14', value: 81.89 },
        { time: '2019-04-15', value: 74.43 },
        { time: '2019-04-16', value: 80.01 },
        { time: '2019-04-17', value: 96.63 },
        { time: '2019-04-18', value: 76.64 },
        { time: '2019-04-19', value: 81.89 },
        { time: '2019-04-20', value: 74.43 },
    ];

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
    <Ferdous width={420} height={420} data={data}/>  
  </div>
</main>

<style lang="postcss">
</style>
