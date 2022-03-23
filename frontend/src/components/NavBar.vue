<template>
  <div class="navbar">
    <div class="navbarBox">
      <a-menu mode="horizontal" :default-selected-keys="[select]" @menu-item-click="changePage">
        <a-menu-item disabled key="0" :style="{padding: '10px', marginRight: '28px' }">
          <img class="logo" alt="Vue logo" src="@/assets/logo1.png">
        </a-menu-item>
        <a-menu-item key="home">主页</a-menu-item>
        <a-menu-item key="recommend">推荐</a-menu-item>
        <a-menu-item key="explore">探索</a-menu-item>
        <a-menu-item key="about">关于</a-menu-item>
      </a-menu>
    </div>
    <div class="userBox">
      <a-avatar :size="48">
        <img
          alt="avatar"
          src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
        />
      </a-avatar>
    </div>
  </div>
</template>

<script>
import router from "@/router";

export default {
  name: "NavBar",
  props: {
    selected: {
      type: Array,
      default: ()=>{
        return []
      },
    }
  },
  data() {
    return {
      select: 'home',
    }
  },
  methods: {
    changePage(key) {
      router.push('/'+key);
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  .navbarBox {
    flex-grow: 1;
    text-align: left;
    .logo {
      width: 160px;
      height: 40px;
      cursor: default;
    }
  }
  .userBox {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 14px 20px;
    width: 70px;
    height: 70px;
    background-color: white;
  }
}
</style>