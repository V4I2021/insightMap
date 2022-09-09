<template>
    <g>
        <circle :r=size fill="white" fill-opacity="0.5"> </circle>
        <line :x1=" centerBoundary" :y1=" centerBoundary" :x2="centerBoundary" :y2="size" :stroke="stroke" stroke-width="1"></line>
        <line :x1="-centerBoundary" :y1=" centerBoundary" :x2="-centerBoundary" :y2="size" :stroke="stroke" stroke-width="1"></line>
        <line :x1="-centerBoundary" :y1=" centerBoundary" :x2="-size" :y2="centerBoundary" :stroke="stroke" stroke-width="1"></line>
        <line :x1="-centerBoundary" :y1="-centerBoundary" :x2="-size" :y2="-centerBoundary" :stroke="stroke" stroke-width="1"></line>
        <line :x1="-centerBoundary" :y1="-centerBoundary" :x2="-centerBoundary" :y2="-size" :stroke="stroke" stroke-width="1"></line>
        <line :x1=" centerBoundary" :y1="-centerBoundary" :x2="centerBoundary" :y2="-size" :stroke="stroke" stroke-width="1"></line>
        <line :x1=" centerBoundary" :y1="-centerBoundary" :x2="size" :y2="-centerBoundary" :stroke="stroke" stroke-width="1"></line>
        <line :x1=" centerBoundary" :y1=" centerBoundary" :x2="size" :y2="centerBoundary" :stroke="stroke" stroke-width="1"></line>
    </g>
</template>

<script>
export default {
    name: "ControlGlyph",
    data(){
        return {
            centerBoundary: 2,
            size: 12,
            stroke: 'grey'
            // steelblue
        }
    }
}
</script>

<style scoped>

</style>