<template>
  <a-card hoverable class="card">
    <template #cover>
      <div class="img-box">
        <img
          :style="{ width: '100%' }"
          alt="dessert"
          :src="item.fields.movie_poster"
        />
      </div>
    </template>
    <a-card-meta :title="item.fields.movie_title">
      <template #description>
        <div class="desc-box">
          上映时间：{{item.fields.movie_time}}<br>
          豆瓣评分：{{item.fields.movie_score || '暂无'}}
        </div>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script>
export default {
  name: "MovieCard",
  props: ['item'],
}
</script>

<style lang="scss" scoped>
.card {
  width: 140px;
  margin: 10px;
  .img-box {
    height: 200px;
    overflow: hidden;
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
  .desc-box {
    text-align: left;
  }
}
</style>