<template>
    <div>
        <el-descriptions size="mini"
                v-for="(item, i) in displayInsights"  :key='i'
                :title="'Insight Index: '+item.index" :column="1" border>
            <el-descriptions-item
                    v-for="(entry, j) in item.featureValues"  :key='j'
                    :label="entry[0]">{{entry[1]}}</el-descriptions-item>
        </el-descriptions>
    </div>
</template>

<script>
import {mapState} from "vuex";

export default {
    name: "Information",
    computed:{
        ...mapState('test', {
            selectedDots: state => state.selectedDots,
            fullData: state => state.data.full
        }),
        displayInsights(){
            return Array.from(this.selectedDots, d=>
                {
                    let _data = this.fullData[d]
                    return {
                        featureValues: Object.entries(_data),
                        index: _data.index
                    }
                }
            )
        }
    },
    watch:{
        selectedDots(){
        }
    }
}
</script>

<style scoped>

</style>