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

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.nav {
  width: 100%;
  box-shadow: 0px -10px 20px 0px rgb(var(--primary-9));
}
.wrapper {
  margin: 20px auto 0;
  padding: 0 20px;
  max-width: 1200px;
}
</style>
