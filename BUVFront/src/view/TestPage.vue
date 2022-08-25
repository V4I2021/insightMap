<template>
    <div class="main-page" style="height: 95vh; width: 100%">
        <div style="height:100%; width: 100%;">
            <el-row style="height: 100%">
                <el-col :span="3" style="height: 100%;" >
                    <el-row>
                        <div>App ID: {{appID}}</div>
                        <el-button size="mini" @click="submit">submit</el-button>
                    </el-row>
                    <el-divider></el-divider>
                    <el-row>
                        <div>Select breakdown: </div>
                        <el-select size="mini" v-model="selectBreakdown" multiple
                                   style="margin-top: 10px"
                                   placeholder="Select Measure">
                            <el-option size="mini"
                                       v-for="item in breakdownCount"
                                       :key="item.breakdown"
                                       :label="item.breakdown"
                                       :value="item.breakdown">
                                <span style="float: left">{{ item.breakdown }}</span>
                                <span style="float: right; color: #8492a6; font-size: 2px">{{ item.index }}</span>
                            </el-option>
                        </el-select>
                        <el-button size="mini" @click="submitBreakdown">submit</el-button>
                    </el-row>
                    <el-divider></el-divider>
                    <el-row>
                        <div>Select subspace: </div>
                        <!--TODO: here-->
                        <el-select
                                style="margin-top: 10px"
                                size="mini" v-for="(subspaceFeature, i) in subspaceStatistics" :key=i
                                v-model="subspaceFeatureMap[subspaceFeature.feature]" multiple :placeholder="subspaceFeature.feature">
                            <el-option size="mini"
                                       v-for="item in subspaceFeature.values"
                                       :key="item"
                                       :label="item"
                                       :value="item">
                                <span style="float: left">{{ item}}</span>
                            </el-option>

                        </el-select>
                        <el-button size="mini" @click="submitSubspace">submit subspace</el-button>
                    </el-row>
                </el-col>
                <el-col :span="21" style="height: 100%;">
                    <main-view
                            style="width: 100%; height: 100%"
                            :allData='data'
                            :symboScale="symboScale"
                            :insightTypes="insightTypes"
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
import MainView from "@/components/visualization/MainView";
import * as d3 from "d3";

export default {
    name: 'TestPage',
    components: {
        MainView,
        TestComponent,
    },
    data(){
        let names = ['symbolCircle', 'symbolDiamond', 'symbolCross', 'symbolDiamond', 'symbolSquare', 'symbolStar', 'symbolTriangle', 'symbolWye'];
        let symbos = []
        names.forEach(name=>{
            let sym = d3.symbol()
                .size(function() { return 120 } )
                .type(function() { return d3[name] })()
            symbos.push(sym)
        })
        return {
            nodes: [],
            links: [],
            selectInsightTypes: [],
            selectBreakdown: [],
            subspaceFeatureMap: {},

            aIndexList: [],
            bIndexList: [],
            cIndexList: [],

            symbos: symbos,
            symboScale: d3.scaleOrdinal().range(symbos)
        }
    },
    mounted(){

    },
    computed: {
        ...mapState('test', {
            data: state => state.data,
            counter: state => state.counter,
            appID: state => state.appID,
            measureValues: state => state.measureValues,
            insightTypes: state => state.insightTypes,
            breakdownCount: state => state.breakdownCount,
            subspaceStatistics: state => state.subspaceStatistics,
            index2View: state => state.index2View

        }),
    },
    methods:{
        submit(){
            this.$store.dispatch('test/fetchDataByApp', {'appID':this.appID});
        },
        updateAllViews(){
            let aIndex = []
            this.data.full.forEach(d=>{
                aIndex.push(d.index)
            })
            let a = aIndex.filter(value => (!this.bIndexList.includes(value)&&(!this.cIndexList.includes(value))));
            let d = this.cIndexList.filter(value => this.bIndexList.includes(value));
            let c = this.cIndexList.filter(value => !d.includes(value));
            let b = this.bIndexList.filter(value => !d.includes(value));

            a.forEach(index=>{
                this.index2View[index] = 'A'
            })
            b.forEach(index=>{
                this.index2View[index] = 'B'
            })
            c.forEach(index=>{
                this.index2View[index] = 'C'
            })
            d.forEach(index=>{
                this.index2View[index] = 'D'
            })

            this.$store.dispatch('test/updateSubViewData', {
                'appID': this.appID,
                'subviewID': 'A',
                'indexList': a
            })

            this.$store.dispatch('test/updateSubViewData', {
                'appID': this.appID,
                'subviewID': 'B',
                'indexList': b
            })

            this.$store.dispatch('test/updateSubViewData', {
                'appID': this.appID,
                'subviewID': 'C',
                'indexList': c
            })

            this.$store.dispatch('test/updateSubViewData', {
                'appID': this.appID,
                'subviewID': 'D',
                'indexList': d
            })
        },
        submitBreakdown(){

            let indexList = []
            let breakdownMap  = {}
            this.selectBreakdown.forEach(breakdown=>{
                breakdownMap[breakdown] = true
            })

            this.data.full.forEach((d)=>{
                if(breakdownMap[d.breakdown]){
                    indexList.push(d.index)
                }
            })
            this.cIndexList = indexList

            this.updateAllViews()

        },
        submitSubspace(){
            console.log('subspaces', this.subspaceFeatureMap)
            let hSubspaceMap = {}
            for(let subspaceFeature in this.subspaceFeatureMap){
                if(this.subspaceFeatureMap[subspaceFeature].length!=0){
                    if(hSubspaceMap[subspaceFeature] == undefined){
                        hSubspaceMap[subspaceFeature] = {}
                    }
                    this.subspaceFeatureMap[subspaceFeature].forEach(d=>{
                        hSubspaceMap[subspaceFeature][d] = true
                    })
                }
            }
            let selectList =  []
            this.data.full.forEach((d)=>{
                let selectSign = true;
                for(let feature in hSubspaceMap){
                    if(hSubspaceMap[feature][d[feature]] != true){
                        selectSign = false
                    }
                }
                if(selectSign == true){
                    selectList.push(d.index)
                }
            })

            this.bIndexList=selectList

            this.updateAllViews()
        },

    },
    watch:{
        subspaceStatistics(newVal){
            console.log('new Feature subspace', newVal)
            // 为什么不能初始化？
            // newVal.forEach(subspaceFeature=>{
            //     this.subspaceFeatureMap[subspaceFeature.feature] = []
            // })
        },
        insightTypes(vals){
            let features = []
            vals.forEach(d=>{
                features.push(d.insight)
            })
            this.symboScale.domain(features)
        }

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
