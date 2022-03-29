<template>
  <div class="search">
    <div class="banner">
      <div class="input-box">
        <a-input-search
          v-model:model-value="movieName"
          class="search-input" placeholder="搜电影"
          allow-clear @search="handleSearchMovie"
          size="large"
          @press-enter="handleSearchMovie"
        />
      </div>
    </div>
    <div class="result">
      <div class="movie-cards">
        <a-space wrap size="large">
          <MovieCard v-for="item in movies" :key="item.pk" :item="item"/>
        </a-space>
      </div>
    </div>
  </div>
</template>

<script>
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import {get} from "@/utils/request";

import MovieCard from "@/components/MovieCard";

export default {
  name: "SearchView",
  components: {
    MovieCard
  },
  setup() {
    const route = useRoute()
    const movieName = ref('')
    const movies = ref([])
    const handleSearchMovie = () => {
      movieName.value = movieName.value.trim()
      if (movieName.value.length > 0 ) {
        get('/api/search_movie', { movieName: movieName.value}).then(res => {
          movies.value = res.movies
          console.log(res, movies)
        })
      }
    }
    onMounted(async () => {
      movieName.value = route.params.movieName
      if ( movieName.value ) {
        await handleSearchMovie()
      }
    })
    return {
      movieName,
      movies,
      handleSearchMovie
    }
  }
}
</script>

<style lang="scss" scoped>
.banner {
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #47464a;
  .input-box {
    width: 540px;
    margin: 24px auto 16px;
    padding-bottom: 24px;
    border-bottom: 10px solid rgb(var(--red-5));
    .search-input {
      padding: 4px;
    }
  }
}
.result {
  width: 1100px;
  margin: 0 auto;
}
</style>