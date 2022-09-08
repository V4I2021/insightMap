<template>
    <svg>
        <g v-if="init">
            <g class="legend">
                <g v-for="(d, i) in insightTypes" :key=i :transform="'translate(' + [15, 10 + i * 25] + ')' ">
                    <path :d="symboScale(d.insight)" fill="none" stroke="grey" stroke-width="1"></path>
                    <text x="20" y="5" style="font-size: 10px">{{ d.insight}}</text>
                </g>
            </g>

            <sub-view
                    class="A"
                    :x="0" :y="0"
                    :width="px" :height="py"
                    :viewID="'A'"
                    :allData="allData"
                    :symboScale="symboScale"
                    :xScale="scaleConfig.A.xScale"
                    :yScale="scaleConfig.A.yScale"
            ></sub-view>
            <sub-view
                    class="B"
                    :x="px" :y="0"
                    :width="width - px" :height="py"
                    :viewID="'B'"
                    :allData="allData"
                    :symboScale="symboScale"
                    :xScale="scaleConfig.B.xScale"
                    :yScale="scaleConfig.B.yScale"
            ></sub-view>
            <sub-view
                    class="C"
                    :x="0" :y="py"
                    :width="px" :height="height - py"
                    :viewID="'C'"
                    :allData="allData"
                    :symboScale="symboScale"
                    :xScale="scaleConfig.C.xScale"
                    :yScale="scaleConfig.C.yScale"
            ></sub-view>
            <sub-view
                    class="D"
                    :x="px" :y="py"
                    :width="width - px" :height="height - py"
                    :viewID="'D'"
                    :allData="allData"
                    :symboScale="symboScale"
                    :xScale="scaleConfig.D.xScale"
                    :yScale="scaleConfig.D.yScale"
            ></sub-view>
            <g class="links">
                <path v-for="(d, i) in renderingPath" :key=i
                      :d="d.path"
                      :stroke="d.same == false? 'steelblue' : 'orange'"
                      stroke-width="2"
                      stroke-opacity="0.3"

                      fill="none">
                </path>
                <!--                stroke-dasharray="3 1"-->
            </g>


        </g>
        <g class="circleContainer">
            <circle r=25 fill="red" :transform="'translate(' + [tpx, tpy] + ')'"> </circle>
        </g>
    </svg>
</template>

<script>

import SubView from "@/components/visualization/SubView";
import * as d3 from "d3";
import {mapState} from "vuex";

let curveGenerator = d3.line()
    .x((p) => p.x)
    .y((p) => p.y)
    .curve(d3.curveBasis);

export default {
    name: "MainView",
    components: {SubView},
    props:['records', 'allData', 'symboScale', 'insightTypes'],
    data(){
        return {
            width: 0,  height: 0,
            px: 0,  py: 0,
            tpx:0, tpy:0,
            init: false,
            boundary: 30,

            scaleConfig:{
                'A': {
                    xScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                    yScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                },
                'B':{
                    xScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                    yScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                },
                'C':{
                    xScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                    yScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                },
                'D':{
                    xScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                    yScale: d3.scaleLinear().domain([0, 1]).range([0,1]),
                }
            },

            offsetConfig:{
                "A":[0,0],
                "B":[0,0],
                "C":[0,0],
                "D":[0,0],
            }
        }
    },
    mounted(){
        this.width = this.$el.clientWidth;
        this.height = this.$el.clientHeight;

        this.px = this.width * 0.7
        this.py = this.height * 0.7

        this.tpx = this.px
        this.tpy = this.py

        this.offsetConfig = {
            "A":[0,0],
            "B":[this.px,0],
            "C":[0,this.py],
            "D":[this.px,this.py]
        }

        let ratioCircle = d3.select(this.$el).select('.circleContainer').select('circle')
        console.log('rationCircle', ratioCircle)
        ratioCircle.call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

        function dragstarted() {

        }
        let _this = this;
        function dragged(event) {
            _this.tpx = event.x;
            _this.tpy = event.y;
            // console.log('dragiiiiiiiiiiiiiiiiiing',event, d)
        }

        function dragended() {
            _this.px = _this.tpx;
            _this.py = _this.tpy;
            _this.updateScale();
        }

        this.updateScale()

        this.init = true
    },
    methods:{

        updateScale(){
            this.scaleConfig.A.xScale.range([this.boundary, this.px-this.boundary])
            this.scaleConfig.A.yScale.range([this.boundary, this.py-this.boundary])

            this.scaleConfig.B.xScale.range([this.boundary, this.width - this.px-this.boundary])
            this.scaleConfig.B.yScale.range([this.boundary, this.height - this.py-this.boundary])

            this.scaleConfig.C.xScale.range([this.boundary, this.px-this.boundary])
            this.scaleConfig.C.yScale.range([this.boundary, this.height - this.py-this.boundary])

            this.scaleConfig.D.xScale.range([this.boundary, this.width - this.px-this.boundary])
            this.scaleConfig.D.yScale.range([this.boundary, this.height - this.py-this.boundary])

            console.log('update Scale', this.scaleConfig.A.xScale.range(), this.scaleConfig.A.xScale.domain())
        }
    },
    watch:{
        selectedLinks(){

        }
    },
    computed:{
        ...mapState('test', {
            selectedLinks: state=>state.selectLinks,
            fullData: state=>state.data.full,
            data: state=>state.data,
            index2View: state=>state.index2View,
            index2Loc: state=>state.index2Loc
        }),
        renderingLink(){
            let out = []
            this.selectedLinks.forEach(d=>{
                let src_index = d[0];
                let dst_index = d[1];

                let srcViewIndex = this.index2View[src_index];
                let dstViewIndex = this.index2View[dst_index];

                let srcOffset = this.offsetConfig[srcViewIndex];
                let dstOffset = this.offsetConfig[dstViewIndex];

                let srcScale = this.scaleConfig[srcViewIndex];
                let dstScale = this.scaleConfig[dstViewIndex];

                let sign = false
                if(srcViewIndex == dstViewIndex){
                    sign = true
                }
                out.push({
                    src:{
                        x: srcOffset[0] + srcScale.xScale(this.index2Loc[src_index][0]),
                        y: srcOffset[1] + srcScale.yScale(this.index2Loc[src_index][1])
                    },
                    dst:{
                        x: dstOffset[0] + dstScale.xScale(this.index2Loc[dst_index][0]),
                        y: dstOffset[1] + dstScale.yScale(this.index2Loc[dst_index][1])
                    },
                    same: sign
                })
            })
            return out
        },
        renderingPath(){
            let paths = []
            this.renderingLink.forEach(d=>{

                let arr = [d.src,
                    {
                        x:d.src.x + (d.dst.x - d.src.x) * 3 / 4,
                        y:d.src.y,
                    },
                    d.dst]

                paths.push({path: curveGenerator(arr), same: d.same})
            })

            return paths
        }
    }
}

</script>

<style scoped>

</style>