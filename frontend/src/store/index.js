import { createStore } from 'vuex'

export default createStore({
  state: {
    rootPath: '',
    loginStatus: false,
    userInfo: {
      username: '',
      avatar: '',
      userId: ''
    }
  },
  getters: {
  },
  mutations: {
    changeChooseNavbar(state, path) {
      state.rootPath = path
      console.log(state.rootPath)
    },
    changeLoginStatus(state, payload) {
      state.loginStatus = payload.status
    },
    changeUser(state, payload) {
      state.userInfo = {...payload}
    }
  },
  actions: {
  },
  modules: {
  }
})
