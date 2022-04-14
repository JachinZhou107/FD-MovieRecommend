<template>
  <div class="notfound">
    <a-empty>
      <template #image>
        <icon-exclamation-circle-fill />
      </template>
      404 Not Found
    </a-empty>
  </div>
</template>

<script>
export default {
  name: "NotFound"
}
</script>

<style scoped>
.notfound {
  height: 500px;
  display: flex;
  align-items: center;
}
</style>