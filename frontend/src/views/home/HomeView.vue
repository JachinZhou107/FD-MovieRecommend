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
          @change="log"
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
        <div class="movie-cards">
          <MovieCard v-for="item in data" :key="item.pk" :item="item"/>
        </div>
      </a-layout-content>
      <a-layout-sider :style="{width: '30%', maxWidth: '300px'}">
        <SiderList></SiderList>
      </a-layout-sider>
    </a-layout>
    <a-layout-footer>Footer</a-layout-footer>
  </div>
</template>

<script>
import {get} from "@/utils/request";

import SiderList from "@/views/home/SiderList";
import MovieCard from "@/views/home/MovieCard";

export default {
  name: "HomeView",
  components: {
    SiderList,
    MovieCard
  },
  data() {
    return {
      images: [
        'http://127.0.0.1:8000/static/poster_1.jpg',
        'http://127.0.0.1:8000/static/poster_2.jpg',
        'http://127.0.0.1:8000/static/poster_3.jpg',
        'http://127.0.0.1:8000/static/poster_4.jpg',
        'http://127.0.0.1:8000/static/poster_5.jpg',
      ],
      data: []
    }
  },
  mounted() {
    get('/api/show_movies').then(data =>{
      data.list.forEach((val,index) => {
        let title = data.list[index].fields.movie_title
        let score = data.list[index].fields.movie_score
        data.list[index].fields.movie_title = title.replace(/.*《/g,'').replace(/》.*/g,'')
        data.list[index].fields.movie_score = score.replace(/\/.*/g,'')

      })
      this.data = data.list.slice(0,30)
    })
  },
}
</script>

<style lang="scss" scoped>
.home {
  .content {
    margin-right: 20px;
  }
  .movie-cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
}
</style>