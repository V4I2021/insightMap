import {dataService} from '@/service';

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
  subspaceStatistics: []
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
  fetchDataByApp({commit}, payload) {

    dataService.fetchDataByApp(payload, resp => {
      commit('updateFullData', resp)
      let l = []
      for(let i = 0, ilen = resp.data.length; i< ilen; i++){
        l.push(i)
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
    let statistics = []
    for(let feature in fullData['subspace_statistics']){
      statistics.push({
        feature: feature,
        values: fullData['subspace_statistics'][feature]
      })
    }

    state.subspaceStatistics = statistics
    console.log('statistics ', state.subspaceStatistics)
    console.log('full', fullData)
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
        state.data[subViewId].count +=1
      })
    }else{
      state.data[subViewId]['loc'] = para.calc
      state.data[subViewId].count +=1
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
