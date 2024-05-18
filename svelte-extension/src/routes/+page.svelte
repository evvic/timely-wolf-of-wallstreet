<script lang="js">
// @ts-nocheck
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { Jellyfish } from 'svelte-loading-spinners';
    import * as Card from "$lib/components/ui/card/index.js";
    import Select from '../components/select.svelte'
    import ComboBox from '../components/combobox.svelte'
    import LineChart from '../components/LineChart.svelte';
    import { onMount } from 'svelte';
    import { isValidStockSymbol, queryStockData, calculatePercentChange } from "../lib/utils"
    
    //let counter = 0;
    let symbol = "";
    let num_weeks = undefined;
    let data = [];
    let current_price = undefined;
    let percent_change = undefined;
    let loading = false;
    let error_state = false;

    const dateAccessor = d => d.date;
    const priceAccessor = d => d.price;

    onMount(() => {
        chrome.storage.local.get(["counter", "symbol", "num_weeks"], (data) => {
            //const cnt = data["counter"];
            const sym = data["symbol"];
            const nwks = data["num_weeks"];

            //counter = cnt ? cnt : counter;
            symbol = sym ? sym.toUpperCase() : symbol;
            num_weeks = nwks ? nwks : num_weeks;
        });
    })

    // reactive statement to trigger updateData when symbol or num_weeks changes
    $: {
        getData(symbol, num_weeks);
    }

    function getData(sym, nweeks) {
        updateData(sym, nweeks);
    }

    async function updateData(symbol, num_weeks) {

        // save data to local vars
        const temp_current_price = current_price
        const temp_percent_change = percent_change
        const temp_data = data

        //counter++;
        loading = true;
        error_state = false;

        if (!num_weeks || num_weeks <= 0) {
            data = [];
            current_price = undefined;
            percent_change = undefined;
            error_state = true;
            return;
        }

        if (isValidStockSymbol(symbol.toUpperCase())) {
            console.log("STOCK SYMBOL IS VALID")
        } else {
            console.log("STOCK SYMBOL IS INVALID");
            data = [];
            current_price = undefined;
            percent_change = undefined;
            error_state = true;
            return;
        }

        current_price = undefined;
        percent_change = undefined;

        const tempStockData = await queryStockData(symbol, num_weeks)

        if (tempStockData.length > 0) {
            //console.log("Successfully retrieved stock data:", stockData);
            console.log("Successfully retrieved stock data")
            //return tempStockData
        } else {
            console.log("No data found for the symbol.");
            error_state = true;
            return;
        }

        current_price = parseFloat(tempStockData.slice(-1)[0]["price"]).toFixed(2);
        const past_price = tempStockData[0]["price"];
        percent_change = calculatePercentChange(current_price, past_price)

        data = tempStockData.map(obj => ({
            date: new Date(obj.date),
            price: obj.price,
        }));

        saveToChromeStorage()

        loading = false;
    }

    function saveToChromeStorage() {
        // Increment the counter
        //counter++;

        //chrome.storage.local.set({ counter: counter });
        chrome.storage.local.set({ symbol: symbol });
    }

</script>

<svelte:head>
    <link rel="stylesheet" href="popup.css" />
</svelte:head>

<div class="divbody">
    <nav>
        <img class="icon" src="icons/clb.png" alt="Icon">
        <div>
            <h2 class="main-text">Janka Finance</h2>
            <a href="https://dailychart.freewebhostmost.com/" target="_blank" rel="noopener noreferrer" class="sub-text">© 2024 Jankalites</a>
        </div>
    </nav>
    <div class="chart-container m-4">
        <div class="container px-0">
            <!-- Symbol CombBox -->
            <ComboBox bind:symbol={symbol} on:change={saveToChromeStorage} />
            <!-- Time Window Dropdown -->
            <Select bind:window={num_weeks} />
        </div>
        <div class="flex items-center py-4">
            <h2 class="scroll-m-20 text-2xl font-semibold tracking-tight pr-2">
                ${current_price? current_price : "-"}
            </h2>
            <Badge class="font-weight-bold">{percent_change? percent_change : "- "}%</Badge>
        </div>
        <Card.Root class="max-w-lg max-h-lg m-0 overflow-hidden relative">
            <Card.Content class="p-0">
                <LineChart 
                    data={data} 
                    xAccessor={dateAccessor} 
                    yAccessor={priceAccessor} 
                    label={symbol}
                    width={325}
                    height={325}
                />
                {#if loading}
                <div class="absolute inset-0 flex items-center justify-center bg-background bg-opacity-50">
                    <div class="flex justify-center items-center">
                      <Jellyfish size="60" color="#FFFFFF" unit="px" />
                    </div>
                </div>
                {:else if error_state}
                <div class="absolute inset-0 flex items-center justify-center bg-background bg-opacity-50">
                    <div class="flex flex-col items-center justify-center h-screen">
                        <p class="leading-7 [&:not(:first-child)]:mt-6">Error fetching stock data for the last {num_weeks} weeks of {symbol}.</p>
                    </div>
                </div>
                {:else if (num_weeks === undefined || symbol === "")}
                <div class="absolute inset-0 flex items-center justify-center bg-background bg-opacity-50">
                    <div class="flex flex-col items-center justify-center h-screen">
                        <div class="text-lg font-semibold">Welcome to Janka Finance.</div>
                        <p class="leading-7 [&:not(:first-child)]:mt-6">Select a symbol and time window to get started!</p>
                    </div>
                </div>
                {/if}
            </Card.Content>
        </Card.Root>
    </div>
</div>
