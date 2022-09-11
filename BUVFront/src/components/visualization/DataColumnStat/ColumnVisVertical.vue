<template>
  <g>
    <rect :width="width" :height="height" fill="none" stroke="white" stroke-width="1"></rect>
    <g :transform="'translate(' + [0, 0] + ')'">
      <BarChartVertical :data="data" :width="width" :height="height"></BarChartVertical>
    </g>
    <text class="name" :y="textOffsetY" :x='textOffsetX' style="font-size: 10px">{{data.column}}</text>
  </g>
</template>

<script>
import BarChartVertical from "@/components/visualization/DataColumnStat/BarChartVertical";
import * as d3 from 'd3'
export default {
  name: "ColumnVis",
  components: {BarChartVertical},
  props:['data', 'width', 'height'],
  data(){
    return {
      offsetLeft: 80,
      textOffsetX: 0,
      textOffsetY: 0
    }
  },
  mounted(){
    let nameContext = d3.select(this.$el).select('.name');
    let bBox = nameContext.node().getBBox()
    this.textOffsetY = bBox.height;
    this.textOffsetX = (this.width - bBox.width) / 2;
  }
}
</script>

<style scoped>

</style>