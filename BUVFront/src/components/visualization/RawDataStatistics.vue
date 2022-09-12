<template>
  <svg :height="height">
    <g v-if="init">
      <g v-if="false">
        <g v-for="(columnObj, i) in inputData" :key="i" :transform="'translate(' + [0, i * (unitHeight + 5)] + ')'">
          <ColumnVis :data="columnObj" :width="width" :height="unitHeight"></ColumnVis>
        </g>
      </g>
      <g>
        <g v-for="(columnObj, i) in inputData" :key="i" :transform="'translate(' + [i * unitWidthVertical, 0] + ')'">
          <ColumnVisVertical :data="columnObj" :width="unitWidthVertical" :height="height"> </ColumnVisVertical>
        </g>
      </g>
    </g>
  </svg>
</template>

<script>
import ColumnVis from "@/components/visualization/DataColumnStat/ColumnVis";
import ColumnVisVertical from "@/components/visualization/DataColumnStat/ColumnVisVertical";
export default {
  name: "RawDataStatistics",
  components: {ColumnVis, ColumnVisVertical},
  props:['inputData'],
  data(){
    return {
      width: 0,
      height: 0,
      unitHeight: 30,
      init: false,
      offsetLeft: 150,

      heightVertical: 0,
      unitWidthVertical: 150,
    }
  },
  mounted(){
    console.log('statistics results', this.inputData)
    this.width = this.$el.clientWidth;
    this.height = this.$el.clientHeight;


    this.init = true
    // this.height = this.unitHeight * this.inputData.length
    // this.height  = 500
  },
  watch:{
    inputData(){
      console.log('inputData', this.inputData)
      this.height = this.unitHeight* this.inputData.length
      this.unitWidthVertical = this.width / this.inputData.length;
      this.height = 300
    },


  }
}
</script>

<style scoped>

</style>