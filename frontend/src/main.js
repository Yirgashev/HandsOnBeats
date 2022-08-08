import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import store from './store'
import { createRouter, createWebHashHistory } from 'vue-router'
import {post,get} from "/src/utils/http.js";
// import Axios from 'axios'
// import Vue from 'vue'


// 把axios挂载到vue的原型中，在vue中每个组件都可以使用axios发送请求,
// 不需要每次都 import一下 axios了，直接使用 $axios 即可
// Vue.prototype.$axios = Axios

// Axios.defaults.baseURL = '/api'

// 1. Define route components.
// These can be imported from other files
const Home = { template: '<div>Home</div>' }
// const About = { template: '<div>About</div>' }

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  { path: '/', component: Home },
  // { path: '/about', component: About },
]

// 3. Create the router instance and pass the `routes` option
const router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
})

// 5. Create and mount the root instance.
const app = createApp(App)
// Make sure to _use_ the router instance to make the
// whole app router-aware.
app.use(router).use(store)
app.mount('#app')
