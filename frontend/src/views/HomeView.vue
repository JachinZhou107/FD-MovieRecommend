<template>
  <nav>
    <router-link to="/about">About</router-link>
  </nav>
  <div class="home">
    <a-avatar>
      <img alt="Vue logo" src="../assets/logo.png">
    </a-avatar>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
