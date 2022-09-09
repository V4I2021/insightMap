<template>
    <g>
        <text>{{data.column}}</text>
        <g :transform="'translate(' + [offsetLeft, 0] + ')'">
            <circle r="5" fill="red"></circle>
            <BarChart :data="data" :width="width - offsetLeft" :height="height"></BarChart>
        </g>
    </g>
</template>

<script>
import BarChart from "@/components/visualization/DataColumnStat/BarChart";
export default {
    name: "ColumnVis",
    components: {BarChart},
    props:['data', 'width', 'height'],
    data(){
        return {
            offsetLeft: 150
        }

    }
}
</script>

<style scoped>

</style>