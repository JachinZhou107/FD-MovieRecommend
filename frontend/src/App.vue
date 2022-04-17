<template>
  <a-affix>
    <div class="nav">
      <nav-bar />
    </div>
  </a-affix>

  <div class="wrapper">
    <router-view/>
  </div>
  <div class="footer">

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
  font-family: 'MiSans-Normal', Avenir, Helvetica, Arial, sans-serif;
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
  background-color: var(--color-white);
}
.wrapper {
  min-height: 500px;
}
.footer {
  margin-top: 32px;
  width: 100%;
  min-width: 1240px;
  height: 200px;
  background-color: var(--color-neutral-8);
}
</style>