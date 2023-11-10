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

    <!-- 仅在 already_searched = true 的时候显示如下表单 -->
    <div v-if="already_searched">
        <div class="card bg-dark overlay overlay-black text-white shadow-lg border-0">
            <img class="card-img" src="../assets/img/demo/7.jpg" alt="Card image">
            <div class="card-img-overlay d-flex align-items-center text-center">
                <div class="card-body">
                    <h3 class="card-title">Overlay center align</h3>
                    <p class="card-text text-muted">
                        With supporting text below as a natural lead-in to additional content.
                    </p>
                    <a href="#" class="btn btn-info btn-round">Do anything</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            component_title: "get Requset",
            already_searched: false,
        }
    },

    methods: {
        search() {
            axios.get('http://localhost:8001/api/v1/paper/info', {
                params: {
                    id: this.searchTerm
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    console.log(response);
                    this.already_searched = true;
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                });
        }
    }
}
</script>

