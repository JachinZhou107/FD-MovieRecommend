<template>
  <div class="recommend">
    <a-spin :loading="loadingRecommend" dot style="width: 100%">
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
        <a-space wrap size="medium" :class="{'movies-box': true, 'open-box': userCFMore }">
          <template v-for="(item, index) in userCFData" :key="item.pk">
            <MovieCard v-if="index<5||userCFMore"  :item="item">
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
          </template>
        </a-space>
      </a-card>
      <a-card
        class="card" title="和你感兴趣的影片相似的影片有">
        <template #extra>
          <a-link @click="itemCFMore=!itemCFMore">
            {{itemCFMore?'收起':'更多'}}
            <template #icon>
              <icon-up v-if="itemCFMore" />
              <icon-down v-else/>
            </template>
          </a-link>
        </template>
        <a-space wrap size="medium" :class="{'movies-box': true, 'open-box': itemCFMore }">
          <template v-for="(item, index) in itemCFData" :key="item.pk">
            <MovieCard v-if="index<5||itemCFMore"  :item="item">
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
          </template>
        </a-space>
      </a-card>
    </a-spin>
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
    const itemCFData = ref([])
    const itemCFMore = ref(false)
    const loadingRecommend = ref(false)
    onMounted(async ()=>{
      loadingRecommend.value = true
      const res = await get('/api/recommend', {userId: store.state.userInfo.userId})
      userCFData.value = res.moviesUserCF
      itemCFData.value = res.moviesItemCF
      loadingRecommend.value = false
    })
    return {
      userCFData,
      userCFMore,
      itemCFData,
      itemCFMore,
      loadingRecommend
    }
  }
}
</script>

<style lang="scss" scoped>
.recommend {
  margin: 20px auto 0;
  padding: 0 20px;
  width: 1120px;
  display: flex;
  flex-direction: column;
  .card {
    margin-bottom: 24px;
    width: 100%;
    .movies-box {
      margin-left: 0;
      &.open-box {
        margin-left: 22px;
      }
    }
  }
}
@media screen and (max-width: 1160px){
  .recommend {
    width: 900px;
    .card{
       .movies-box {
         margin-left: 20px;
         &.open-box {
           margin-left: 20px;
         }
       }
    }
  }
}
</style>