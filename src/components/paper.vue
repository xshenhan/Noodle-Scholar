<!-- Paper.vue -->
<template>
    <div>
        <h1>Paper Page</h1>
        <p>ID: {{ $route.params.id }}</p>
        <!-- 在这里显示搜索结果 -->
    </div>
</template>
  
<script>
export default {
    mounted() {
        console.log(this.$route.params.id);
    }
};
</script>
  