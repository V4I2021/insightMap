<template>
    <div class="main-page" style="height: 95vh; width: 100%">
        <div style="height:100%; width: 100%; text-align: left">
            <el-row style="width: 100%">
                <div>
                    <div class="mini_head">
                        <div class="mini_title">Control</div>
                    </div>
                    <!-- Section 1 select data-->
                    <el-select style="width: 120px; margin-top: 5px; margin-bottom: 5px"
                               size="mini" v-model="selectedData"
                               placeholder="Select data">
                        <el-option size="mini"
                                   v-for="item in dataNames"
                                   :key="item"
                                   :label="item"
                                   :value="item">
                            <span style="float: left">{{item}}</span>
                            <span style="float: right; color: #8492a6; font-size: 2px">{{item.index }}</span>
                        </el-option>
                    </el-select>

                    <el-button style="margin-left: 5px" size="mini" @click="submit">Confirm</el-button>

                    <el-divider v-if="selectedData" direction="vertical"></el-divider>

                    <!-- Section 2 select breakdown-->

                    <el-select v-if="selectedData"
                               style="width: 120px;"
                               size="mini" v-model="selectBreakdown" multiple
                               placeholder="Select Breakdown">
                        <el-option size="mini"
                                   v-for="item in breakdownCount"
                                   :key="item.breakdown"
                                   :label="item.breakdown"
                                   :value="item.breakdown">
                            <span style="float: left">{{ item.breakdown }}</span>
                            <span style="float: right; color: #8492a6; font-size: 2px">{{ item.index }}</span>
                        </el-option>
                    </el-select>
                    <el-button v-if="selectedData"
                               size="mini" @click="submitBreakdown" style="margin-top: 0px; margin-left:5px"
                               :disabled="!breakdownSelected">Confirm</el-button>
                    <el-divider v-if="selectedData" direction="vertical"></el-divider>


                    <!-- Section 3 select subspace-->

                    <el-select
                            style="margin-top: 0px; width: 120px; margin-left: 5px"
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
                    <el-button v-if="selectedData" style="margin-top: 5px; margin-bottom: 5px; margin-left: 5px" size="mini"
                               :disabled="!subspaceSelected"
                               @click="submitSubspace">Confirm subspace</el-button>
                </div>

            </el-row>
            <el-row style="height: 100%" >
                <el-col :span="16" style="height: 100%;" class="boundary">
                    <div class="mini_head">
                        <div class="mini_title">Projection View:</div>
                    </div>
                    <main-view
                            style="width: 100%; height: calc(100% - 20px)"
                            :allData='data'
                            :symboScale="symboScale"
                            :insightTypes="insightTypes"
                    ></main-view>
                </el-col>
                <el-col v-if="false" :span="6" style="height: 100%;" class="boundary">
                    <div class="mini_head">
                        <div class="mini_title">Information View:</div>
                    </div>
                    <Information></Information>
                </el-col>

                <el-col :span="8"  style="height: 100%;" class="boundary">
                    <el-row style="width: 100%">

                        <div class="mini_head">
                            <div class="mini_title">Data distribution:</div>
                        </div>
                        <RawDataStatistics
                                :inputData ="rawStatistics"
                                style="width: 100%;">
                        </RawDataStatistics>
                    </el-row>
                    <el-row style="width: 100%;height:calc(100% - 270px)">
                        <div class="mini_head">
                            <div class="mini_title">Insight List:</div>
                        </div>
                        <InsightList style="width: 100%; height:calc(100% - 20px)"></InsightList>
                    </el-row>
                </el-col>
            </el-row>
        </div>

    </div>
</template>

<script>
import {mapState} from "vuex";
import MainView from "@/components/visualization/MainView";
import * as d3 from "d3";
import Information from "@/components/visualization/Information";
import InsightList from "@/components/visualization/InsightList";
import RawDataStatistics from "@/components/visualization/RawDataStatistics";

export default {
    name: 'TestPage',
    components: {
        RawDataStatistics,
        InsightList,
        Information,
        MainView
    },
    data(){
        let names = ['symbolCircle', 'symbolDiamond', 'symbolCross', 'symbolDiamond', 'symbolSquare', 'symbolStar', 'symbolTriangle', 'symbolWye'];
        let symbos = []
        names.forEach(name=>{
            let sym = d3.symbol()
                .size(function() { return 40 } )
                .type(function() { return d3[name] })()
            symbos.push(sym)
        })
        return {
            dataNames: ['NBA'],
            selectedData: undefined,

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
            index2View: state => state.index2View,
            rawStatistics: state=>state.rawStatistics
        }),
        subspaceSelected(){
            let totalLength = d3.sum(Object.values(this.subspaceFeatureMap), l=>l.length)
            console.log('total length', totalLength)
            if(totalLength == 0){
                return false
            }else{
                return true
            }
        },
        breakdownSelected(){
            if(this.selectBreakdown == 0){
                return false
            }else{
                return true
            }
        }
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
        subspaceStatistics(){
            console.log('For feature', Object.values(this.subspaceFeatureMap))
            return undefined
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
        },
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
