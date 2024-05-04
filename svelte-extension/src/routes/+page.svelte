<script lang="js">
// @ts-nocheck
    import { Input } from "$lib/components/ui/input/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { Jellyfish } from 'svelte-loading-spinners';
    import * as Card from "$lib/components/ui/card/index.js";
    import Select from '../components/select.svelte'
    import ComboBox from '../components/combobox.svelte'
    import LineChart from '../components/LineChart.svelte';
    import { onMount, onDestroy } from 'svelte';
    import * as d3 from "d3";
    import { isValidStockSymbol, queryStockData } from "../lib/utils"
    

    let counter = 0;
    let symbol = "";
    let num_weeks = undefined;
    let data = [];
    let current_price = undefined;
    let percent_change = undefined;
    let loading = true;

    let test = "what"

    const borderVariants = {
        "normal": "",
        "error": "border-red-500"
    }

    const parseDate = d3.timeParse("%m/%d/%Y");
    //const dateAccessor = d => parseDate(d.date);
    const dateAccessor = d => d.date;
    const priceAccessor = d => d.price;

    onMount(() => {
        chrome.storage.local.get(["counter", "symbol", "num_weeks"], (data) => {
            const cnt = data["counter"];
            const sym = data["symbol"];
            const nwks = data["num_weeks"];

            counter = cnt ? cnt : counter;
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
        // Your function logic using symbol and num_weeks
        //console.log("Symbol:", symbol, "Num Weeks:", num_weeks);

        // @ts-ignore
        //chrome.storage.local.set({ counter: counter });

        // @ts-ignore
        //chrome.storage.local.set({ symbol: symbol });

        // save data to lcaol vars
        let temp_current_price = current_price
        let temp_percent_change = percent_change
        let temp_data = data

        counter++;
        loading = true;

        if (!num_weeks || num_weeks <= 0) {
            data = [];
            current_price = undefined;
            percent_change = undefined;
            return;
        }

        if (isValidStockSymbol(symbol.toUpperCase())) {
            test = "STOCK SYMBOL IS VALID"
        } else {
            test = "STOCK SYMBOL IS INVALID";
            data = [];
            current_price = undefined;
            percent_change = undefined;
            return;
        }

        current_price = undefined;
        percent_change = undefined;

        const tempStockData = await queryStockData(symbol, num_weeks)

        if (tempStockData.length > 0) {
            //console.log("Successfully retrieved stock data:", stockData);
            test = "Successfully retrieved stock data:"
            //return tempStockData
        } else {
            console.log("No data found for the symbol.");
            test = "No data found for the symbol."
            return;
        }

        // FORMAT DATA

        // API call would get the data here
        const fakedata = [
            { date: new Date(2023, 9, 15), price: 40 },
            { date: new Date(2023, 10, 1), price: 100 },
            { date: new Date(2023, 10, 15), price: 60 },
            { date: new Date(2023, 11, 1), price: 100 },
            { date: new Date(2023, 11, 15), price: 120 },
            { date: new Date(2024, 0, 1), price: 115 },
            // Add more data points...
        ];

        current_price = tempStockData.slice(-1)[0]["price"];
        percent_change = "-40"

        data = tempStockData.map(obj => ({
            date: new Date(obj.date),
            price: obj.price,
        }));

        saveToChromeStorage()

        loading = false;
    }


    function saveToChromeStorage() {
        // Increment the counter
        counter++;

        // Store the counter value in storage
        // @ts-ignore
        chrome.storage.local.set({ counter: counter });
        // @ts-ignore
        chrome.storage.local.set({ symbol: symbol });
        // @ts-ignore
        //chrome.storage.local.set({ num_weeks: num_weeks });

        // API call would get the data here
        const fakedata = [
            { date: new Date(2023, 9, 15), price: 40 },
            { date: new Date(2023, 10, 1), price: 100 },
            { date: new Date(2023, 10, 15), price: 60 },
            { date: new Date(2023, 11, 1), price: 100 },
            { date: new Date(2023, 11, 15), price: 120 },
            { date: new Date(2024, 0, 1), price: 115 },
            // Add more data points...
        ];

        //data = fakedata
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
            <span class="sub-text">Jankalites LLC</span>
        </div>
    </nav>
    <div class="chart-container m-4">
        <div class="container px-0">
            <!-- Search bar -->
            <ComboBox bind:symbol={symbol} on:change={saveToChromeStorage} />
            <!-- <Input type="symbol" placeholder="SYMBOL" class={"w-20 uppercase font-weight-bold border-red-500"} bind:value={symbol} on:change={saveToChromeStorage} /> -->
            <!-- <Input type="symbol" placeholder="SYMBOL" class={"w-20 uppercase font-weight-bold" + symbol_error_status === true ? "border-red-500" : ""} bind:value={symbol} on:change={saveToChromeStorage} /> -->
            <!-- Dropdown -->
            <Select bind:window={num_weeks} />
        </div>
        <!-- <button id="update-chart-btn" on:click={saveToChromeStorage}>Update Chart {counter}  {symbol || '(enter symbol)'}</button> -->
        <!-- <div>
            <canvas id="myChart"></canvas>
        </div> -->
        <!-- {#each data as number}
            <p>{number}</p>
        {/each} -->
        <!-- <p>num_weeks: {num_weeks} {test}</p>     -->
        <p>{test}</p>
        <div class="flex items-center py-4">
            <h2 class="scroll-m-20 text-2xl font-semibold tracking-tight pr-2">
                ${current_price? current_price : "-"}
            </h2>
            <Badge class="font-weight-bold">{percent_change? percent_change : "- "}%</Badge>
        </div>
        <Card.Root class="max-w-lg max-h-lg m-0 overflow-hidden">
            <Card.Content class="p-0">
                {#if loading}
                    <div class="w-325 h-325 flex justify-center items-center">
                        <Jellyfish size="60" color="#FFFFFF" unit="px" />
                    </div>
                {:else}
                    <LineChart 
                        data={data} 
                        xAccessor={dateAccessor} 
                        yAccessor={priceAccessor} 
                        label={symbol}
                        width={325}
                        height={325}
                    />
                {/if}
            </Card.Content>
        </Card.Root>
        
    </div>
</div>

<style>
    /* .divbody {
        max-width: 400px;
        height: 400px;
    } */
</style>