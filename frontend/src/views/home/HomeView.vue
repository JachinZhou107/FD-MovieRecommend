<template>
  <div class="home">
    <a-layout>
      <a-layout-content>
        <a-carousel
          :style="{
            width: '100%',
            height: '240px'
          }"
          :default-current="2"
          animation-name="card"
          indicator-position="outer"
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
      </a-layout-content>
      <a-layout-sider :style="{width: '30%', maxWidth: '300px'}">
        <a-list>
          <a-list-item>
            <a-list-item-meta title="蜘蛛侠：英雄归来"
                              description="Beijing ByteDance Technology Co., Ltd."
            >
              <template #avatar>
                <a-avatar shape="square">
                  <img alt="avatar" src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp" />
                </a-avatar>
              </template>
            </a-list-item-meta>
          </a-list-item>
          <a-list-item>
            <a-list-item-meta title="钢铁侠"
                              description="Beijing ByteDance Technology Co., Ltd."
            >
              <template #avatar>
                <a-avatar shape="square">
                  <img alt="avatar" src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp" />
                </a-avatar>
              </template>
            </a-list-item-meta>
          </a-list-item>
          <a-list-item>
            <a-list-item-meta title="尼罗河上的惨案"
                              description="Beijing ByteDance Technology Co., Ltd."
            >
              <template #avatar>
                <a-avatar shape="square">
                  <img alt="avatar" src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp" />
                </a-avatar>
              </template>
            </a-list-item-meta>
          </a-list-item>
          <a-list-item>
            <a-list-item-meta title="阿甘正传"
                              description="Beijing ByteDance Technology Co., Ltd."
            >
              <template #avatar>
                <a-avatar shape="square">
                  <img alt="avatar" src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/3ee5f13fb09879ecb5185e440cef6eb9.png~tplv-uwbnlip3yd-webp.webp" />
                </a-avatar>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </a-layout-sider>
    </a-layout>
    <a-layout-footer>Footer</a-layout-footer>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  data() {
    return {
      images: [
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/cd7a1aaea8e1c5e3d26fe2591e561798.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/6480dbc69be1b5de95010289787d64f1.png~tplv-uwbnlip3yd-webp.webp',
        'https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/0265a04fddbd77a19602a15d9d55d797.png~tplv-uwbnlip3yd-webp.webp',
      ],
    }
  }
}
</script>

<style scoped>

</style>