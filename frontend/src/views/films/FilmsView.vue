<template>
  <div class="film">
    <div class="banner">
      <div class="info">
        <div class="movie-poster">
          <a-image
              :src="movieInfo.fields?.movie_poster"
              :width="226"
              :height="330"
              referrerPolicy="no-referrer"
          ></a-image>
        </div>
        <h1 class="movie-title">
          <span>{{ movieInfo.fields?.movie_title }}</span>
        </h1>
        <div class="movie-details">
          <div class="movie-brief">
            <div class="movie-brief-field movie-name">
              <span>译名 / 别名：</span><span :title="movieInfo.fields?.movie_name">{{movieInfo.fields?.movie_name}}</span>
            </div>
            <div class="movie-brief-field">
              {{movieInfo.fields?.movie_time}} {{movieInfo.fields?.movie_contry}}
            </div>
            <div class="movie-brief-field">
              {{movieInfo.fields?.movie_length}} {{movieInfo.fields?.movie_type}}
            </div>
            <div class="movie-brief-field movie-director">
              <span>导演：</span><span>{{movieInfo.fields?.movie_director}}</span>
            </div>
            <div class="movie-brief-field movie-actors">
              <div>主演 / 演员：</div><span :title="movieInfo.fields?.movie_actors">{{movieInfo.fields?.movie_actors}}</span>
            </div>
          </div>
          <div class="movie-score">
            <div class="score-number">
              <a-statistic title="豆瓣评分" :value="movieScore*2" :precision="1" style="color: white" />
            </div>
            <div class="score-star">
              <div>{{ movieScoreCount }}人评分</div>
              <a-rate :count="5" v-model:model-value="movieScore" readonly allow-half>
              </a-rate>
            </div>
            <div class="add-score">
              <a-button status="danger" size="large">去评分</a-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="content-container">
      <div class="content">
        <div class="movie-desc">
          <div class="title">
            <h2>剧情简介</h2>
          </div>
          <div class="main">
            <p>{{ movieInfo.fields.movie_desc }}</p>
          </div>
        </div>
        <div class="movie-comment">
          <div class="title">
            <h2>电影评价</h2>
          </div>
          <div class="main">
            <CommentSection/>
            <a-divider />
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
  </div>
</template>

<script>
import {useRoute} from "vue-router";
import {onMounted, reactive, ref} from "vue";
import {get} from "@/utils/request";

import CommentSection from '@/components/CommentSection.vue'

export default {
  name: "FilmsView",
  components: {
    CommentSection,
  },
  setup() {
    const route = useRoute()
    const movieInfo = reactive({
      fields: {},
      movieId: ''
    })
    const movieScore = ref(0)
    const movieScoreCount = ref(0)
    onMounted(()=>{
      get('/api/get_movie', { movieId: route.params.filmId }).then(res => {
        movieInfo.fields = res.movie.fields
        movieInfo.fields.movie_title = movieInfo.fields.movie_title.replace(/.*《/g,'').replace(/》.*/g,'')
        movieInfo.movieId = res.movie.pk
        movieScore.value = Number(movieInfo.fields.movie_score.replace(/\/.*/g,''))/2
        movieScoreCount.value = Number(movieInfo.fields.movie_score.replace(/.*from/g,'').replace(/users.*/g,''))
        console.log(movieInfo,movieScoreCount)
      })
    })
    return {
      movieInfo,
      movieScore,
      movieScoreCount
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
          width: 500px;
          height: 200px;
          &-field {
            margin: 12px;
          }
          .movie-name {
            font-size: 18px;
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
            -webkit-line-clamp: 3;
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