<template>
    <div style="background-color: darkseagreen">
        <div v-for="insight in selectedInsights" :key="insight.iid">{{insight.iid}}</div>
    </div>
</template>

<script>
import {mapState} from "vuex";

export default {
    name: "InsightList",
    computed:{
        ...mapState('test', {
            selectedInsights: state=>state.selectedInsights,
        }),
    }



}
</script>

<style scoped>

</style>