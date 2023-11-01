<template>
    <h1>{{ component_title }}</h1>
    <div>
        <input type="text" v-model="searchTerm" placeholder="输入要查询的文章 id">
        <button @click="search">Search</button>
    </div>
    <div class="btn-group" role="group" aria-label="Basic example">
        <button type="button" class="btn btn-secondary">上一篇</button>
        <button type="button" class="btn btn-secondary">下一篇</button>
    </div>
</template>
  
<script>
import axios from 'axios';
export default {
    data() {
        return {
            component_title: "get Requset",
        }
    },

    methods: {
        search() {
            axios.get('http://localhost:8001/api/v1/paper/info', {
                params: {
                    id: this.searchTerm
                }
            })
                .then(function (response) {
                    // 响应数据待处理
                    console.log(response);
                    // print(response);
                })
                .catch(function (error) {
                    console.log(error);
                });
        }
    }
}
</script>

