<script lang="ts">
  import { Chart, LineSeries } from 'svelte-lightweight-charts';
  export let graphData: { time: string, value: number }[] = [];
  export let width: number = 800;
  export let height: number = 600;
</script>

<div>
  <Chart {width} {height}  >
    <LineSeries data={graphData} reactive={true}/>
  </Chart>
</div>
