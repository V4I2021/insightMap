<template>
    <svg>
        <g v-if="init">
            <g v-for="(columnObj, i) in inputData" :key="i" :transform="'translate(' + [0, i * (unitHeight + 20)] + ')'">
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
    },
    watch:{
        inputData(){
            console.log('inputData', this.inputData)
        }
    }
}
</script>

<style scoped>

</style>