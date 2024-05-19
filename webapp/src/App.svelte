<script lang="ts">
  import { onMount } from "svelte";
  import * as Card from "$lib/components/ui/card";
  import { ModeWatcher } from "mode-watcher";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
  import { Button } from "$lib/components/ui/button/index.js";

  // import "../app.css";
  import Ferdous from "./components/Ferdous.svelte";
  import clb from "./assets/images/clb.png";

  let position = "top";

  let timeseries = "WEEKLY";
  let graphDataLength = 12;

  const lengthMap = new Map();
  lengthMap.set(12, "3 Months");
  lengthMap.set(26, "6 Months");
  lengthMap.set(52, "1 Year");

  let trackedMockPolitician = "Nancy Pelosi";

  let graphData: { time: string; value: number; symbol: string }[] = [];
  let graphSymbols: { symbol: string; dif: string }[] = [];

  let gainer = "";
  let loser = "";
  let gainerPercentage = 0;
  let loserPercentage = 0;

  // Define the theme object here
  const graphTheme = {
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
    {
      symbol: "AAPL",
      tradeDate: "2024-04-18",
      type: "SELL",
      amount: 1000,
      politicianName: "Nancy Pelosi",
    },
    {
      symbol: "PANW",
      tradeDate: "2024-04-13",
      type: "BUY",
      amount: 5000,
      politicianName: "Kevin Hern",
    },
    {
      symbol: "NVDA",
      tradeDate: "2024-04-09",
      type: "BUY",
      amount: 25000,
      politicianName: "Max Miller",
    },
    {
      symbol: "MSFT",
      tradeDate: "2024-03-17",
      type: "SELL",
      amount: 100,
      politicianName: "Nancy Pelosi",
    },
    {
      symbol: "QQQ",
      tradeDate: "2024-03-13",
      type: "BUY",
      amount: 50000,
      politicianName: "Kevin Hern",
    },
    {
      symbol: "TSLA",
      tradeDate: "2024-03-09",
      type: "SELL",
      amount: 25000,
      politicianName: "Max Miller",
    },
    {
      symbol: "MSFT",
      tradeDate: "2024-02-17",
      type: "BUY",
      amount: 10000,
      politicianName: "Nancy Pelosi",
    },
    {
      symbol: "TSLA",
      tradeDate: "2024-02-12",
      type: "SELL",
      amount: 50000,
      politicianName: "Kevin Hern",
    },
    {
      symbol: "NVDA",
      tradeDate: "2024-02-01",
      type: "SELL",
      amount: 25000,
      politicianName: "Max Miller",
    },
    {
      symbol: "MSFT",
      tradeDate: "2024-02-17",
      type: "BUY",
      amount: 10000,
      politicianName: "Nancy Pelosi",
    },
  ];

  function getPercentChange(first: number, last: number): string {
    let dif = last - first;
    let avg = (first + last) / 2;
    return ((dif / avg) * 100).toFixed(2);
  }

  onMount(() => {
    const scrollers: any = document.querySelectorAll(".slider");

    // If a user hasn't opted in for recuded motion, then we add the animation
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      addAnimation();
    }

    function addAnimation() {
      scrollers.forEach(
        (scroller: {
          setAttribute: (arg0: string, arg1: boolean) => void;
          querySelector: (arg0: string) => any;
        }) => {
          // add data-animated="true" to every `.scroller` on the page.
          // Had to hardcode onto element.
          // scroller.setAttribute("data-animated", true);

          // Make an array from the elements within `.scroller-inner`
          const scrollerInner = scroller.querySelector(".slider__inner");
          const scrollerContent = Array.from(scrollerInner.children);

          // For each item in the array, clone it
          // add aria-hidden to it
          // add it into the `.scroller-inner`
          scrollerContent.forEach((item: any) => {
            const duplicatedItem = item.cloneNode(true);
            duplicatedItem.setAttribute("aria-hidden", true);
            scrollerInner.appendChild(duplicatedItem);
          });
        },
      );
    }
  });

  async function fetchData() {
    graphData = [];
    graphSymbols = [];

    for (let i = 0; i < trackedSymbols.length; i++) {
      await fetch(
        `https://65f7764db2fafbd9238d.appwrite.global/stocks?symbol=${trackedSymbols[i]}&timeseries=WEEKLY&length=${graphDataLength}&offset=1`,
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

    for (let i = 0; i < trackedSymbols.length; i++) {
      let temp = graphData.filter((item) => item.symbol == trackedSymbols[i]);
      let cur = {
        symbol: trackedSymbols[i],
        dif: getPercentChange(temp[0].value, temp[temp.length - 1].value),
      };
      graphSymbols = [...graphSymbols, cur];
    }
    gainerPercentage = graphSymbols.reduce((acc, value) => {
      return (acc = acc > parseFloat(value.dif) ? acc : parseFloat(value.dif));
    }, 0);
    loserPercentage = graphSymbols.reduce((acc, value) => {
      return (acc = acc < parseFloat(value.dif) ? acc : parseFloat(value.dif));
    }, 0);

    let gainerOBJ = graphSymbols.find(
      (item) => parseFloat(item.dif) === gainerPercentage,
    );
    if (gainerOBJ) {
      gainer = gainerOBJ.symbol;
    }

    let loserOBJ = graphSymbols.find(
      (item) => parseFloat(item.dif) === loserPercentage,
    );
    if (loserOBJ) {
      loser = loserOBJ.symbol;
    }
  }

  let isDropdownOpen = false;
  let isDropdownOpenPolitician = false;

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

  const handleDropdownClickPolitician = () => {
    isDropdownOpenPolitician = !isDropdownOpenPolitician;
  };
  //figure out type of these 2 bitches
  const handleDropdownFocusLossPolitician = ({
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
    isDropdownOpenPolitician = false;
  };
</script>

<ModeWatcher />

<main class="main h-dvh w-screen bg-neutral-900 overflow-y-scroll dark">
  {#key graphDataLength}
    {#await fetchData()}
      <div class="animate-pulse flex flex-col items-center text-white mt-20">
        <img alt="CLB Logo" src={clb} />
        <p>Loading...</p>
      </div>
    {:then chart}
      <div class="flex-col text-center mb-2">
        <h1
          class="mb-4 text-4xl font-extrabold leading-none tracking-tight text-white md:text-5xl lg:text-6xl dark:text-white"
        >
          Welcome Back for your Weekly Update!
        </h1>

        <div class="flex justify-center">
          <div class="slider" data-animated="true">
            <ul class="tag-list slider__inner">
              {#each mockPoliticianData as item}
                <li class="text-white font-bold">
                  {#if item.type == "BUY"}
                    <Card.Root class="w-[180px]">
                      <Card.Header>
                        <Card.Title class="text-green-700"
                          >{item.type}
                        </Card.Title>
                        <Card.Description>{item.symbol}</Card.Description>
                      </Card.Header>
                      <Card.Content>
                        <p>$ {item.amount}</p>
                        <p>{item.politicianName}</p>
                        <p>{item.tradeDate}</p>
                      </Card.Content>
                    </Card.Root>
                  {:else}
                    <Card.Root class="w-[180px]">
                      <Card.Header>
                        <Card.Title class="text-red-700">{item.type}</Card.Title
                        >
                        <Card.Description>{item.symbol}</Card.Description>
                      </Card.Header>
                      <Card.Content>
                        <p>$ {item.amount}</p>
                        <p>{item.politicianName}</p>
                        <p>{item.tradeDate}</p>
                      </Card.Content>
                    </Card.Root>
                  {/if}
                </li>
              {/each}
            </ul>
          </div>
        </div>

        <div class="flex justify-evenly mb-5">
          <div
            class="max-w-md rounded-xl overflow-hidden shadow-lg bg-green-900"
          >
            <div class="px-2 py-4">
              <div class="font-extrabold text-xl mb-2">
                The {lengthMap.get(graphDataLength)} Gainer 💪
              </div>
              <p class="text-black text-base font-bold">
                The {lengthMap.get(graphDataLength)} gainer is {gainer} with a growth
                of {gainerPercentage}%
              </p>
              <p class="text-black text-base">
                “Happiness is not in the mere possession of money; it lies in
                the joy of achievement, in the thrill of creative effort.” <br
                />– Franklin D. Roosevelt
              </p>
            </div>
          </div>

          <div class="max-w-md rounded-xl overflow-hidden shadow-lg bg-red-900">
            <div class="px-6 py-4">
              <div class="font-extrabold text-xl mb-2">
                The {lengthMap.get(graphDataLength)} Loser 👋🏼
              </div>
              <p class="text-black text-base font-bold">
                The {lengthMap.get(graphDataLength)} loser is TESLA with a loss of
                {loserPercentage}%
              </p>
              <p class="text-black text-base">
                “Wealth consists not in having great possessions, but in having
                few wants.” <br />– Epictetus.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-evenly border-b-2 pb-2">
        <h2 class="text-2xl">Stocks of Interest</h2>

          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild let:builder>
              <Button variant="outline" builders={[builder]}
                >{lengthMap.get(graphDataLength)} 👈</Button
              >
            </DropdownMenu.Trigger>
            <DropdownMenu.Content class="w-56 text-center">
              <DropdownMenu.Label class="">Time Series</DropdownMenu.Label>
              <DropdownMenu.Separator />
              <DropdownMenu.RadioGroup bind:value={position}>
                <DropdownMenu.RadioItem
                  value="top"
                  on:click={() => (graphDataLength = 12)}
                  >3 Months</DropdownMenu.RadioItem
                >
                <DropdownMenu.RadioItem
                  value="bottom"
                  on:click={() => (graphDataLength = 26)}
                  >6 Months</DropdownMenu.RadioItem
                >
                <DropdownMenu.RadioItem
                  value="right"
                  on:click={() => (graphDataLength = 52)}
                  >1 Year</DropdownMenu.RadioItem
                >
              </DropdownMenu.RadioGroup>
            </DropdownMenu.Content>
          </DropdownMenu.Root>
      </div>

      <div>
        <!-- {#key graphDataLength}
      {#await fetchData()}
        <div class="flex flex-col items-center text-white">
          <p>Loading...</p>
        </div>
      {:then chart} -->
        <div
          class="sm:grid sm:grid-rows-2 sm:grid-flow-col sm:gap-x-28 sm:gap-y-10 justify-center mb-2 mt-2"
        >
          {#each graphSymbols as graph}
            <div class="bg-slate-900 p-2 rounded-lg w-min">
              <div class="flex flex-row justify-between">
                <p class="text-white font-bold text-xl">
                  {graph.symbol}
                </p>
                {#if parseInt(graph.dif) > 0}
                  <p class="text-emerald-700 font-bold text-xl">
                    🤑{graph.dif}%
                  </p>
                {:else}
                  <p class="text-red-700 font-bold text-xl">😮{graph.dif}%</p>
                {/if}
              </div>
              <Ferdous
                width={520}
                height={420}
                theme={graphTheme}
                graphData={graphData.filter(
                  (item) => item.symbol == graph.symbol,
                )}
              />
            </div>
          {/each}
        </div>
        <!-- {/await}
    {/key} -->
      </div>
    {/await}
  {/key}
</main>

<style>
  .main {
    font-family: "Outfit", "Helvetica Neue", Helvetica, Arial, sans-serif;
  }

  .slider {
    max-width: 900px;
  }

  .slider__inner {
    padding-block: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .slider[data-animated="true"] {
    overflow: hidden;
    -webkit-mask: linear-gradient(
      90deg,
      transparent,
      white 20%,
      white 80%,
      transparent
    );
    mask: linear-gradient(
      90deg,
      transparent,
      white 20%,
      white 80%,
      transparent
    );
  }

  .slider[data-animated="true"] .slider__inner {
    width: max-content;
    flex-wrap: nowrap;
    animation: scroll var(--_animation-duration, 40s)
      var(--_animation-direction, forwards) linear infinite;
  }

  .slider[data-animated="true"] .slider__inner:hover {
    animation-play-state: paused;
  }

  @font-face {
    src: url(https://fonts.gstatic.com/s/outfit/v4/QGYyz_MVcBeNP4NjuGObqx1XmO1I4deyC4G-EiAou6Y.ttf);
    font-family: "Outfit";
    font-style: normal;
    font-weight: 700;
  }

  @font-face {
    src: url(https://fonts.gstatic.com/s/outfit/v4/QGYyz_MVcBeNP4NjuGObqx1XmO1I4TC1C4G-EiAou6Y.ttf);
    font-family: "Outfit";
    font-style: normal;
    font-weight: 400;
  }

  /* Options below to make infinte scroll dynamic speed and direction*/
  /* .slider[data-direction="right"] {
  --_animation-direction: reverse;
}

.slider[data-direction="left"] {
  --_animation-direction: forwards;
}

.slider[data-speed="fast"] {
  --_animation-duration: 20s;
}

.slider[data-speed="slow"] {
  --_animation-duration: 60s;
} */

  @keyframes scroll {
    to {
      transform: translate(calc(-50% - 0.5rem));
    }
  }

  :root {
    --clr-neutral-100: hsl(0, 0%, 100%);
    --clr-primary-100: hsl(205, 15%, 58%);
    --clr-primary-400: hsl(215, 25%, 27%);
    --clr-primary-800: hsl(217, 33%, 17%);
    --clr-primary-900: hsl(218, 33%, 9%);
  }

  .tag-list {
    margin: 0;
    padding-inline: 0;
    list-style: none;
  }

  .tag-list li {
    padding: 1rem;
    border-radius: 0.5rem;
  }
</style>
