<template>
    <g :transform="transform">
        <!--        <circle rx="0" ry="0" r="3" fill="red"></circle>-->
        <rect :width="width" :height="height" fill="none" stroke="grey" stroke-width="1"></rect>
        <rect fill="red" x="100" y="20" width="20" height="20" v-on:click="click"></rect>
        <g v-if="init">
            <Dot v-for="(loc, i) in locs" :key='i'
                 :xScale="xScale"
                 :yScale="yScale"
                 :loc="loc"
                 :data="subData.data[i]"
                 :symboScale="symboScale"
            ></Dot>
        </g>
    </g>
</template>

<script>
import * as d3 from "d3";
import Dot from "@/components/visualization/Dot";

export default {
    components: {Dot},
    props: ['x', 'y', 'width', 'height', 'viewID', 'allData', 'symboScale', 'xScale', 'yScale'],
    name: "SubView",
    data(){
        return {
            xRange: [0, 0],
            yRange: [0, 0],
            wholeWidth: this.width,
            wholeHeight: this.height,
            boundary: 20,
            init: false,
            locs: []
        }
    },
    mounted(){
        this.avoidOverlap()
        this.init = true
    },
    computed: {
        // xScale(){
        //     return d3.scaleLinear().domain(this.xRange).range([this.boundary, this.wholeWidth-this.boundary])
        // },
        // yScale(){
        //     return d3.scaleLinear().domain(this.yRange).range([this.boundary, this.wholeHeight-this.boundary])
        // },
        transform(){
            return 'translate(' + [this.x, this.y] + ')'
        },
        subData(){
            return this.allData[this.viewID]
        },
        updateCount(){
            return this.allData[this.viewID]['count']
        },
        // locs(){
        //     let arr = []
        //     arr = Array.from(this.allData[this.viewID].loc, d=>{
        //         return {x:d[0], y:d[1]}
        //     })
        //     return arr
        // }
    },
    watch:{
        updateCount(){
            this.xRange = d3.extent(this.subData.loc, d=>d[0])
            this.yRange = d3.extent(this.subData.loc, d=>d[1])
            this.xScale.domain(this.xRange);
            this.yScale.domain(this.yRange)
            console.log('domain  ', this.viewID, this.xRange, this.yRange, this.subData)
            console.log('range  ',this.xScale.range(), this.yScale.range() )

            this.locs = Array.from(this.allData[this.viewID].loc, d=>{
                return {x:d[0], y:d[1]}
            })

        },
        locs(){
            console.log('new loc', this.loc)
        }
    },
    methods:{
        // disf(a, b){
        //     return Math.sqrt((this.xScale(a[0]) - this.xScale(b[0]))**2 + (this.yScale(a[1]) - this.yScale(b[1]))**2)
        // },
        disf(a, b){
            return Math.sqrt((this.xScale(a.x) - this.xScale(b.x))**2 + (this.yScale(a.y) - this.yScale(b.y))**2)
        },
        click(){
            console.log('click')
            this.avoidOverlap()
        },
        avoidOverlap(){
            let locs = this.locs;
            let r = 6
            let nOverlap = 0
            this.init = false
            for(let i = 0, ilen = locs.length; i<ilen; i++){
                let src = locs[i]
                for(let j = 0, jlen = locs.length; j<jlen; j++){
                    let dst = locs[j]
                    let dis = this.disf(src, dst)
                    if(dis < r){
                        let dx = dst.x - src.x
                        let dy = dst.y - src.y
                        dst.x += dx
                        dst.y += dy
                        src.x -= dx
                        src.y -= dy
                        nOverlap += 1
                    }
                }
            }
            this.init = true
            console.log('runs', nOverlap)
        }
    }
}
</script>

<style scoped>

</style>