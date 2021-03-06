<template>
  <a-popover
      v-if="popover"
      position="rt" :title="item.fields.movie_title||item.fields.movie_name"
      :content-style="{width: '300px'}"
  >
    <a-card hoverable class="card" @click="handleClickFilm">
      <template #cover>
        <div class="img-box">
          <a-image
            width="170"
            height="240"
            :preview="false"
            :src="moviePosterFilter(item.fields.movie_poster)"
            referrerPolicy="no-referrer"
          >
            <template #error-icon>
              <icon-live-broadcast />
            </template>
            <template #loader>
              <icon-loading :style="{height: '100%'}"/>
            </template>
          </a-image>
        </div>
      </template>
      <a-card-meta>
        <template #title>
          <span>
            {{item.fields.movie_title||item.fields.movie_name}}
          </span>
        </template>
        <template #description>
          <div class="desc-box">
            上映时间：{{item.fields.movie_time}}<br>
            豆瓣评分：{{item.fields.movie_score || '暂无'}}
          </div>
        </template>
      </a-card-meta>
    </a-card>
    <template #content>
      <div :style="{
        display: 'flex',
        alignItems: 'center'
      }">
        <a-rate :count="5" :default-value="(item.fields.movie_score/2)||0" readonly allow-half>
          <template #character>
            <icon-star-fill size="16"/>
          </template>
        </a-rate>
        <span v-if="!item.fields.movie_score">（无评价）</span>
      </div>
      <a-space>
        <a-tag v-for="(tag,index) in item.fields.movie_type.split('/')" :key="index">
          {{ tag }}
        </a-tag>
      </a-space>
      <p>{{ item.fields.movie_length }}</p>
      <p>导演： {{ item.fields.movie_director || '暂无'}}</p>
      <p>主演： {{ movieActorsFilter(item.fields.movie_actors) || '暂无'}}</p>
    </template>
  </a-popover>
  <a-card hoverable class="card" @click="handleClickFilm" v-else>
    <template #cover>
      <div class="img-box">
        <a-image
          width="170"
          height="240"
          :preview="false"
          :src="moviePosterFilter(item.fields.movie_poster)"
          referrerPolicy="no-referrer"
        >
          <template #error-icon>
            <icon-live-broadcast />
          </template>
          <template #loader>
            <icon-loading :style="{height: '100%'}"/>
          </template>
        </a-image>
      </div>
    </template>
    <a-card-meta>
      <template #title>
        <slot name="title"></slot>
      </template>
      <template #description>
        <slot name="desc"></slot>
      </template>
    </a-card-meta>
  </a-card>
</template>

<script>
import {link} from "@/utils/link";

export default {
  name: "MovieCard",
  // props: ['item', 'popover'],
  props: {
    'item': {
      type: Object,
      default: () => {
        return {
          fields: {
            movie_name: 'ERROR'
          }
        }
      }
    },
    'popover': {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const movieActorsFilter = (actorList) => {
      return actorList.split('/').slice(0,4).join('/')
    }
    const moviePosterFilter = (posterUrl) => {
      if ( posterUrl?.indexOf('l_ratio_poster') > -1)
        return posterUrl.replace('l_ratio_poster', 's_ratio_poster')
      else return posterUrl
    }
    const handleClickFilm = () => {
      link(`/films/${props.item.pk}`,'films',{ filmId: props.item.pk })
    }
    return {
      movieActorsFilter,
      moviePosterFilter,
      handleClickFilm
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  width: 170px;
  margin: 12px;
  cursor: pointer;
  transition-property: all;
  &:hover{
    transform: translateY(-4px);
  }
  .img-box {
    height: 240px;
    overflow: hidden;
    img {
      width: 100%;
      height: 100%;
      object-fit: fill;
    }
  }
  .desc-box {
    text-align: left;
    margin-top: 10px;
  }
}
</style>