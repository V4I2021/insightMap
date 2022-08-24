<template>
    <g :transform="transform">
        <circle rx="0" ry="0" r="3" fill="red"></circle>
        <rect :width="width" :height="height" fill="pink" stroke="white" stroke-width="1"></rect>

        <g>
            <Dot v-for="(loc, i) in subData.loc" :key='i'
                 :xScale="xScale"
                 :yScale="yScale"
                 :loc="loc"
                 :data="subData.data[i]"
            ></Dot>
        </g>
    </g>
</template>

<script>
import * as d3 from "d3";
import Dot from "@/components/visualization/Dot";

export default {
    components: {Dot},
    props: ['x', 'y', 'width', 'height', 'viewID', 'allData'],
    name: "SubView",
    data(){
        return {
            xRange: [0, 0],
            yRange: [0, 0],
            wholeWidth: this.width,
            wholeHeight: this.height,
            boundary: 20
        }
    },
    mounted(){

    },
    computed: {
        xScale(){
            return d3.scaleLinear().domain(this.xRange).range([this.boundary, this.wholeWidth-this.boundary])
        },
        yScale(){
            return d3.scaleLinear().domain(this.yRange).range([this.boundary, this.wholeHeight-this.boundary])
        },
        transform(){
            return 'translate(' + [this.x, this.y] + ')'
        },
        subData(){
            return this.allData[this.viewID]
        },
        updateCount(){

            return this.allData[this.viewID]['count']
        }
    },
    watch:{
        updateCount(){
            this.xRange = d3.extent(this.subData.loc, d=>d[0])
            this.yRange = d3.extent(this.subData.loc, d=>d[1])
            console.log('domain  ', this.viewID, this.xRange, this.yRange, this.subData)
            console.log('range  ',this.xScale.range(), this.yScale.range() )
        }
    }
}
</script>

<style scoped>

</style>