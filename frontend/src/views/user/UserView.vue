<template>
    <a-form :model="form" :style="{width:'600px'}" @submit="handleSubmit">
    <a-form-item field="username" label="用户名">
      <a-input v-model="username" placeholder="用户名" disabled/>
    </a-form-item>
    <a-form-item>
      <a-button html-type="submit">退出登录</a-button>
    </a-form-item>
  </a-form>
</template>

<script>
import {get} from "@/utils/request";
import router from "@/router";

export default {
  name: "UserView",
  data() {
    return {
      username: '',
    }
  },
  mounted() {
    get('/api/login_info').then(res => {
      this.username = res.username
    })
  },
  methods:{
    async handleSubmit() {
      const res = await get('/api/logout')
      await router.push('/')
      console.log(res)
    }
  }
}
</script>

<style scoped>

</style>