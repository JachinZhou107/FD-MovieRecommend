<template>
  <a-layout style="height: 800px;">
    <a-layout-header><h3>{{msg}}</h3></a-layout-header>
    <a-layout>
      <a-layout-content>Body</a-layout-content>
      <a-layout-sider>Sider</a-layout-sider>
    </a-layout>
    <a-layout-footer>Footer</a-layout-footer>
  </a-layout>
</template>

<script>

export default {
  name: 'HelloWorld',
  props: [
    'msg'
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
