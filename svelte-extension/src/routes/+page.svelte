<script lang="js">
// @ts-nocheck
    import { Input } from "$lib/components/ui/input/index.js";
    import { Badge } from "$lib/components/ui/badge/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
    import Select from '../components/select.svelte'
    import LineChart from '../components/LineChart.svelte';
    import { onMount, onDestroy } from 'svelte';
    import * as d3 from "d3";
    import { isValidStockSymbol } from "../lib/utils"


    let counter = 0;
    let symbol = ""
    let num_weeks = undefined
    let data = []

    let test = "what"

    
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
            symbol = sym ? sym : symbol;
            num_weeks = nwks ? nwks : num_weeks;
        });
        
    
    })

    // reactive statement to trigger updateData when symbol or num_weeks changes
    $: {
        data = updateData(symbol, num_weeks);
    }
    
    

    function updateData(symbol, num_weeks) {
        // Your function logic using symbol and num_weeks
        //console.log("Symbol:", symbol, "Num Weeks:", num_weeks);

        // @ts-ignore
        //chrome.storage.local.set({ counter: counter });

        // @ts-ignore
        //chrome.storage.local.set({ symbol: symbol });

        counter++;

        if (isValidStockSymbol(symbol.toUpperCase())) {
            test = "STOCK SYMBOL IS VALID"
        } else {
            test = "STOCK SYMBOL IS INVALID"
        }

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

        return fakedata
    }


    function updateChart() {
        // Increment the counter
        counter++;

        // Store the counter value in storage
        // @ts-ignore
        chrome.storage.local.set({ counter: counter });
        // @ts-ignore
        chrome.storage.local.set({ symbol: symbol });
        // @ts-ignore
        //chrome.storage.local.set({ num_weeks: num_weeks });

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
            <Input type="symbol" placeholder="SYMBOL" class="w-20 uppercase font-weight-bold" bind:value={symbol} on:change={updateChart} />
            <!-- Dropdown -->
            <Select bind:window={num_weeks} />
        </div>
        <!-- <button id="update-chart-btn" on:click={updateChart}>Update Chart {counter}  {symbol || '(enter symbol)'}</button> -->
        <!-- <div>
            <canvas id="myChart"></canvas>
        </div> -->
        <!-- {#each data as number}
            <p>{number}</p>
        {/each} -->
        <p>num_weeks: {num_weeks} {test}</p>    
        <div class="flex items-center py-4">
            <h2 class="scroll-m-20 text-2xl font-semibold tracking-tight pr-2">
                $450.69
            </h2>
            <Badge class="font-weight-bold">+30%</Badge>
        </div>
        <Card.Root class="max-w-lg max-h-lg m-0">
            <Card.Content class="p-1">
                <LineChart 
                    data={data} 
                    xAccessor={dateAccessor} 
                    yAccessor={priceAccessor} 
                    label={symbol}
                    width={325}
                    height={325}
                />
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