<template>
    <g :transform="transform">
        <foreignObject :x="0" :y="0" :width="width" :height="height">
            <canvas class='canvasContainer' :width="width" :height="height"></canvas>
        </foreignObject>
        <rect :width="width" :height="height" fill="none" stroke="grey" stroke-width="1"></rect>
        <!--        <rect fill="red" x="100" y="20" width="20" height="20" v-on:click="click"></rect>-->
        <g class="voronoiContainer"></g>
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
    mounted(){    },
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
            // data: this.subData.data[i]
            this.locs = Array.from(this.allData[this.viewID].loc, (d, i)=>{
                return {x:d[0], y:d[1], c:d[2], score: this.subData.data[i].score}
            })
            let groups = d3.groups(this.locs, d=>d.c)

            let groupObjs = Array.from(groups, d=>{
                return {
                    clusterId: d[0],
                    x: d3.mean(d[1], e=>e.x),
                    y: d3.mean(d[1], e=>e.y),
                    avgScore: d3.mean(d[1], e=>e.score)
                }
            })
            this.avoidOverlap()
            this.avoidOverlap()
            this.renderVoronoi(groupObjs)
        },
        locs(){
            console.log('new loc', this.loc)
        },
        init(){}
    },

    // ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]
    methods:{
        renderVoronoi(particles){
            let width = this.width;
            let height = this.height;
            // const particles = Array.from({length: 100}, () => [Math.random() * width, Math.random() * height]);
            // console.log('particles', particles[0])
            const delaunay = d3.Delaunay.from(particles, d=>this.xScale(d.x), d=>this.yScale(d.y));
            const voronoi = delaunay.voronoi([0.5, 0.5, width - 0.5, height - 0.5]);

            let line = d3.line().x(d=>d[0]).y(d=>d[1])
            let polyContainer = d3.select(this.$el).select('.voronoiContainer')
            polyContainer.selectAll('*').remove()
            for(let polygon of voronoi.cellPolygons()){
                let color = d3.interpolateYlGn(particles[polygon.index].avgScore)
                polyContainer.append('path').attr('d', line(polygon)).attr('fill', color)
                    .attr('fill-opacity', 0.5)
                    .attr('stroke','grey').attr('stroke-width', 1)
            }

        },
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