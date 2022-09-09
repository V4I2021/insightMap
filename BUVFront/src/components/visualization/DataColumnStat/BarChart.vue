<template>
  <g>
    <rect :width="width" :height="height" fill="none" stroke="grey" stroke-width="1"></rect>
    <!--        <rect :x="" :y="" ></rect>-->
    <g>
      <g v-for="(obj, i) in data.list" :key="i" :transform="'translate(' + [xScale(i), 0] + ')' ">
        <rect
             :y="height - yScale(obj[1])" :width="unitWidth*0.9" :height="yScale(obj[1])" fill="steelblue"></rect>
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
    }
  },
  mounted(){
    console.log('data', this.data);
    this.xScale.domain([0, this.data.list.length]).range([0, this.width])
    this.yScale.domain(d3.extent(this.data.list, d=>d[1])).range([3, this.height])
    this.unitWidth = this.width / this.data.list.length
  }
}
</script>

<style scoped>

</style>