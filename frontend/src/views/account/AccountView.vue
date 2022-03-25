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
            <a-input-password v-model="regForm.password_1" placeholder="密码"/>
          </a-form-item>
          <a-form-item field="password_2" label="重复密码">
            <a-input-password v-model="regForm.password_2" placeholder="重复密码"/>
          </a-form-item>
          <a-form-item>
            <div class="switch" @click="switchMode">已有账号？去登录</div>
          </a-form-item>
          <a-form-item>
            <a-button type="primary" long html-type="submit">注册并登录</a-button>
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
import {link} from "@/utils/link";
import {useStore} from "vuex";
import {reactive, ref} from "vue";

export default {
  name: "AccountView",
  data() {
    return {
      images: [
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
      ],
    }
  },
  setup() {
    const contentType = ref('content-login')
    const showLoginError = ref(false)
    const showRegError = ref(false)
    const errorMsg = ref('')
    const loginForm = reactive({
        username: '',
        password: '',
        isStay: false,
    })
    const regForm = reactive({
        username: '',
        password_1: '',
        password_2: '',
    })
    const store = useStore()
    const handleChangeStatus = async (res) => {
      store.commit('changeLoginStatus', {status: true})
      store.commit('changeUser', { username: res.username, avatar: res.avatar})
      await link('/', 'home')
    }
    const handleLoginSubmit = async (data) => {
      console.log(data.values)
      const res = await post('/api/login',data.values)
      if ( !res.error ) await handleChangeStatus(res)
      else {
        errorMsg.value = res.msg
        showLoginError.value = true
      }
      console.log(res)
    }
    const handleRegSubmit = async (data) => {
      console.log(data.values)
      const res = await post('/api/register',data.values)
      if ( !res.error ) {
        contentType.value = 'content-login'
        await handleChangeStatus(res)
      }
      else {
        errorMsg.value = res.msg
        showRegError.value = true
      }
      console.log(res)
    }
    const switchMode = () => {
      console.log(errorMsg)
      if(contentType.value == 'content-login') {
        contentType.value = 'content-reg'
      } else contentType.value = 'content-login'
    }
    return {
      handleLoginSubmit,
      handleRegSubmit,
      switchMode,
      errorMsg,
      showRegError,
      showLoginError,
      contentType,
      loginForm,
      regForm
    }
  }
}
</script>

<style lang="scss" scoped>
.content-box {
  margin: auto;
  width: 830px;
  border-radius: var(--border-radius-medium);
  overflow: hidden;
  box-shadow: 4px 6px 20px -4px rgb(var(--primary-9));
  .content {
    height: 600px;
    width: 1360px;
    display: flex;
    flex-direction: row;
    transition: all .8s ease ;
    &-login {
      transform: translateX(-530px);
    }
    &-reg {
      transform: translateX(0);
    }
    .login-box,.reg-box {
      margin: 20px;
      padding: 0 20px;
      flex-grow: 1;
      flex-basis: 0;
      .title {
        padding-bottom: 16px;
      }
      .switch {
        cursor: pointer;
      }
    }
    .login-box {
      .tools-box {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      }
    }
    .reg-box {
      .switch {
        width: 100%;
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
  }
}
</style>