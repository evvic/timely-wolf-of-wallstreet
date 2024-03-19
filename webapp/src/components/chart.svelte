<script lang="ts" context='module'>
    import { Chart, LineSeries } from "svelte-lightweight-charts";
  
    export interface ChartProps {
      width?: number;
      height?: number;
      data: { time: string; value: number }[];
    }



    
  </script>
  
  <Chart bind:width bind:height bind:data>
    <LineSeries bind:data />
  </Chart>


  <style>
    /* Add any styles for the chart here (optional) */
  </style>