<template>
  <g>
    <text class="name" :y="textOffsetY" :x='textOffsetX' style="font-size: 10px">{{data.column}}</text>
    <g :transform="'translate(' + [offsetLeft, 0] + ')'">
      <BarChart :data="data" :width="width - offsetLeft" :height="height"></BarChart>
    </g>
  </g>
</template>

<script>
import BarChart from "@/components/visualization/DataColumnStat/BarChart";
import * as d3 from 'd3'
export default {
  name: "ColumnVis",
  components: {BarChart},
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
    this.textOffsetY = this.height / 2 + bBox.height / 2;
    this.textOffsetX = this.offsetLeft - bBox.width - 10;
  }
}
</script>

<style scoped>

</style>