<template>
  <a-upload
    action="/api/avatar"
    :fileList="file ? [file] : []"
    :show-file-list="false"
    :auto-upload="false"
    ref="avatar_upload"
    @change="onChange"
    @progress="onProgress"
    @success="changeUserInfo"
  >
    <template #upload-button>
      <div
        :class="`arco-upload-list-item${
          file && file.status === 'error' ? ' arco-upload-list-item-error' : ''
        }`"
      >
        <div
          class="arco-upload-list-picture custom-upload-avatar"
          v-if="(file && file.url) || avatar"
        >
          <img :src="file.url || avatar" />
          <div class="arco-upload-list-picture-mask">
            <IconEdit />
          </div>
          <a-progress
            v-if="file.status === 'uploading' && file.percent < 100"
            :percent="file.percent"
            type="circle"
            size="mini"
            :style="{
              position: 'absolute',
              left: '50%',
              top: '50%',
              transform: 'translateX(-50%) translateY(-50%)',
            }"
          />
        </div>
        <div class="arco-upload-picture-card" v-else>
          <div class="arco-upload-picture-card-text">
            <IconPlus />
            <div style="margin-top: 10px; font-weight: 600">选择头像</div>
          </div>
        </div>
      </div>
      <a-button v-if="file && file.url" type="primary" @click="submit"> 更改头像 </a-button>
    </template>
  </a-upload>
</template>

<script>
import {useStore} from "vuex";
import {onMounted, ref} from "vue";
import {get} from "@/utils/request";

export default {
  name: "UserAvatar",
  data() {
    return {
      file: '',
    };
  },
  methods: {
    onChange(_, currentFile) {
      this.file = {
        ...currentFile,
        // url: URL.createObjectURL(currentFile.file),
      };
    },
    onProgress(currentFile) {
      this.file = currentFile;
    }
  },
  setup() {
    const store = useStore()
    const avatar = ref('')
    const avatar_upload = ref(null)
    onMounted(()=>{
      avatar.value = store.state.userInfo.avatar
      console.log(avatar_upload.value)
    })
    const submit = async (e) => {
      e.stopPropagation();
      await avatar_upload.value.submit();
    }
    const changeUserInfo = () =>{
      get('/api/login_info').then(res => {
        if (res.login) {
          store.commit('changeUser', { username: res.username, avatar: res.avatar})
        }
      })
    }
    return {
      avatar,
      avatar_upload,
      submit,
      changeUserInfo
    }
  }
}
</script>

<style scoped>

</style>