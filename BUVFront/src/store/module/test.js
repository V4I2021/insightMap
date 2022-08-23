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
  }
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
      for(let i = 0, ilen = resp.length; i< ilen; i++){
        l.push(i)
      }
      commit('setSubViewData', {subViewId: 'A', indexList: l})
    })
  },
}

// mutations
const mutations = {
  updateFullData(state, fullData){
    state.data.full = fullData
    console.log('state', state, fullData)
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

    let newList = []
    let indexList = para['indexList']
    let subViewId = para['subViewId']
    indexList.forEach(index=>{
      newList.push(state.data.full[index])
    })
    state.data[subViewId]['data'] = []
    state.data[subViewId]['data'] = newList

    dataService.generateProjectionByApp({appID: state.appID, indexList: indexList}, function(resp){
      state.data[subViewId]['loc'] = resp
      state.data[subViewId].count +=1
    })
  }
}


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
