<template>
    <svg :height="height">
        <g v-if="init">
            <g v-for="(columnObj, i) in inputData" :key="i" :transform="'translate(' + [0, i * (unitHeight + 5)] + ')'">
                <ColumnVis :data="columnObj" :width="width" :height="unitHeight"></ColumnVis>
            </g>
        </g>
    </svg>
</template>

<script>
import ColumnVis from "@/components/visualization/DataColumnStat/ColumnVis";
export default {
    name: "RawDataStatistics",
    components: {ColumnVis},
    props:['inputData'],
    data(){
        return {
            width: 0,
            height: 0,
            unitHeight: 30,
            init: false,
            offsetLeft: 150,
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
        },


    }
}
</script>

<style scoped>

</style>