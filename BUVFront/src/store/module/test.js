import {dataService} from '@/service';
// import * as d3 from 'd3'
// initial state
const state = () => ({
  counter: 0,
  appID: 'NBA',
  data:{
    full: undefined,
    A: {data: [], loc:[], count: 0},
    B: {data: [], loc:[], count: 0},
    C: {data: [], loc:[], count: 0},
    D: {data: [], loc:[], count: 0}
  },
  subspaceColumns:[],
  measureValues: [],
  fullProjection: [],
  insightTypes: [],
  breakdownCount: [],
  subspaceStatistics: [],
  simMatrix:[],
  topK: 15,
  topIndexList: [],
  selectLinks: [], //[src_index, dst_index]
  index2View: {},
  index2Loc: {},
})

// getters
const getters = {
}

// actions
const actions = {
  updateCounter({ state, commit }) {
    dataService.updateCounter({counter: state.counter}, resp => {
      commit('changeCounter', resp.counter);
    })
  },
  fetchData({commit}, payload) {
    dataService.fetchData(payload, resp => {
      commit('updateData', resp)
    })
  },
  fetchDataByApp({state, commit}, payload) {
    dataService.fetchDataByApp(payload, resp => {
      commit('updateFullData', resp)
      let l = []
      for(let i = 0, ilen = resp.data.length; i< ilen; i++){
        l.push(i)
        state.index2View[i] = 'A'
      }

      commit('setSubViewData', {subViewId: 'A', indexList: l, calc: resp['projection']})
    })
  },
  updateSubViewData({commit}, payload) {
    let l = payload['indexList']
    let subViewId = payload['subviewID']
    commit('setSubViewData', {subViewId: subViewId, indexList: l, calc: true})
  },
}

// mutations
const mutations = {
  updateFullData(state, fullData){
    state.data.full = fullData.data
    state.subspaceColumns = fullData.subspace_columns
    state.measureValues= fullData.measure_values
    state.fullPorjection= fullData.projection
    state.insightTypes = fullData.insight_types
    state.breakdownCount = fullData.breakdown_count
    state.simMatrix = fullData.sim_matrix
    state.simMatrix.forEach((scores)=>{
      let scorePackets = Array.from(scores, (e, i)=>[e, i])
      let _scoreObjs = scorePackets.sort((a, b) => b[0]-a[0])

      state.topIndexList.push(_scoreObjs.splice(0, state.topK))
    })
    let statistics = []
    for(let feature in fullData['subspace_statistics']){
      statistics.push({
        feature: feature,
        values: fullData['subspace_statistics'][feature]
      })
    }

    state.subspaceStatistics = statistics
    // console.log('statistics ', state.subspaceStatistics)
    // console.log('full', fullData)
  },
  changeCounter(state, newCounter) {
    state.counter = newCounter;
  },
  updateData(state, data){
    console.log('data', data)
    data.A_results.forEach(d=>{
      d.lx = 0;
      d.ly = 0;
      d.fill='red'
    })
    state.data = data
  },
  setSubViewData(state, para){
    console.log("Para ", para)
    let newList = []
    let indexList = para['indexList']
    let subViewId = para['subViewId']
    indexList.forEach(index=>{
      newList.push(state.data.full[index])
    })
    state.data[subViewId]['data'] = []
    state.data[subViewId]['data'] = newList
    if(para.calc === true){
      dataService.generateProjectionByApp({appID: state.appID, indexList: indexList}, function(resp){
        state.data[subViewId]['loc'] = resp
        resp.forEach((d,i)=>{
          state.index2Loc[indexList[i]] = d
        })

        state.data[subViewId].count +=1
      })
    }else{
      state.data[subViewId]['loc'] = para.calc
      para.calc.forEach((d,i)=>{
        state.index2Loc[indexList[i]] = d
      })
      state.data[subViewId].count +=1
    }

  },
  selectDot(state, para){
    if(para){
      state.selectLinks = Array.from(state.topIndexList[para], d=>[para, d[1]])
    }else{
      state.selectLinks = []
    }

  }
}


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
