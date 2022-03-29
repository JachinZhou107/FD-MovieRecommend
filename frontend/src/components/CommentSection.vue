<template>
  <a-comment
    datetime="2 天前"
    align="right"
  >
    <template #actions>
      <span class="action" key="heart" @click="onLikeChange">
        <span v-if="like">
          <IconHeartFill :style="{ color: '#f53f3f' }" />
        </span>
        <span v-else>
          <IconHeart />
        </span>
        {{ 83 + (like ? 1 : 0) }}
      </span>
    </template>
    <template #avatar>
      <a-avatar>
        <img
          alt="avatar"
          src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp"
        />
      </a-avatar>
    </template>
    <template #author>
      <div :style="{display: 'flex', flexDirection: 'column'}">
        <div>看啥片儿</div>
        <a-rate :count="5" default-value="4" readonly>
          <template #character>
            <icon-star-fill size="16"/>
          </template>
        </a-rate>
      </div>
    </template>
    <template #content>
      <div>
        《青春变形记》这么好的片子竟然没上院线，真是太遗憾了。将少女成长、中式母女关系与变成红色小熊猫结合，充满了想象力的比喻。整体轻松欢快却也温馨治愈，尤其是最后那一段，原来妈妈也会因担心无法达到她妈妈所期望的“完美”而懊恼，最后美美拉着妈妈一步步变走向姥姥，三代人彼此和解。相信大部分人尤其是女性观众一定感同身受吧。
      </div>
    </template>
    <slot></slot>
  </a-comment>
</template>

<script>
export default {
  name: "CommentSection"
}
</script>

<style scoped>

</style>