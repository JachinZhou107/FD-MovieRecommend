<template>
  <div class="about">
    <a-table :columns="columns" :data="data"></a-table>
  </div>
</template>

<script>
import {get} from "@/utils/request";

export default {
  name: 'AboutView',
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
  beforeMount() {
    get('/api/show_movies').then(data =>{
      this.data = data.list
      console.log(this.data)
    })
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>