// src/store/index.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    selectedPrjId: 0,
    selectedPrjName:''
  },
  mutations: {
    setSelectedPrjId(state, id) {
      state.selectedPrjId = id;
    },
    setSelectedPrjName(state,name){
        state.selectedPrjName = name;
    }
  },
  actions: {
    updateSelectedPrjId({ commit }, id) {
      commit('setSelectedPrjId', id);
    },
    updateSelectedPrjName({ commit }, name) {
      commit('setSelectedPrjName', name);
    }
  },
  getters: {
    getSelectedPrjId: state => state.selectedPrjId,
    getSelectedPrjName: state => state.selectedPrjName
  }
});