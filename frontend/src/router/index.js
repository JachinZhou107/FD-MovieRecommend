import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/home/HomeView.vue'
import {get} from "@/utils/request";

const routes = [
  {
    path: '',
    redirect: '/home',
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/about/AboutView.vue')
  },
  {
    path: '/account',
    name: 'account',
    component: () => import(/* webpackChunkName: "account" */ '../views/account/AccountView.vue')
  },
  {
    path: '/user',
    name: 'user',
    component: () => import(/* webpackChunkName: "user" */ '../views/user/UserView.vue')
  },
  {
    path: '/films/:filmId?',
    name: 'films',
    component: () => import(/* webpackChunkName: "films" */ '../views/films/FilmsView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "NotFound" */ '../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async(to, from, next) => {
  if ( to.name === 'account' ) {
    let isLogin = await get('/api/login_info');
    if ( isLogin.login ) {
      next({name: 'home'})
    } else next()
  } else if ( to.name === 'user' ) {
    let isLogin = await get('/api/login_info');
    if ( isLogin.login ) {
      next()
    } else next({name: 'account'})
  }
  else next()
})

export default router
