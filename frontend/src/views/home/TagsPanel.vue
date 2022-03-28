<template>
  <a-collapse class="wrapper">
    <a-collapse-item header="电影筛选" key="1">
      <TagSelector :selected="queries.catId" tag-type-name="类型" :tag-list="tagOfType" :change-tag="(val)=>{handleChangeTag('catId',val)}"/>
      <a-divider />
      <TagSelector :selected="queries.sourceId" tag-type-name="区域" :tag-list="tagOfArea" :change-tag="(val)=>{handleChangeTag('sourceId',val)}"/>
      <a-divider />
      <TagSelector :selected="queries.yearId" tag-type-name="年代" :tag-list="tagOfYear" :change-tag="(val)=>{handleChangeTag('yearId',val)}"/>
    </a-collapse-item>
  </a-collapse>
</template>

<script>
import TagSelector from "@/views/home/TagSelector";

export default {
  name: "TagsPanel",
  components: {
    TagSelector
  },
  props: ['queries', 'changeTag'],
  setup(props) {
    const tagOfYear = '2022 2021 2020 2019 2018 2017 2016 2015 2014 2013 2012 2011 2000-2010 更早'.split(' ')
    const tagOfArea = '大陆 美国 韩国 日本 中国香港 中国台湾 泰国 印度 法国 英国 俄罗斯 意大利 西班牙 德国 波兰 澳大利亚'.split(' ')
    const tagOfType = '爱情 喜剧 动画 剧情 恐怖 惊悚 科幻 动作 悬疑 犯罪 冒险 战争 奇幻 运动 家庭 古装 武侠 西部 历史 传记 歌舞 黑色电影 纪录片 音乐 灾难 青春 儿童'.split(' ')
    const handleChangeTag = (index, value) => {
      props.changeTag({[index]: value, page: 1})
      console.log({[index]: value})
    }
    console.log(props.queries)
    return {
      tagOfType,
      tagOfArea,
      tagOfYear,
      handleChangeTag
    }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  text-align: left;
}
</style>