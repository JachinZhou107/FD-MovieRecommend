<template>
  <div class="film">
    <div class="banner">
      <div class="info">
        <div class="movie-title">
          <span>{{ movieInfo.fields?.movie_title }}</span>
        </div>
        <div class="movie-poster">
          <a-image
              :src="movieInfo.fields?.movie_poster"
              :width="240"
              :height="330"
              referrerPolicy="no-referrer"
          ></a-image>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {useRoute} from "vue-router";
import {onMounted, reactive} from "vue";
import {get} from "@/utils/request";

export default {
  name: "FilmsView",
  setup() {
    const route = useRoute()
    let movieInfo = reactive({
      fields: {},
      movieId: ''
    })
    onMounted(()=>{
      get('/api/get_movie', { movieId: route.params.filmId }).then(res => {
        movieInfo.fields = res.movie.fields
        movieInfo.fields.movie_title = movieInfo.fields.movie_title.replace(/.*《/g,'').replace(/》.*/g,'')
        movieInfo.movieId = res.movie.pk
        console.log(movieInfo)
      })
    })
    return {
      movieInfo
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
        padding-bottom: 16px;
      }
      .movie-poster {
        width: 240px;
        height: 330px;
        border: solid 2px var(--color-white);
      }
    }
  }
}
</style>