<template>
  <div class="navbar">
    <div class="navbar-box">
      <a-menu class="menu" mode="horizontal" v-model:selected-keys="selected" @menu-item-click="changePage">
        <a-menu-item disabled key="0" :style="{padding: '10px', marginRight: '28px' }">
          <img class="logo" alt="Vue logo" src="@/assets/logo1.png" @click="()=>changePage('home')">
        </a-menu-item>
        <a-menu-item key="home">主页</a-menu-item>
        <a-menu-item key="recommend">推荐</a-menu-item>
        <a-menu-item key="explore">探索</a-menu-item>
        <a-menu-item key="about">关于</a-menu-item>
      </a-menu>
    </div>
    <div class="search-box">
      <a-input-search
        v-model:model-value="movieName"
        class="search-input"
        placeholder="搜电影"
        allow-clear
        @search="handleSearchMovie"
        @press-enter="handleSearchMovie"
      >
      </a-input-search>
    </div>
    <div class="user-box" @click="isLogin?changePage('user'):changePage('account')">
      <div class="go-login" v-if="!isLogin">
        登陆/注册
      </div>
      <div class="go-user" v-else>
        <a-avatar :size="48">
          <img
            alt="avatar"
            :src="user_avatar"
          />
        </a-avatar>
      </div>
    </div>
  </div>
</template>

<script>
import { get } from "@/utils/request"
import { useStore } from 'vuex'
import { link } from "@/utils/link";
import {computed, onMounted, ref} from "vue"

export default {
  name: "NavBar",
  setup() {
    const store = useStore()
    const selected = computed(()=>{
      return [store.state.rootPath]
    })
    const isLogin = computed(()=>{
      return store.state.loginStatus
    })
    const user_avatar = computed(() => {
      return store.state.userInfo.avatar
    })
    const changePage = (key) => {
      link('/'+key, key)
    }
    const movieName = ref('')
    const handleSearchMovie = () => {
      // get('/api/search_movie', { movieName: movieName.value}).then(res => {
      //   console.log(res)
      // })
      link(`/search/${movieName.value}`, 'search',{ movieName: movieName.value })
      movieName.value = ''
    }
    onMounted(()=>{
      get('/api/login_info').then(res => {
        if (res.login) {
          store.commit('changeLoginStatus', {status: true})
          store.commit('changeUser', { username: res.username, avatar: res.avatar})
        }
      })
    })
    return {
      selected,
      isLogin,
      user_avatar,
      movieName,
      changePage,
      handleSearchMovie,
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  .navbar-box {
    flex-grow: 1;
    text-align: left;
    .logo {
      width: 160px;
      height: 40px;
      cursor: default;
    }
    .menu {
      font-size: 16px;
    }
  }
  .search-box {
    height: 40px;
    .search-input {
      height: 100%;
    }
  }
  .user-box {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 14px 20px;
    width: 70px;
    height: 70px;
    background-color: var(--color-menu-light-bg);
    cursor: pointer;
    .go-login {
      a {
        color: var(--color-text-2);
      }
    }
  }
}
</style>