<template>
  <div class="avatar">
    <UserAvatar></UserAvatar>
  </div>
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
import {useStore} from "vuex";
import {link} from "@/utils/link";

import UserAvatar from "@/views/user/UserAvatar";

export default {
  name: "UserView",
  components: {
    UserAvatar
  },
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
  setup() {
    const store = useStore()
    const handleSubmit = async () => {
      const res = await get('/api/logout')
      console.log(res)
      store.commit('changeLoginStatus', {status: false})
      await link('/', 'home')
    }
    return {
      handleSubmit
    }
  }
}
</script>

<style scoped>

</style>