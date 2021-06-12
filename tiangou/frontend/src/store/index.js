import Vue from 'vue'
import Vuex from 'vuex'

// import example from './module-example'

Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    state: {
      loggedIn: false,
      username: '',
      userid: -1,
      isAdmin: false,
      order_count: 0,
      cart_count: 0,
      token: ''
    },
    mutations: {
      login(state, payload) {
        state.loggedIn = true
        state.username = payload.name
        state.userid = payload.id
        state.isAdmin = payload.isAdmin
        state.order_count = payload.order_count,
        state.cart_count = payload.cart_count,
        state.token = payload.token
        sessionStorage.setItem('token', state.token)
      },
      logout(state) {
        state.loggedIn = false
        state.username = ''
        state.userid = -1
        state.isAdmin = false
        state.order_count = 0
        state.cart_count = 0
        state.token = ''
        sessionStorage.setItem('token', state.token)

      },
      updateCount(state, payload) {
        state.order_count = payload.order
        state.cart_count = payload.cart
      }
    },
    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEBUGGING
  })

  return Store
}
