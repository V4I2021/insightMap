<template>
  <g>
    <rect :width="width" :height="height" fill="white" stroke="white" stroke-width="1"></rect>

    <g>
      <g v-for="(obj, i) in data.list" :key="i" :transform="'translate(' + [0, yScale(i)] + ')' ">
        <rect :width="xScale(obj[1])" fill="steelblue" :height="unitHeight*0.9"></rect>
      </g>
    </g>
  </g>
</template>

<script>
import * as d3 from "d3";
export default {
  name: "BarChart",
  props:['data', 'width', 'height'],
  data(){
    return {
      xScale: d3.scaleLinear(),
      yScale: d3.scaleLinear(),
      unitWidth: 0,
      unitHeight: 0
    }
  },
  mounted(){
    this.yScale.domain([0, this.data.list.length]).range([16, this.height])
    this.xScale.domain(d3.extent(this.data.list, d=>d[1])).range([1, this.width-5])
    this.unitWidth = this.width / this.data.list.length
    this.unitHeight = this.height / this.data.list.length
  }
}
</script>

<style scoped>

</style>