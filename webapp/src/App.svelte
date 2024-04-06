<script lang="ts">
  // import "../app.css";
  import Ferdous from "./components/Ferdous.svelte";
  import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
  import { ChevronDownIcon } from "@heroicons/vue/20/solid";

  let timeseries = "WEEKLY";

  let graphData: { time: string; value: number; symbol: string }[] = [];

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

    <template>
      <Menu as="div" class="relative inline-block text-left">
        <div>
          <MenuButton
            class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          >
            Options
            <ChevronDownIcon
              class="-mr-1 h-5 w-5 text-gray-400"
              aria-hidden="true"
            />
          </MenuButton>
        </div>

        <transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <MenuItems
            class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
          >
            <div class="py-1">
              <MenuItem v-slot={active}>
                <a
                  
                  class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']"
                  >Account settings</a
                >
              </MenuItem>
              <MenuItem v-slot={active}>
                <a
                  href="#"
                  :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']"
                  >Support</a
                >
              </MenuItem>
              <MenuItem v-slot={active}>
                <a
                  href="#"
                  :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm']"
                  >License</a
                >
              </MenuItem>
              <form method="POST" action="#">
                <MenuItem v-slot={active}>
                  <button
                    type="submit"
                    :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block w-full px-4 py-2 text-left text-sm']"
                    >Sign out</button
                  >
                </MenuItem>
              </form>
            </div>
          </MenuItems>
        </transition>
      </Menu>
    </template>
  </div>
  {#key timeseries}
    {#await fetchData()}
      <div class="flex flex-col items-center text-white">
        <p>Loading...</p>
      </div>
    {:then chart}
      <div class="grid grid-rows-3 grid-flow-col gap-4">
        <div class="flex flex-col items-center mb-10 text-white">
          QQQ
          <Ferdous
            width={420}
            height={420}
            graphData={graphData.filter((item) => item.symbol == "QQQ")}
          />
        </div>
        <div class="flex flex-col items-center mb-10 text-white">
          PANW
          <Ferdous
            width={420}
            height={420}
            graphData={graphData.filter((item) => item.symbol == "PANW")}
          />
        </div>
        <div class="flex flex-col items-center mb-10 text-white">
          TSLA
          <Ferdous
            width={420}
            height={420}
            graphData={graphData.filter((item) => item.symbol == "TSLA")}
          />
        </div>
        <div class="flex flex-col items-center mb-10 text-white">
          AAPL
          <Ferdous
            width={420}
            height={420}
            graphData={graphData.filter((item) => item.symbol == "AAPL")}
          />
        </div>
        <div class="flex flex-col items-center mb-10 text-white">
          MSFT
          <Ferdous
            width={420}
            height={420}
            graphData={graphData.filter((item) => item.symbol == "MSFT")}
          />
        </div>
        <div class="flex flex-col items-center mb-10 text-white">
          NVDA
          <Ferdous
            width={420}
            height={420}
            graphData={graphData.filter((item) => item.symbol == "NVDA")}
          />
        </div>
      </div>
    {/await}
  {/key}
</main>

<style lang="postcss">
</style>
