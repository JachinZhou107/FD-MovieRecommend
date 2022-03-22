<template>
  <a-form :model="form" :style="{width:'600px'}" @submit="handleSubmit">
    <a-form-item field="username" label="用户名">
      <a-input v-model="form.username" placeholder="用户名" />
    </a-form-item>
    <a-form-item field="password_1" label="密码">
      <a-input v-model="form.password_1" placeholder="密码" />
    </a-form-item>
    <a-form-item field="password_2" label="重复密码">
      <a-input v-model="form.password_2" placeholder="重复密码" />
    </a-form-item>
    <a-form-item>
      <a-button html-type="submit">注册</a-button>
    </a-form-item>
  </a-form>
</template>

<script>
import {post} from "@/utils/request";
import router from "@/router";

export default {
  name: "RegisterView",
  data() {
    return {
      form: {
        username: '',
        password_1: '',
        password_2: '',
      }
    }
  },
  methods:{
    async handleSubmit(data) {
      console.log(data.values)
      const res = await post('/api/register',data.values)
      await router.push('/login')
      console.log(res)
    }
  }
}
</script>

<style scoped>

</style>