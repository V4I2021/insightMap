<template>
    <div id="insight-list" ref="test" s>
      <el-row style="width: 100%"> </el-row>
        <el-col v-for="insight in selectedInsights" :key="insight.iid" :span="8"
                class="boundary">
          <chart-box class="insight boundary"
                       :insight="insight" :ref="`chartbox${insight.iid}`"/>
        </el-col>
    </div>
</template>

<script>
import {mapState} from "vuex";
import ChartBox from "./ChartBox";

export default {
    name: "InsightList",
    components: {ChartBox},
    data() {
        return {
          unitWidth: 0,
        };
    },
    mounted() {
      this.unitWidth = this.$el.clientWidth / 3;
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
    /*overflow-x: scroll;*/
    /*overflow-y: scroll;*/
}

.insight {
    width: calc(100% - 12px) !important;
    aspect-ratio: 3 / 2;
    margin: 10px 5px 0 5px;
}
</style>
