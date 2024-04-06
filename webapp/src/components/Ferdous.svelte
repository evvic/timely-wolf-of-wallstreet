<script lang="ts">
  import { Chart, LineSeries } from 'svelte-lightweight-charts';

  
  export let graphData: { time: string, value: number }[] = [];
  export let width: number = 800;
  export let height: number = 600;
  export let theme: any;

  
</script>

<style>
  /* Style for the chart container */
  .chart-container {
    border-radius: 10px; /* Adjust the value to control the roundness of the corners */
    overflow: hidden; /* Ensure that content inside the container is clipped to the rounded shape */
  
  }
</style>



<div class="chart-container">
  <Chart {width} {height} {...theme.chart}  >
    <LineSeries data={graphData} reactive={true} color={'silver'}/>
  </Chart>
</div>
