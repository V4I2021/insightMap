<template>
    <div class="main-page" style="height: 100vh; width: 100%">
        <div style="height: 100%; width: 100%; background-color: #fdf4f1">
            <el-row style="height: 100%">
                <el-col :span="3" style="height: 100%; background-color: coral" >

                    <div>{{appID}}</div>
                    <el-button size="mini" @click="submit">submit</el-button>
                </el-col>
                <el-col :span="21" style="height: 100%; ; background-color: darkseagreen">
                    <main-view
                            style="width: 100%; height: 100%"
                            :allData='data'
                    ></main-view>
                </el-col>
            </el-row>
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

    },
    computed: {
        ...mapState('test', {
            data: state => state.data,
            counter: state => state.counter,
            appID: state => state.appID
        }),
    },
    methods:{
        submit(){
            this.$store.dispatch('test/fetchDataByApp', {'appID':this.appID});
        }
    },
    watch:{}
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
