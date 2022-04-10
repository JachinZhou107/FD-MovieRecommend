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
      <div class="movie-cards" ref="movie_cards">
        <a-space wrap size="large">
          <MovieCard v-for="item in movies" :key="item.pk" :item="item" :popover="false" />
        </a-space>
      </div>
      <div class="empty-list" v-if="errorCode!='0'||(errorCode=='0'&&totalElements==0)">
        <h3>{{ errorMessage }}</h3>
        <dl v-if="errorCode!==1">
          <dt>本站建议您：</dt>
          <dd>1. 请检查输入的关键词是否有误</dd>
          <dd>2. 尝试搜索电影原名、英文名而不是中文名</dd>
          <dd>或者，亲自来帮本站添加</dd>
        </dl>
      </div>
      <div class="movies-paginator" v-if="totalElements>0">
        <a-pagination
            :total="totalElements"
            :current="pageParams.page"
            :page-size="pageParams.pageSize"
            @change="async (page) => {await changePage(page);scrollIntoMovieCards();}"
            show-total
            show-jumper
        />
      </div>
    </div>
  </div>
</template>

<script>
import {useRoute, useRouter} from "vue-router";
import {onMounted, reactive, ref} from "vue";
import {get} from "@/utils/request";

import MovieCard from "@/components/MovieCard";

export default {
  name: "SearchView",
  components: {
    MovieCard
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const movieName = ref('')
    const movies = ref([])
    const errorMessage = ref('')
    const errorCode = ref(0)
    const pageParams = reactive({
      movieName: '',
      page: 1,
      pageSize: 12,
    })
    const totalElements = ref(0)
    const movie_cards = ref(null)
    const searchMovie = () => {
      movieName.value = movieName.value.trim()
      if (movieName.value.length > 0 ) {
        pageParams.movieName = movieName.value
        get('/api/search_movie', pageParams).then(res => {
          movies.value = res.list
          totalElements.value = res.totalElements || 0
          errorMessage.value = res.error == '1'?res.msg:'很抱歉，没找到相关的影片'
          errorCode.value = Number(res.error)
          console.log(res, movies, errorCode, errorMessage)
        })
      }
      router.replace(`/search/${movieName.value}?page=${pageParams.page}`)
    }
    const handleSearchMovie = () => {
      totalElements.value = 0
      pageParams.page = 1
      searchMovie()
    }
    const scrollIntoMovieCards = () => {
      movie_cards.value.scrollIntoView()
    }
    const changePage = async (page) => {
      pageParams.page = page
      await searchMovie()
    }
    onMounted(async () => {
      movieName.value = route.params.movieName
      pageParams.page = Number(route.query.page)||1
      if ( movieName.value ) {
        await searchMovie()
      }
    })
    return {
      movieName,
      movies,
      errorMessage,
      errorCode,
      pageParams,
      movie_cards,
      totalElements,
      scrollIntoMovieCards,
      changePage,
      handleSearchMovie
    }
  }
}
</script>

<style lang="scss" scoped>
.search {
  min-width: 1240px;
  width: 100%;
}
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
  width: 880px;
  margin: 24px auto 0;
  padding-left: 24px;
  .empty-list  {
    text-align: left;
    h3 {
      margin-top: 64px;
      font-size: 26px;
      color: var(--color-neutral-5);
      font-weight: 400;
    }
    dl {
      dt {
        color: var(--color-danger-light-4);
      }
      dd {
        margin-top: 10px;
        margin-left: 0;
        &:last-child {
          margin-top: 24px;
          text-decoration-line: underline;
          cursor: pointer;
        }
      }
    }
  }
  .movies-paginator {
    width: 100%;
    display: flex;
    justify-content: center;
  }
}
</style>