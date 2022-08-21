<template>
    <svg>
        <g  v-if="init">
            <g
                    class="legend" :transform="'translate('+[width, 15]+')'">
                <g
                        v-for="(d, i) in insightTypes" :key=i
                        :transform="'translate('+[10, 20 * i]+')'">
                    <circle r="5"
                            :fill-opacity="fillOpacity"
                            :fill="colorScale(d)"

                    ></circle>
                    <text x=10 y=4 style="font-size: 12px">{{d}}</text>
                </g>

            </g>
            <g>
                <line v-for="(d, i) in currentLinks" :key="i"
                      :x1="d.src.x"
                      :y1="d.src.y"
                      :x2="d.dst.x"
                      :y2="d.dst.y"
                      stroke="grey"
                      stroke-width="1"
                ></line>
            </g>
            <g>
                <circle v-for="(d, i) in records.A_results" :key=i
                        @mouseover="mouseover(d, A)"
                        @mouseout="mouseout(d, A)"
                        :cx="A.xScale(d.x)" :cy="A.yScale(d.y)" r="5" :fill="colorScale(d.insight)" :fill-opacity="fillOpacity" stroke="white"
                >
                </circle>
            </g>
            <g>
                <g :transform="'translate(' + [B.config[0], B.config[1]]+ ')'">
                    <circle v-for="(d, i) in records.B_results" :key="i"
                            :cx="B.xScale(d.x)" :cy="B.yScale(d.y)" r="5" :fill="colorScale(d.insight)" :fill-opacity="fillOpacity" stroke="white"
                            @mouseover="mouseover(d, B)"
                            @mouseout="mouseout(d, B)"
                    ></circle>
                </g>

                <g :transform="'translate(' + [C.config[0], C.config[1]]+ ')'">
                    <circle v-for="(d, i) in records.C_results" :key="i"
                            @mouseover="mouseover(d, C)"
                            @mouseout="mouseout(d, C)"
                            :cx="C.xScale(d.x)" :cy="C.yScale(d.y)" r="5" :fill="colorScale(d.insight)" :fill-opacity="fillOpacity" stroke="white"
                    ></circle>
                </g>

                <g :transform="'translate(' + [D.config[0], D.config[1]]+ ')'">
                    <circle v-for="(d, i) in records.D_results" :key="i"
                            @mouseover="mouseover(d, D)"
                            @mouseout="mouseout(d, D)"
                            :cx="D.xScale(d.x)" :cy="D.yScale(d.y)" r="5" :fill="colorScale(d.insight)" :fill-opacity="fillOpacity" stroke="white"
                    ></circle>
                </g>
            </g>

            <g >
                <rect class="A"
                      :x="A.config[0]" :y="A.config[1]"
                      :width="A.config[2]" :height="A.config[3]"
                      stroke="grey" stroke-width="2" fill="none">
                </rect>
                <g :transform="'translate(' + [B.config[0], B.config[1]] + ')' ">
                    <rect class="B"
                          :width="B.config[2]" :height="B.config[3]"
                          stroke="grey" stroke-width="2" fill="none">
                    </rect>
                    <text style="font-size:10px" :y="15">subspace: team_name is Los Angeles Lakers</text>

                </g>
                <g :transform="'translate(' + [C.config[0], C.config[1]] + ')' ">
                    <rect class="C"
                          :width="C.config[2]" :height="C.config[3]"
                          stroke="grey" stroke-width="2" fill="none">
                    </rect>
                    <text style="font-size:10px" :y="15">breakdown: lg_name</text>
                </g>
                <rect class="D"
                      :x="D.config[0]" :y="D.config[1]"
                      :width="D.config[2]" :height="D.config[3]"
                      stroke="grey" stroke-width="2" fill="none">
                </rect>
            </g>

        </g>
    </svg>
</template>

<script>
import * as d3 from "d3";

export default {
    name: "MainView",
    props:['records'],
    data(){
        return {
            init: false,
            A:{
                xScale: d3.scaleLinear(),
                yScale: d3.scaleLinear(),
                config: [0,0,0,0], //x, y, width, height
                d: undefined
            },
            B:{
                xScale: d3.scaleLinear(),
                yScale: d3.scaleLinear(),
                config:[0,0,0,0], //x, y, width, height,
                d: undefined
            },
            C:{
                xScale: d3.scaleLinear(),
                yScale: d3.scaleLinear(),
                config:[0,0,0,0], //x, y, width, height
                d: undefined
            },
            D:{
                xScale: d3.scaleLinear(),
                yScale: d3.scaleLinear(),
                config:[0,0,0,0], //x, y, width, height
                d: undefined
            },


            width: 1000,
            height: 800,

            insightTypes:[],
            colorScale: undefined,
            fillOpacity: 0.9,

            currentLinks: []
        }
    },
    mounted(){


        this.A.d = this.records.A_results;
        this.B.d = this.records.B_results;
        this.C.d = this.records.C_results;
        this.D.d = this.records.D_results;
        // 0,1,2,3
        this.A.config = [0, 0, this.width*3.5/5, this.height*3.5/5]
        this.B.config = [this.A.config[2], 0, this.width - this.A.config[2], this.A.config[3]]
        this.C.config = [0, this.A.config[3],this.A.config[2], this.height -  this.A.config[3]]
        this.D.config = [this.A.config[2], this.A.config[3], this.width - this.A.config[2], this.height -  this.A.config[3]]


        this.A.xScale.domain(d3.extent(this.records.A_results, d=>d.x)).range([15, this.A.config[2] - 15]);
        this.A.yScale.domain(d3.extent(this.records.A_results, d=>d.y)).range([15, this.A.config[3] - 15]);

        this.B.xScale.domain(d3.extent(this.records.B_results, d=>d.x)).range([15, this.B.config[2] - 15]);
        this.B.yScale.domain(d3.extent(this.records.B_results, d=>d.y)).range([15, this.B.config[3] - 15]);

        this.C.xScale.domain(d3.extent(this.records.C_results, d=>d.x)).range([15, this.C.config[2] - 15]);
        this.C.yScale.domain(d3.extent(this.records.C_results, d=>d.y)).range([15, this.C.config[3] - 15]);

        this.D.xScale.domain(d3.extent(this.records.D_results, d=>d.x)).range([15, this.D.config[2] - 15]);
        this.D.yScale.domain(d3.extent(this.records.D_results, d=>d.y)).range([15, this.D.config[3] - 15]);

        let insightMap= {}
        let insightTypes = []
        console.log('rrrrr')
        this.records.A_results.forEach(d=>{
            let insightType = d.insight
            if(!insightMap[insightType]){
                insightMap[insightType] = true
                insightTypes.push(insightType)
            }
        })

        let colorScale = d3.scaleOrdinal().domain(insightTypes).range(d3['schemeCategory10'])

        this.colorScale = colorScale

        // this.records.A_results.forEach(d=>{
        //     d.lx = this.A.xScale(d.x)
        //     d.ly = this.A.yScale(d.y)
        //     d.fill=colorScale(d.insight)
        // })

        console.log('records', this.records.A_results, insightMap)

        console.log('insight Types ', insightTypes)

        this.insightTypes = insightTypes
        //
        // let legendContainer = d3.select(this.$el).select('.legend')
        // legendContainer.selectAll('circle').data(insightTypes).enter().append('circle')
        //     .attr('cx', 10)
        //     .attr('cy', (d, i)=> i * 25)
        //     .attr('r', 5)
        //     .attr('fill', d=>colorScale(d))

        this.init = true

    },
    methods:{
        mouseover(d, X){
            console.log('mouseover', d, X)
            let src = {
                x: X.config[0] + X.xScale(d.x),
                y: X.config[1] + X.yScale(d.y),

            }

            let cons = [this.A, this.B, this.C, this.D]
            cons.forEach(dstX=>{
                if(dstX == X){
                    return
                }
                let ds = dstX.d
                ds.forEach(td=>{
                    if(td.id == d.id){
                        let dst = {
                            x: dstX.config[0] + dstX.xScale(td.x),
                            y: dstX.config[1] + dstX.yScale(td.y),
                        }
                        this.currentLinks.push({
                            'src': src, 'dst': dst
                        })
                    }

                })

            })
            console.log('currentLink', this.currentLinks)
        },
        mouseout(d){
            console.log('mouseout', d)
            this.currentLinks = []
        }
    }
}
</script>

<style scoped>

</style>