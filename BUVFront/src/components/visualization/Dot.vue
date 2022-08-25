<template>
    <g :transform="transform">
        <path  :d="symboScale(data.insight)"
               @mouseover="mouseover"
               @mouseout="mouseout"
               fill="white" fill-opacity="0.5" stroke="grey" stroke-width="1"></path>
    </g>
</template>

<script>
import * as d3 from "d3";

export default {
    name: "Dot",
    props:['xScale', 'yScale', 'loc', 'data', 'symboScale'],
    data(){
        return {}
    },
    mounted(){
    },
    computed:{
        transform(){
            return "translate(" + [this.xScale(this.loc[0]), this.yScale(this.loc[1])] + ")"
        },
        path(){
            return d3.symbol()
                .size(function() { return 150 } )
                .type(function() { return d3.symbolCross })()
        }
    },
    methods:{
        mouseover(){
            this.$store.commit('test/selectDot', this.data.index)
        },
        mouseout(){
            this.$store.commit('test/selectDot', false)
        }
    }
}
</script>

<style scoped>

</style>