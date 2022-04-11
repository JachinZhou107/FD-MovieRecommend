<template>
  <a-list class="list-box">
    <template #header>
      最近热映
    </template>
    <a-list-item v-for="(item) in data" :key="item.pk">
      <a-list-item-meta>
        <template #avatar>
          <div class="img-box">
            <a-image alt="无图片" width="70" height="100" :preview="false"
                     :src="item.fields.movie_poster" referrerPolicy="no-referrer">
              <template #loader>
                <img
                  width="70"
                  :src="item.fields.movie_poster"
                  style="filter: blur(5px);"
                  referrerPolicy="no-referrer"
                />
              </template>
            </a-image>
          </div>
        </template>
        <template #title>
          <div class="title-box">
            {{item.fields.movie_title}}
          </div>
        </template>
        <template #description>
          <div class="desc-box">
            上映时间：{{item.fields.movie_time}}<br>上映地区：{{item.fields.movie_country}}<br>豆瓣评分：{{item.fields.movie_score || '暂无'}}
          </div>
        </template>
      </a-list-item-meta>
    </a-list-item>
  </a-list>
</template>

<script>
import {get} from "@/utils/request";

export default {
  name: "SiderList",
  data() {
    return {
      columns: [
        {
          title: 'Movie Name',
          dataIndex: 'fields.movie_name',
        },{
          title: 'Movie Time',
          dataIndex: 'fields.movie_time'
        }
      ],
      data: [],
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
      console.log(this.data)
    })
  },
}
</script>

<style lang="scss" scoped>
.list-box {
  text-align: left;
}
.img-box {
  height: 100px;
  width: 70px;
  img {
    height: 100%;
    width: 100%;
    object-fit: fill;
  }
}
</style>