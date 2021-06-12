import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$axios = axios

axios.interceptors.request.use(res => {
  res.headers.common['token'] = sessionStorage.getItem('token')
  return res;
});
