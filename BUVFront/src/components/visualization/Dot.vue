<template>
    <circle r="5" fill="red"
            :cx="xScale(loc[0])"
            :cy="xScale(loc[1])"
            stroke="white"
    ></circle>
</template>

<script>
export default {
    name: "Dot",
    props:['xScale', 'yScale', 'loc', 'data'],
    mounted(){
        console.log('data ', this.data)
    }
}
</script>

<style scoped>

</style>