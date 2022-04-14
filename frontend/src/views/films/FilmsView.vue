<template>
  <div class="film">
    <div class="banner">
      <a-spin :loading="loading" dot style="width: 100%">
        <div class="info">
          <div class="movie-poster">
            <a-image
                :src="movieInfo.fields?.movie_poster"
                :width="226"
                :height="330"
                referrerPolicy="no-referrer"
            >
              <template #error-icon>
                <icon-live-broadcast />
              </template>
              <template #loader>
                <icon-loading :size="24" :style="{height: '100%'}"/>
              </template>
            </a-image>
          </div>
          <h1 class="movie-title">
            <span>{{ movieInfo.fields?.movie_title }} {{ movieInfo.fields?.movie_name }}</span>
          </h1>
          <div class="movie-details">
            <div class="movie-brief">
              <div class="movie-brief-field movie-name" v-if="movieInfo.fields?.movie_other_name">
                <span>别名：</span><span :title="movieInfo.fields?.movie_other_name">{{movieInfo.fields?.movie_other_name}}</span>
              </div>
              <div class="movie-brief-field">
                {{movieInfo.fields?.movie_time}} {{movieInfo.fields?.movie_country}}
              </div>
              <div class="movie-brief-field">
                {{movieInfo.fields?.movie_length}} {{movieInfo.fields?.movie_type}}
              </div>
              <div class="movie-brief-field movie-director" v-if="movieInfo.fields?.movie_director">
                <span>导演：</span><span>{{movieInfo.fields?.movie_director}}</span>
              </div>
              <div class="movie-brief-field movie-actors" v-if="movieInfo.fields?.movie_actors">
                <div>主演 / 演员：</div><span :title="movieInfo.fields?.movie_actors">{{movieInfo.fields?.movie_actors}}</span>
              </div>
            </div>
            <div class="movie-score">
              <div class="score-number">
                <a-statistic title="豆瓣评分" :value="movieScore*2" :precision="1" style="color: white" />
              </div>
              <div class="score-star">
                <div>{{ movieScoreCount }}</div>
                <a-rate :count="5" v-model:model-value="movieScore" readonly allow-half>
                </a-rate>
              </div>
              <div class="add-score">
                <a-button status="danger" size="large" @click="handleOpenRating">去评分</a-button>
              </div>
            </div>
          </div>
        </div>
      </a-spin>
    </div>
    <div class="content-container" v-show="!loading">
      <div class="content">
        <div class="movie-desc">
          <div class="title">
            <h2>剧情简介</h2>
          </div>
          <div class="main">
            <p v-for="(item,index) in movieInfo.fields.movie_desc" :key="index">{{ item.trim() }}</p>
          </div>
        </div>
        <div class="movie-comment">
          <div class="title">
            <h2>电影评价</h2>
          </div>
          <div class="main">
            <template v-for="item in movieRaingList" :key="item.pk">
              <CommentSection :item="item"/>
              <a-divider />
            </template>
          </div>
        </div>
      </div>
      <div class="sider">
        <div class="similar">
          <div class="title">
            <h2>同类电影</h2>
          </div>
        </div>
      </div>
    </div>
    <a-modal
        v-model:visible="error"
        ok-text="回到上一页"
        hide-cancel
        :closable="false"
        :mask-closable="false"
        @ok="handleGoBack"
    >
      <template #title>
        提示
      </template>
      <div>{{ errorMsg }}</div>
    </a-modal>
    <a-modal
        v-model:visible="rating"
        ok-text="提交评价"
        @ok="handleSubmitRating"
    >
      <template #title>
        写短评
      </template>
      <div style="width: 100%; text-align: center">
        <a-rate allow-half v-model:model-value="ratingNum"/>
      </div>
      <a-textarea
          v-model:model-value="comments"
          placeholder="说说你的看法吧"
          allow-clear show-word-limit
          :max-length="180"
          :auto-size="{
            minRows:3,
            maxRows:5
          }"
          style="margin-top: 20px"
      />
    </a-modal>
  </div>
</template>

<script>
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted, reactive, ref} from "vue";
import {get, post} from "@/utils/request";

import CommentSection from '@/components/CommentSection.vue'
import {useStore} from "vuex";

export default {
  name: "FilmsView",
  components: {
    CommentSection,
  },
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const movieInfo = reactive({
      fields: {},
      movieId: ''
    })
    const movieRaingList = ref([])
    const movieScore = ref(0)
    const movieScoreCount = ref(0)
    const loading = ref(true)
    const error = ref(false)
    const errorMsg = ref('')
    const handleGoBack = () => {
      router.back()
    }
    const rating = ref(false)
    const ratingNum = ref(0)
    const comments = ref('')
    const isLogin = computed(()=>{
      return store.state.loginStatus
    })
    const handleOpenRating = () => {
      if (isLogin.value) rating.value = true
    }
    const handleSubmitRating = async () => {
      const res = await post('/api/deal_movie',
          {
            movieImdbId: movieInfo.fields.movie_imdb_id,
            rating: ratingNum.value,
            comments: comments.value,
            userId: store.state.userInfo.userId
          })
      console.log(res)
      rating.value = false
    }
    onMounted(async ()=>{
      const movie = await get('/api/get_movie', { movieId: route.params.filmId })
      if ( movie.error == '0' ) {
        movieInfo.fields = movie.movie.fields
        movieInfo.movieId = movie.movie.pk
        movieInfo.fields.movie_desc = movieInfo.fields.movie_desc.split('<br>')
        movieScore.value = Number(movieInfo.fields.movie_score)/2
        movieScoreCount.value = movieInfo.fields.movie_score_sum
        console.log(movieInfo,movieScoreCount)
        loading.value = false
      }
      else {
        error.value = true
        errorMsg.value = movie.msg
        loading.value = false
      }
      const movieRatings = await post('/api/get_movie_ratings', { movieImdbId: movieInfo.fields.movie_imdb_id })
      console.log(movieRatings)
      if ( movieRatings.error == '0' )
        movieRaingList.value = movieRatings.list

      if (isLogin.value) {
        const ratingInfo = await post('/api/get_user_rating', {
          movieImdbId: movieInfo.fields.movie_imdb_id,
          userId: store.state.userInfo.userId
        })
        if ( ratingInfo.error == '0' ) {
          ratingNum.value = ratingInfo.rating
          comments.value = ratingInfo.comments
        }
      }

    })
    return {
      movieInfo,
      movieRaingList,
      movieScore,
      movieScoreCount,
      loading,
      error,
      errorMsg,
      handleGoBack,
      rating,
      ratingNum,
      comments,
      handleOpenRating,
      handleSubmitRating,
    }
  }
}
</script>

<style lang="scss" scoped>
.film {
  .banner {
    width: 100%;
    min-width: 1240px;
    background: #392f59 url(https://s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:5788b470/banner_bg.f7fd103e3b8c16b6f449cce43fc57f45.png) no-repeat 50%;
    .info {
      margin: 0 auto;
      padding: 16px 0;
      height: 344px;
      width: 1120px;
      color: var(--color-white);
      .movie-title {
        text-align: left;
        font-size: 26px;
        font-weight: bold;
        margin-left: 260px;
      }
      .movie-poster {
        width: 225px;
        height: 330px;
        border: solid 2px var(--color-white);
        border-radius: 4px;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 4px 4px 14px -4px rgb(var(--primary-9));
        float: left;
      }
      .movie-details {
        margin-left: 270px;
        .movie-brief {
          text-align: left;
          width: 520px;
          height: 200px;
          line-height: 1.4;
          &-field {
            margin: 4px;
          }
          .movie-name {
            font-weight: bold;
            font-size: 17px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 1;
          }
          .movie-director {
            margin-top: 20px;
          }
          .movie-actors {
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 4;
          }
        }
        .movie-score {
          width: 500px;
          height: 70px;
          display: flex;
          align-items: center;
          justify-content: flex-start;
          .score-star {
            height: 60px;
            margin-left: 20px;
            text-align: right;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
          }
          .add-score {
            margin-left: auto;
          }
        }
      }
    }
  }
  .content-container {
    margin: 40px auto 0;
    padding: 0 20px;
    width: 1100px;
    display: flex;
    h2 {
      display: inline-block;
      &::before {
        float: left;
        content: "";
        display: inline-block;
        width: 4px;
        height: 24px;
        margin-right: 6px;
        background-color: rgb(var(--primary-6));
      }
    }
    .title {
      text-align: left;
    }
    .main {
      text-align: left;
      p {
        text-indent: 4em;
        line-height: 1.6;
      }
    }
    .content {
      flex-grow: 1;
      padding-right: 36px;
    }
    .sider {
      width: 360px;
      .similar {
        width: 360px;
      }
    }
  }
}
</style>

<style lang="scss">
.film .movie-score .score-number {
  .arco-statistic-title {
    font-size: 12px;
    color: var(--color-white);
  }
  .arco-statistic-value {
    color: rgb(var(--gold-6));
  }
}
</style>