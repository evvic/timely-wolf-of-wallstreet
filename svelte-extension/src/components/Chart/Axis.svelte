<script>
// @ts-nocheck

    import {  getContext } from "svelte";
    import * as d3 from "d3";
  
    export let dimension = "x";
    export let scale = null;
    export let label;
    export let formatTick = d3.format(",");
  
    const { dimensions: dimensionsStore } = getContext("Chart");
    $: dimensions = $dimensionsStore;
  
    $: numberOfTicks =
      dimension == "x"
        ? dimensions.boundedWidth < 600
          ? dimensions.boundedWidth / 100
          : dimensions.boundedWidth / 250
        : dimensions.boundedHeight / 70;
  
    $: ticks = scale.ticks(numberOfTicks);

  </script>
  
<g
    class="text-white Axis Axis--dimension-{dimension}"
    transform={`translate(0, ${dimension == "x" ? dimensions.boundedHeight : 0})`}>
    <line
      class="Axis__line"
      x2={dimension == "x" ? dimensions.boundedWidth : 0}
      y2={dimension == "y" ? dimensions.boundedHeight : 0}
    />
  
    {#each ticks as tick, i}
        <text class="Axis__tick text-white" transform={`translate(${(
            dimension == "x"
            ? [scale(tick), -5]
            : [5, scale(tick) - 3]
            ).join(", ")})`}>   
            {formatTick(tick)}
        </text>
    {/each}
  
    {#if label}
      <text
        class="Axis__label"
        style="transform: translate({(
          dimension == "x"
            ? [dimensions.boundedWidth / 2, 60]
            : [-56, dimensions.boundedHeight / 2]
        ).map(d => d + "px").join(", ")}) {
          dimension == "y" ? "rotate(-90deg)" : ""
        }
        t">
        {label}
      </text>
    {/if}
  </g>
  
  <style>
    .Axis__line {
      stroke: #bdc3c7;
      color: white;
    }
  
    .Axis__label {
      text-anchor: middle;
      font-size: 0.8em;
      letter-spacing: 0.01em;
      color: white;
    }
  
    .Axis__tick {
      font-size: 0.9em;
      font-weight: bold;
      color: white;
      fill: white;
      transition: all 0.3s ease-out;
    }
  
    /* .Axis--dimension-x .Axis__tick {
      text-anchor: middle;
      color: blue;
    }
  
    .Axis--dimension-y .Axis__tick {
      dominant-baseline: middle;
      text-anchor: end;
      color: orange;
    } */
  </style>
  