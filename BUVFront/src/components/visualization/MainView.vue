<template>
    <svg>
        <g v-if="init">
            <sub-view
                    class="A"
                    :x="0" :y="0"
                    :width="px" :height="py"
                    :viewID="'A'"
                    :allData="allData"
            ></sub-view>
            <sub-view
                    class="B"
                    :x="px" :y="0"
                    :width="width - px" :height="py"
                    :viewID="'B'"
                    :allData="allData"
            ></sub-view>
            <sub-view
                    class="C"
                    :x="0" :y="py"
                    :width="px" :height="height - py"
                    :viewID="'C'"
                    :allData="allData"
            ></sub-view>
            <sub-view
                    class="D"
                    :x="px" :y="py"
                    :width="width - px" :height="height - py"
                    :viewID="'D'"
                    :allData="allData"
            ></sub-view>
        </g>

    </svg>
</template>

<script>

import SubView from "@/components/visualization/SubView";
export default {
    name: "MainView",
    components: {SubView},
    props:['records', 'allData'],
    data(){
        return {
            width: 0,  height: 0,
            px: 0,  py: 0,
            init: false
        }
    },
    mounted(){
        this.width = this.$el.clientWidth;
        this.height = this.$el.clientHeight;

        this.px = this.width * 0.8
        this.py = this.height * 0.8

        this.init = true
    },
    methods:{

    }
}
</script>

<style scoped>

</style>