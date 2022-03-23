<template>
  <h1 class="title">乂影电影推荐</h1>
  <a-form :model="form" layout="vertical" :style="{width:'80%', margin: 'auto'}" @submit="handleLoginSubmit">
    <a-form-item field="username" label="用户名">
      <a-input v-model="form.username" placeholder="用户名" />
    </a-form-item>
    <a-form-item field="password" label="密码">
      <a-input-password v-model="form.password" placeholder="密码" allow-clear/>
    </a-form-item>
    <a-form-item field="isStay">
      <div class="tools-box">
        <a-checkbox v-model="form.isStay">
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
</template>

<script>
import {post} from "@/utils/request";
import router from "@/router";

export default {
  name: "LoginView",
  data() {
    return {
      form: {
        username: '',
        password: '',
        isStay: false,
      },
      showError: false,
      errorMsg: ''
    }
  },
  methods:{
    async handleSubmit(data) {
      console.log(data.values)
      const res = await post('/api/login',data.values)
      if ( !res.error ) await router.push('/')
      else {
        this.showError = true
        this.errorMsg = res.msg
      }
      console.log(res)
    }
  }
}
</script>

<style scoped>
.login-box {
  margin: auto;
  width: 80%;
  height: 500px;
  border: 1px solid #2c3e50;
}
</style>