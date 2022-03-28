<template>
  <div class="nav">
    <nav-bar />
  </div>
  <div class="wrapper">
    <router-view/>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar";

export default {
  components: {
    NavBar,
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

<style lang="scss" scoped>
.nav {
  width: 100%;
  min-width: 1240px;
  box-shadow: 0px -10px 20px 0px rgb(var(--primary-9));
}
</style>