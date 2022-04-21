<template>
  <a-list class="list-box" hoverable :loading="loading">
    <template #header>
      我的评价
    </template>
    <a-list-item v-for="(item) in data" :key="item.pk">
      <template #actions>
        <icon-pen style="padding-left: 24px" size="20" @click="handleEditRating(item.movie.movieId)"/>
      </template>
      <a-list-item-meta>
        <template #avatar>
          <div class="img-box">
            <a-image alt="无图片" width="70" height="100" :preview="false"
                     :src="item.movie.moviePoster" referrerPolicy="no-referrer">
            </a-image>
          </div>
        </template>
        <template #title>
          <div class="title-box">
            {{`${item.movie.movieTitle} ${item.movie.movieName}`}}
          </div>
        </template>
        <template #description>
          <a-rate readonly :default-value="item.fields.rating">
            <template #character>
              <icon-star-fill size="16"/>
            </template>
          </a-rate>
        </template>
      </a-list-item-meta>
    </a-list-item>
  </a-list>
</template>

<script>
import {onMounted, ref} from "vue";
import {useStore} from "vuex";
import {get} from "@/utils/request";
import {useRouter} from "vue-router";

export default {
  name: "UserRatings",
  setup() {
    const store = useStore()
    const router = useRouter()
    const data = ref([])
    const loading = ref(true)
    const handleEditRating = (movieId) => {
      router.push({name: 'films', params: {filmId: movieId}, query: { from: 'user'}})
    }
    onMounted(async ()=>{
      const res = await get('/api/user_ratings', { userId: store.state.userInfo.userId })
      data.value = res['ratings']
      console.log(data)
      loading.value = false
    })
    return {
      data,
      loading,
      handleEditRating
    }
  }
}
</script>

<style lang="scss" scoped>
.list-box {
  text-align: left;
  padding-left: 24px;
  width: 600px;
  .title-box {
    margin-bottom: 10px;
  }
}
</style>