<script>
// @ts-nocheck

    import * as d3 from "d3";
  
    import Chart from "./Chart/Chart.svelte";
    import Line from "./Chart/Line.svelte";
    // import Axis from "./Chart/Axis-naive.svelte";
    import Axis from "./Chart/Axis.svelte";
    import Gradient from "./Chart/Gradient.svelte";
    import { getUniqueId, formatPrice } from "./Chart/utils";
    import { onMount } from 'svelte';
  
    const formatDate = d3.timeFormat("%-b %Y");
    //const _formatPrice = formatPrice;
    const gradientColors = ["white", "black"];
    const gradientId = getUniqueId("Timeline-gradient");
  
    export let data = [];
    export let xAccessor = d => d.x;
    export let yAccessor = d => d.y;
    // export let label;
    export let width = undefined
    export let height = undefined


    const margins = {
        marginTop: 15,
        marginRight: 0,
        marginBottom: 0,
        marginLeft: 0
    };
    $: dms = {
        width,
        height,
        ...margins,
        boundedHeight: Math.max(
            height - margins.marginTop - margins.marginBottom,
            0
        ),
        boundedWidth: Math.max(
            width - margins.marginLeft - margins.marginRight,
            0
        )
    };
  
    $: xScale = d3.scaleTime()
        .domain(d3.extent(data, xAccessor))
        .range([0, dms.boundedWidth]);
        //.style("color", "white");
  
    $: yScale = d3.scaleLinear()
        .domain(d3.extent(data, yAccessor))
        .range([dms.boundedHeight, 0])
        .nice();

    $: xAccessorScaled = d => xScale(xAccessor(d));
    $: yAccessorScaled = d => yScale(yAccessor(d));
    $: y0AccessorScaled = yScale(yScale.domain()[0]);
</script>
  
<div class="Timeline placeholder max-w-lg max-h-lg " bind:clientWidth={width} bind:clientHeight={height}>
    <Chart dimensions={dms}>
        <defs>
            <Gradient
                id={gradientId}
                colors={gradientColors}
                x2="0"
                y2="100%"
            />
        </defs>
        <Axis
            dimension="x"
            scale={xScale}
            formatTick={formatDate}
        />
        <Axis
            dimension="y"
            scale={yScale}
            formatTick={formatPrice}
        />
        <Line
            type="area"
            data={data}
            xAccessor={xAccessorScaled}
            yAccessor={yAccessorScaled}
            y0Accessor={y0AccessorScaled}
            
        />
        <Line
            data={data}
            xAccessor={xAccessorScaled}
            yAccessor={yAccessorScaled}
        />
    </Chart>
</div>
  
<style>
    .Timeline {
        /* height: 250px; */
        min-width: 300px;
        /*width: calc(100% + 1em); */
        /* max-width: 400px; */
        /* margin-bottom: 1em; */
    }
</style>
  