<script lang="js">
// @ts-nocheck
    import { Input } from "$lib/components/ui/input/index.js";
    import Select from '../components/select.svelte'
    import LineChart from '../components/LineChart.svelte';
    import { onMount, onDestroy } from 'svelte';
    import * as d3 from "d3";


    let counter = 0;
    let symbol = ""
    let num_weeks = undefined

    

    // test data
    const data = [
        { date: new Date(2023, 11, 1), price: 100 }, // December 1st, 2023 price: 100
        { date: new Date(2023, 11, 15), price: 120 }, // December 15th, 2023 price: 120
        { date: new Date(2024, 0, 1), price: 115 }, // January 1st, 2024 price: 115
        // Add more data points...
    ];
    const parseDate = d3.timeParse("%m/%d/%Y");
    //const dateAccessor = d => parseDate(d.date);
    const dateAccessor = d => d.date;
    const priceAccessor = d => d.price;

    let unloadListener;

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
    

    // onDestroy(() => {
    //     chrome.runtime.sendMessage({ type: 'save-data', data: { counter, symbol, num_weeks } });
    // });


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


    // Attach the event listener
</script>


<svelte:head>
    <link rel="stylesheet" href="popup.css" />
</svelte:head>

<div>
    <nav>
        <img class="icon" src="icons/clb.png" alt="Icon">
        <div>
            <h2 class="main-text">Janka Finance</h2>
            <span class="sub-text">Jankalites LLC</span>
        </div>
    </nav>
    <div class="chart-container">
        <div class="container">
            <!-- Search bar -->
            <Input type="symbol" placeholder="Search..." class="max-w-xs" bind:value={symbol} on:change={updateChart}/>
            <!-- Dropdown -->   
            <Select bind:window={num_weeks}  />
        </div>
        <button id="update-chart-btn" on:click={updateChart}>Update Chart {counter}  {symbol || '(enter symbol)'}</button>
        <!-- <div>
            <canvas id="myChart"></canvas>
        </div> -->
        <p>num_weeks: {num_weeks}</p>
        <LineChart 
            data={data} 
            xAccessor={dateAccessor} 
            yAccessor={priceAccessor} 
            label={symbol}
        />
    </div>
</div>