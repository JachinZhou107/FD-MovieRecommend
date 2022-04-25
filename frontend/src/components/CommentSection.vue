<template>
  <a-comment
    :datetime="getCommentTime(item)"
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
          :src="item.fields.user_avatar"
        />
      </a-avatar>
    </template>
    <template #author>
      <div :style="{display: 'flex', flexDirection: 'column'}">
        <div>{{ item.fields.username }}</div>
        <a-rate :count="5" :default-value="item.fields.rating" allow-half readonly>
          <template #character>
            <icon-star-fill size="16"/>
          </template>
        </a-rate>
      </div>
    </template>
    <template #content>
      <div>
        {{ item.fields.comments }}
      </div>
    </template>
    <slot></slot>
  </a-comment>
</template>

<script>
export default {
  name: "CommentSection",
  props: ['item'],
  setup() {
    const getCommentTime = (item) => {
      const timestamp = new Date(parseInt(item.fields.time_stamp) * 1000);
      return timestamp.toLocaleString().split(' ')[0];
    }
    return {
      getCommentTime,
    }
  }
}
</script>

<style scoped>

</style>