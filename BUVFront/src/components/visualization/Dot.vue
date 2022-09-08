<template>
    <g :transform="transform">
        <path  :d="symboScale(data.insight)"
               @mouseover="mouseover"
               @mouseout="mouseout"
               fill="#ff7f0e" fill-opacity="0.5" :stroke="stroke" :stroke-width="strokeWidth"
               @click="clickOnDot"
        ></path>

        <!--        <circle-->
        <!--                r="5"-->
        <!--                @mouseover="mouseover"-->
        <!--                @mouseout="mouseout"-->
        <!--                fill="steelblue" fill-opacity="0.5" :stroke="stroke" :stroke-width="strokeWidth"-->
        <!--        ></circle>-->
    </g>
</template>

<script>
import * as d3 from "d3";
import {mapState} from "vuex";

export default {
    name: "Dot",
    props:['data', 'symboScale', 'cx', 'cy'],
    data(){
        return {

        }
    },
    mounted(){
        console.log('dot')
    },
    computed:{
        transform(){
            return "translate(" + [this.cx, this.cy] + ")"
        },
        path(){
            return d3.symbol()
                .size(function() { return 150 } )
                .type(function() { return d3.symbolCross })()
        },
        selectedType(){
            if(this.selectedDots.includes(this.data.index)){
                return 'select'
            }else{
                if(this.highlightedDots.includes(this.data.index)){
                    return 'highlight'
                }else{
                    return false
                }
            }
        },
        stroke(){
            if(this.selectedType == 'select'){
                return 'orange'
            }else if(this.selectedType == 'highlight'){
                return 'steelblue'
            }else{
                return 'grey'
            }
        },
        strokeWidth(){
            if(this.selectedType == false){
                return 1
            }else{
                return 3
            }
        },
        ...mapState('test', {
            selectedDots: state => state.selectedDots,
            highlightedDots: state => state.highlightedDots
        }),
    },
    methods:{
        mouseover(){
            this.$store.commit('test/selectDot', this.data.index)
        },
        mouseout(){
            this.$store.commit('test/selectDot', false)
        },
        clickOnDot(){
            this.$store.commit('test/selectDotByClick', this.data.iid)
        }
    }
}
</script>

<style scoped>

</style>