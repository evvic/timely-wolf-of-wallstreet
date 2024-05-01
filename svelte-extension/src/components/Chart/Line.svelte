<script>
// @ts-nocheck

    import * as d3 from "d3";
  
    export let type = "line";
    export let data = [];
    export let xAccessor = () => {};
    export let yAccessor = () => {};
    export let y0Accessor = 0;
    export let interpolation = d3.curveMonotoneX;
    export let style = ""
  
    $: lineGenerator = d3[type]()
      .x(xAccessor)
      .y(yAccessor)
      .curve(interpolation);
  
    $: {
      if (type == "area") {
        lineGenerator
          .y0(y0Accessor)
          .y1(yAccessor);
      }
    }
  
    $: line = lineGenerator(data);
  </script>
  
  <path class={`Line Line--type-${type}`} d={line} {style} />
  
  <style>
    .Line {
      transition: all 0.3s ease-out;
    }
  
    .Line--type-line {
      fill: none;
      /* stroke: #9980fa; */
      stroke: white;
      stroke-width: 2px;
      stroke-linecap: round;
    }
  
    .Line--type-area {
      fill: rgba(202, 193, 237, 0.102);
      stroke-width: 0;
    }
  </style>