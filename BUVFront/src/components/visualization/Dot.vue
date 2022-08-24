<template>
    <circle r="5" fill="blue"
            :cx="xScale(loc[0])"
            :cy="yScale(loc[1])"
            stroke="white"
    ></circle>
</template>

<script>
export default {
    name: "Dot",
    props:['xScale', 'yScale', 'loc', 'data'],
    mounted(){

    }
}
</script>

<style scoped>

</style>