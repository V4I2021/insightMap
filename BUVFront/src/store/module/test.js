import {dataService} from '@/service';

// initial state
const state = () => ({
  counter: 0,
  data: undefined
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
  fetchData({commit}) {
    dataService.fetchData({commit}, resp => {
      commit('updateData', resp)
    })
  }
}

// mutations
const mutations = {
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
  }
}


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
