<template>
  <div class="home">
    <a-layout>
      <a-layout-content class="content">
        <a-carousel
          :style="{
            width: '100%',
            height: '240px'
          }"
          :default-current="2"
          animation-name="card"
          auto-play
        >
          <a-carousel-item v-for="(image,index) in images" :key="index" style="width: 60%">
            <img
              :src="image"
              :style="{
                width: '100%',
                height: '240px',
                objectFit: 'cover',
                objectPosition: 'center center'
              }"
            />
          </a-carousel-item>
        </a-carousel>
        <div class="movies-box">
          <div class="tags" id="tags-panel">
            <TagsPanel :changeTag="changePageParams" :queries="queries"/>
          </div>
          <div class="movie-cards" ref="movie_cards">
            <a-space wrap size="large">
              <MovieCard v-for="item in data" :key="item.pk" :item="item"/>
            </a-space>
          </div>
          <div class="movies-paginator">
            <a-pagination
                :total="totalElements"
                :current="pageParams.page"
                :page-size="pageParams.pageSize"
                @change="async (page) => {await changePageParams({page});scrollIntoMovieCards();}"
                show-total
                show-jumper
            />
          </div>
        </div>
      </a-layout-content>
      <a-layout-sider :style="{width: '30%', maxWidth: '300px'}">
        <SiderList></SiderList>
      </a-layout-sider>
    </a-layout>
    <a-layout-footer>
      <a-button @click="handleDealMovie">接口测试</a-button>
    </a-layout-footer>
  </div>
</template>

<script>
import {get} from "@/utils/request";

import SiderList from "@/views/home/SiderList";
import MovieCard from "@/components/MovieCard";
import TagsPanel from "@/views/home/TagsPanel";
import {onMounted, reactive, ref} from "vue";
import {useRoute, useRouter} from "vue-router";

export default {
  name: "HomeView",
  components: {
    SiderList,
    MovieCard,
    TagsPanel
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const queries = route.query
    const images = reactive([
        'http://127.0.0.1:8000/static/poster_1.jpg',
        'http://127.0.0.1:8000/static/poster_2.jpg',
        'http://127.0.0.1:8000/static/poster_3.jpg',
        'http://127.0.0.1:8000/static/poster_4.jpg',
        'http://127.0.0.1:8000/static/poster_5.jpg',
      ])
    const data = ref([])
    const pageParams = reactive({
      page: 1,
      pageSize: 20,
      catId: 0,
      sourceId: 0,
      yearId: 0
    })
    const totalElements = ref(0)
    const movie_cards = ref(null)
    const getMovies = () => {
      get('/api/show_movies', pageParams).then(res =>{
        res.list.forEach((val,index) => {
          let title = res.list[index].fields.movie_title
          let score = res.list[index].fields.movie_score
          res.list[index].fields.movie_title = title.replace(/.*《/g,'').replace(/》.*/g,'')
          res.list[index].fields.movie_score = score.replace(/\/.*/g,'')
        })
        totalElements.value = res.totalElements
        data.value = res.list
      })
    }
    const scrollIntoMovieCards = () => {
      movie_cards.value.scrollIntoView()
    }
    const changePageParams = async (params) => {
      for (const [key, value] of Object.entries(params)) {
        pageParams[key] = Number(value)
        queries[key] = Number(value)
      }
      await router.replace({path: '/home'})
      await router.replace({path: '/home', query: queries})
      await getMovies()
    }
    const handleDealMovie = () => {
      get('/api/deal_movie', {movieName: 'Siccin 3: Cürmü Ask', movieTime: '2016'}).then((res) => {
        console.log(res)
      })
    }
    onMounted(()=>{
      for (const [key, value] of Object.entries(queries)) {
        pageParams[key] = Number(value)
      }
      getMovies()
    })
    return {
      queries,
      images,
      data,
      pageParams,
      movie_cards,
      totalElements,
      scrollIntoMovieCards,
      changePageParams,
      handleDealMovie
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  margin: 20px auto 0;
  padding: 0 20px;
  width: 1200px;
  .content {
    margin-right: 20px;
    overflow: hidden;
  }
  .movies-box {
    text-align: center;
    .tags {
      margin-top: 20px;
    }
    .movie-cards {
      margin-top: 12px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
    }
    .movies-paginator {
      width: 100%;
      display: flex;
      justify-content: center;
    }
  }
}
</style>

