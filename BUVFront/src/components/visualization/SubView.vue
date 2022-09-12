<template>
    <g :transform="transform">
        <foreignObject :x="0" :y="0" :width="width" :height="height">
            <canvas class='canvasContainer' :width="width" :height="height"></canvas>
        </foreignObject>
        <rect :width="width" :height="height" fill="none" stroke="grey" stroke-width="1"></rect>
        <!--        <rect fill="red" x="100" y="20" width="20" height="20" v-on:click="click"></rect>-->
        <g class="voronoiContainer"></g>
        <g v-if="true">
            <Dot v-for="(loc, i) in locs" :key='i'
                 :cx="loc.cx"
                 :cy="loc.cy"
                 :data="subData.data[i]"
                 :symboScale="symboScale"
            ></Dot>
        </g>
        <rect v-if="viewID == 'B' || viewID == 'C' "
              rx="5" ry="5"
              :width="box.width" :height="box.height" fill="steelblue" fill-opacity="0.5"></rect>
        <g class="container">
            <g class="cc" :transform="textTransform">
                <text class='label' style="font-size:12px" fill="black">{{label}}</text>
            </g>
        </g>
    </g>
</template>

<script>
import * as d3 from "d3";
import Dot from "@/components/visualization/Dot";

export default {
    components: {Dot},
    props: ['x', 'y', 'width', 'height', 'viewID', 'allData', 'symboScale', 'xScale', 'yScale', 'contextConfig'],
    name: "SubView",
    data(){
        return {
            xRange: [0, 0],
            yRange: [0, 0],
            wholeWidth: this.width,
            wholeHeight: this.height,
            boundary: 20,
            init: false,
            locs: [],
            labelSize: 30,
            label:'',
            textTransform: "rotate(0)"

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
        box(){
            if(this.width < this.height){
                return {
                    width: this.width,
                    height: this.labelSize
                }
            }else{
                return {
                    width: this.labelSize,
                    height: this.height
                }
            }
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
        width(){
            this.updateLayout()
        },
        updateCount(){
            this.updateLayout()
        },
        locs(){
            console.log('new loc', this.loc)
        },
        init(){
        },
        contextConfig(val){
            let layer1 = []
            for(let i = 0, ilen = val.value.length; i < ilen; i++){
                let label = val.value[i].name + ': ' + val.value[i].value.join(', ')
                if(val.value[i].value.length == 0) continue
                layer1.push(label)
            }
            let results = layer1.join('; ')
            this.label = results

            let labelEle = d3.select(this.$el).select('.label').text(this.label);
            let bBox = labelEle.node().getBBox();
            console.log(' this.viewID, ', this.viewID, this.width, this.height)
            if(this.width < this.height){
                this.textTransform = 'rotate(0)'
                let x = (this.width - bBox.width) / 2;
                let y = (this.labelSize + bBox.height) / 2 - 2;
                labelEle.attr('x', x).attr('y', y)
            }else{
                this.textTransform = 'rotate(-90)'
                let container = d3.select(this.$el).select('.container')
                container.attr('transform', 'translate(' + [20, (bBox.width + this.height) / 2] + ')')
                console.log('bBox ', this.viewID, bBox)
            }
        }
    },

    // ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"]
    methods:{
        updateLayout(){

            this.xDomain = d3.extent(this.subData.loc, d=>d[0])
            this.yDomain = d3.extent(this.subData.loc, d=>d[1])
            this.xScale.domain(this.xDomain);
            this.yScale.domain(this.yDomain);

            console.log('xRange ', this.xScale.domain(), this.xScale.range())
            // data: this.subData.data[i]
            this.locs = Array.from(this.allData[this.viewID].loc, (d, i)=>{
                return {
                    x:d[0],
                    y:d[1],
                    c:d[2],
                    score: this.subData.data[i].score,
                    cx:this.xScale(d[0]),
                    cy:this.yScale(d[1]),
                }
            })
            let groups = d3.groups(this.locs, d=>d.c)
            let groupObjs = Array.from(groups, d=>{
                return {
                    clusterId: d[0],
                    x: d3.mean(d[1], e=>e.cx),
                    y: d3.mean(d[1], e=>e.cy),
                    avgScore: d3.mean(d[1], e=>e.score)
                }
            })
            // this.avoidOverlap()
            this.avoidOverlap()
            this.avoidOverlap()

            this.renderVoronoi(groupObjs)
        },
        renderVoronoi(particles){
            let width = this.width;
            let height = this.height;

            const delaunay = d3.Delaunay.from(particles, d=>d.x, d=>d.y);
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
            return Math.sqrt((a.cx - b.cx)**2 + (a.cy - b.cy)**2)
        },
        click(){
            console.log('click')
            this.avoidOverlap()
        },
        avoidOverlap(){
            let locs = this.locs;
            let r = 4
            let nOverlap = 0
            this.init = false
            for(let i = 0, ilen = locs.length; i<ilen; i++){
                let src = locs[i]
                for(let j = 0, jlen = locs.length; j<jlen; j++){
                    let dst = locs[j]
                    let dis = this.disf(src, dst)
                    if(dis < r){
                        let dx = dst.cx - src.cx
                        let dy = dst.cy - src.cy
                        dst.cx += dx
                        dst.cy += dy
                        src.cx -= dx
                        src.cy -= dy
                        nOverlap += 1
                    }
                }
            }
            this.init = true
            console.log('nOverlap', nOverlap)
        }
    }
}
</script>

<style scoped>

</style>