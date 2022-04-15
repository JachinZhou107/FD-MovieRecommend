<template>
  <div class="tag-selector">
    <div class="tag-class">
      {{ tagTypeName }}：
    </div>
    <div class="tag-list">
      <a-radio-group v-model:model-value="select" @change="handleChangeTag">
        <a-radio :value="0">全部</a-radio>
        <a-radio v-for="(item,index) in tagList" :key="index" :value="index+1">{{ item }}</a-radio>
      </a-radio-group>
    </div>
  </div>
</template>

<script>
import {onMounted, ref} from "vue";

export default {
  name: "TagSelector",
  props: ['selected','tagTypeName','tagList','changeTag'],
  setup(props) {
    const handleChangeTag = (val) => {
      props.changeTag(val)
    }
    const select = ref(0)
    onMounted(() => {
      select.value = Number(props.selected) || 0
      console.log('TagSelector'+props.tagTypeName, props.selected, select)
    })
    return {
      select,
      handleChangeTag
    }
  }
}
</script>

<style lang="scss" scoped>
.tag-selector {
  margin: 10px 0;
  display: flex;
  align-items: center;
  .tag-class {
    min-width: 42px;
  }
}
</style>