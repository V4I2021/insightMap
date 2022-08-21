<template>
    <div class="main-page" style="height: 100vh; width: 100%">
        <div style="height: 100%; width: 100%; background-color: #fdf4f1">
            <main-view
                    v-if="data"

                    style="height: 100%; width: 100%"
                       :records='data'
            ></main-view>


        </div>
        <TestComponent
                v-if="false"
                :counter="counter"
                :nodes="nodes"
                :links="links"
        ></TestComponent>
    </div>
</template>

<script>
import TestComponent from "@/components/test-page/TestComponent";
import {mapState} from "vuex";
// import * as d3 from "d3";
import MainView from "@/components/visualization/MainView";

export default {
    name: 'TestPage',
    components: {
        MainView,
        TestComponent,
    },
    data(){
        return {
            nodes: [],
            links: []
        }
    },
    mounted(){
        this.$store.dispatch('test/fetchData');
    },
    computed: {
        ...mapState('test', {
            data: state => state.data,
            counter: state => state.counter,
        }),
    },
    watch:{

    }
}
</script>

<style >
.boundary {
    /*border-style: dashed;*/
    border-style: solid;
    border-color: #d3dce6;
    border-width: 0.5px;
    border-radius: 3px;
}

</style>
