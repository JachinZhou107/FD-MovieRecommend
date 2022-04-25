<template>
  <a-list class="list-box" hoverable :loading="loading">
    <template #header>
      我的评价
    </template>
    <a-list-item v-for="(item) in data" :key="item.pk">
      <template #actions>
        <icon-edit style="padding-left: 24px" size="20" @click="handleEditRating(item.movie.movieId)"/>
        <a-popconfirm content="确定删除这条评论?" position="right" :ok-button-props="{status: 'danger'}"
                      :on-before-ok="()=>handleDeleteRating(item.pk)?true:false" :on-before-cancel="handleCloseDeleting">
          <icon-delete style="padding-left: 24px" size="20" />
        </a-popconfirm>

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
          <router-link :to="{ name: 'films', params: { filmId: item.movie.movieId } }" class="title-box">
            {{`${item.movie.movieTitle} ${item.movie.movieName}`}}
          </router-link>
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
    let deleteDone = true
    const handleDeleteRating = async (ratingId) => {
      deleteDone = false
      const res = await get('/api/delete_rating', {userId: store.state.userInfo.userId, ratingId})
      if ( res.error == 0 ) {
        deleteDone = true
        const res = await get('/api/user_ratings', { userId: store.state.userInfo.userId })
        data.value = res['ratings']
      }
      return deleteDone
    }
    const handleCloseDeleting = () => deleteDone
    onMounted(async ()=>{
      loading.value = true
      const res = await get('/api/user_ratings', { userId: store.state.userInfo.userId })
      data.value = res['ratings']
      loading.value = false
    })
    return {
      data,
      loading,
      handleEditRating,
      handleDeleteRating,
      handleCloseDeleting
    }
  }
}
</script>

<style lang="scss" scoped>
.list-box {
  text-align: left;
  padding-left: 24px;
  width: 660px;
  .title-box {
    display: inline-block;
    margin-bottom: 10px;
    text-decoration-line: none;
    font-size: 16px;
  }
}
</style>