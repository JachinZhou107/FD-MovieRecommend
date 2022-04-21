<template>
  <div class="recommend">
    <a-card
      class="card" title="和你有相似爱好的用户还喜欢">
      <template #extra>
        <a-link @click="userCFMore=!userCFMore">
          {{userCFMore?'收起':'更多'}}
          <template #icon>
            <icon-up v-if="userCFMore" />
            <icon-down v-else/>
          </template>
        </a-link>
      </template>
      <a-space wrap size="large">
        <MovieCard v-for="item in userCFData.slice(0,5)" :key="item.pk" :item="item">
          <template v-slot:title>
            <span>
              {{item.fields.movie_title || item.fields.movie_name}}
            </span>
          </template>
          <template v-slot:desc>
            <div class="desc-box">
              上映时间：{{item.fields.movie_time || '未知'}}<br>
              豆瓣评分：{{item.fields.movie_score || '暂无'}}
            </div>
          </template>
        </MovieCard>
      </a-space>
      <a-space v-if="userCFMore" wrap size="large">
        <MovieCard v-for="item in userCFData.slice(5)" :key="item.pk" :item="item">
          <template v-slot:title>
            <span>
              {{item.fields.movie_title || item.fields.movie_name}}
            </span>
          </template>
          <template v-slot:desc>
            <div class="desc-box">
              上映时间：{{item.fields.movie_time || '未知'}}<br>
              豆瓣评分：{{item.fields.movie_score || '暂无'}}
            </div>
          </template>
        </MovieCard>
      </a-space>
    </a-card>
    <a-card
      class="card"
      title="Custom hover style"
    >
      <template #extra>
        <a-link>More</a-link>
      </template>
      Card content <br />
      Card content
    </a-card>
  </div>
</template>

<script>
import MovieCard from "@/components/MovieCard";
import {onMounted, ref} from "vue";
import {get} from "@/utils/request";
import {useStore} from "vuex";
export default {
  name: "RecommendView",
  components: {MovieCard},
  setup() {
    const store = useStore()
    const userCFData = ref([])
    const userCFMore = ref(false)
    onMounted(async ()=>{
      const res = await get('/api/recommend', {userId: store.state.userInfo.userId})
      userCFData.value = res.movies
    })
    return {
      userCFData,
      userCFMore
    }
  }
}
</script>

<style lang="scss" scoped>
.recommend {
  margin: 20px auto 0;
  padding: 0 20px;
  max-width: 1200px;
  min-width: 900px;
  display: flex;
  flex-direction: column;
  .card {
    margin-bottom: 24px;
    width: 100%;
  }
}
</style>