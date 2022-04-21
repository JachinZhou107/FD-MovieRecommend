<template>
  <div class="user-view">
    <a-affix :offsetTop="160">
      <div class="user-menu">
        <a-menu
          :style="{ width: '200px', borderRadius: '4px' }"
          theme="light"
          mode="pop" showCollapseButton
          @menu-item-click="handleClickMenu"
          v-model:selected-keys="selected"
        >
          <a-menu-item key="0" disabled>
            <div>
              用户中心
            </div>
          </a-menu-item>
          <a-menu-item :key="1">
            <template #icon><icon-user/></template>
            个人信息
          </a-menu-item>
          <a-menu-item :key="2">
            <template #icon><icon-heart/> </template>
            评价管理
          </a-menu-item>
    <!--      <a-menu-item key="2">Menu 3</a-menu-item>-->
        </a-menu>
      </div>
    </a-affix>

    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
import {onMounted, ref} from "vue";
import router from "@/router";
import {useRoute} from "vue-router";


export default {
  name: "UserView",
  setup() {
    const route = useRoute()
    const selected = ref([1])
    const handleClickMenu = async (key) => {
      if (key == 1)
        await router.push('/user/info')
      else await router.push('/user/ratings')
    }
    onMounted(async ()=>{
      if (route.name == 'userInfo')
        selected.value = [1]
      else selected.value = [2]
    })
    return {
      selected,
      handleClickMenu
    }
  }
}
</script>

<style lang="scss" scoped>
.user-view {
  display: flex;
  min-height: 600px;
  min-width: 900px;
  max-width: 1100px;
  margin: 20px auto 0;
}

.user-menu {
  height: 400px;
  padding: 40px 20px;
  .arco-menu {
    width: 180px !important;
    height: 100%;
    box-shadow: 0 0 1px rgba(0, 0, 0, 0.4);
    :deep(.arco-menu-item.arco-menu-disabled) {
      cursor: default;
      color: var(--color-black);
    }
    :deep(.arco-menu-collapse-button) {
      width: 32px;
      height: 32px;
      border-radius: 50%;
    }
    &:not(.arco-menu-collapsed) {
      :deep(.arco-menu-collapse-button) {
        right: 0;
        bottom: 8px;
        transform: translateX(50%);
      }
    }
    &:not(.arco-menu-collapsed)::before {
      content: '';
      position: absolute;
      right: 0;
      bottom: 0;
      width: 48px;
      height: 48px;
      background-color: inherit;
      border-radius: 50%;
      transform: translateX(50%);
      box-shadow: -4px 0 2px var(--color-bg-2), 0 0 1px rgba(0, 0, 0, 0.5);
    }
    &.arco-menu-collapsed {
      width: 48px !important;
      height: auto;
      padding-top: 24px;
      padding-bottom: 138px;
      border-radius: 22px !important;
      :deep(.arco-menu-item.arco-menu-disabled) {
        display: none;
      }
      :deep(.arco-menu-collapse-button) {
        right: 8px;
        bottom: 8px;
      }
    }
  }
}
</style>