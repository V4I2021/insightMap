<template>
    <div id="insight-list" ref="test">
        <div v-for="insight in selectedInsights" :key="insight.iid">
            <chart-box class="insight boundary"
                       :insight="insight" :ref="`chartbox${insight.iid}`"/>
        </div>
    </div>
</template>

<script>
import {mapState} from "vuex";
import ChartBox from "./ChartBox";

export default {
    name: "InsightList",
    components: {ChartBox},
    data() {
        return {};
    },
    mounted() {
    },
    computed: {
        ...mapState("test", {
            selectedInsights: state => state.selectedInsights,
        }),
    },
    watch: {
        selectedInsights() {
            const that = this;
            this.$nextTick(() => {
                this.selectedInsights.forEach(item => {
                    that.$refs[`chartbox${item.iid}`][0].drawChart();
                });
            });
        }
    }
};
</script>

<style scoped>

#insight-list {
    overflow-x: hidden;
    overflow-y: scroll;
}

.insight {
    width: calc(100% - 12px) !important;
    aspect-ratio: 3 / 2;
    margin: 10px 5px 0 5px;
}
</style>
