<template>
  <div class="content-box">
    <div class="content" :class="contentType">
      <div class="reg-box">
        <h1 class="title">乂影电影推荐</h1>
        <a-form :model="regForm" layout="vertical" :style="{width:'80%', margin: 'auto'}" @submit="handleRegSubmit">
          <a-form-item field="username" label="用户名">
            <a-input v-model="regForm.username" placeholder="用户名" />
          </a-form-item>
          <a-form-item field="password_1" label="密码">
            <a-input v-model="regForm.password_1" placeholder="密码" />
          </a-form-item>
          <a-form-item field="password_2" label="重复密码">
            <a-input v-model="regForm.password_2" placeholder="重复密码" />
          </a-form-item>
          <a-form-item>
            <div class="switch" @click="switchMode">已有账号？去登录</div>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" long html-type="submit">注册</a-button>
          </a-form-item>
          <a-form-item>
            <a-alert v-if="showRegError" type="error">{{errorMsg}}</a-alert>
          </a-form-item>
        </a-form>
      </div>
      <div class="images-box">
        <a-carousel
            :style="{
              height: '100%',
              width: '100%'
            }"
            :default-current="2"
            indicator-position="inner"
            autoPlay
          >
            <a-carousel-item v-for="(image,index) in images" :key="index" style="height: 100%">
              <img :src="image" />
            </a-carousel-item>
          </a-carousel>
      </div>
      <div class="login-box">
        <h1 class="title">乂影电影推荐</h1>
        <a-form :model="loginForm" layout="vertical" :style="{width:'80%', margin: 'auto'}" @submit="handleLoginSubmit">
          <a-form-item field="username" label="用户名">
            <a-input v-model="loginForm.username" placeholder="用户名" />
          </a-form-item>
          <a-form-item field="password" label="密码">
            <a-input-password v-model="loginForm.password" placeholder="密码" allow-clear/>
          </a-form-item>
          <a-form-item field="isStay">
            <div class="tools-box">
              <a-checkbox v-model="loginForm.isStay">
                记住我
              </a-checkbox>
              <div class="switch" @click="switchMode">没有账号？去注册</div>
            </div>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" long html-type="submit">登录</a-button>
          </a-form-item>
          <a-form-item>
            <a-alert v-if="showLoginError" type="error">{{errorMsg}}</a-alert>
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script>
import {post} from "@/utils/request";
import router from "@/router";

export default {
  name: "LoginView",
  data() {
    return {
      contentType: 'content-login',
      loginForm: {
        username: '',
        password: '',
        isStay: false,
      },
      regForm: {
        username: '',
        password_1: '',
        password_2: '',
      },
      showLoginError: false,
      showRegError: false,
      errorMsg: '',
      images: [
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
      ],
    }
  },
  methods:{
    async handleLoginSubmit(data) {
      console.log(data.values)
      const res = await post('/api/login',data.values)
      if ( !res.error ) await router.push('/')
      else {
        this.errorMsg = res.msg
        this.showLoginError = true
      }
      console.log(res)
    },
    async handleRegSubmit(data) {
      console.log(data.values)
      const res = await post('/api/register',data.values)
      if ( !res.error ) this.contentType = 'content-login'
      else {
        this.errorMsg = res.msg
        this.showRegError = true
      }
      console.log(res)
    },
    switchMode() {
      if(this.contentType==='content-login') {
        this.contentType = 'content-reg'
      } else this.contentType = 'content-login'
    }
  }
}
</script>

<style lang="scss" scoped>
.content-box {
  margin: auto;
  width: 800px;
  border: white 1px solid;
  overflow: hidden;
  .content {
    height: 500px;
    width: 1360px;
    display: flex;
    flex-direction: row;
    transition: all .8s ease ;
    &-login {
      transform: translateX(-490px);
    }
    &-reg {
      transform: translateX(0);
    }
    .reg-box {
      margin: 20px;
      padding-left: 20px;
      padding-right: 20px;
      flex-grow: 1;
      .title {
        padding-bottom: 16px;
      }
      .switch {
        cursor: pointer;
      }
    }
    .images-box {
      width: 300px;
      height: 100%;
      img {
        height: 100%;
        width: 100%;
        object-fit: cover;
        object-position: center center;
      }
    }
    .login-box {
      margin: 20px;
      padding-right: 20px;
      padding-left: 20px;
      flex-grow: 1;
      .title {
        padding-bottom: 16px;
      }
      .tools-box {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        .switch {
          cursor: pointer;
        }
      }
    }
  }
}
</style>