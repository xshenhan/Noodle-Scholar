<template>
    <h1>{{ component_title }}</h1>
    <div>
        <input type="text" v-model="searchTerm" placeholder="输入要查询的文章 id">
        <button @click="search">Search</button>
        <p>hello, 6532290ad507ea15ca185e7f</p>
        <br>
        <p><strong>Paper ID:</strong> {{ paper_id }}</p>
        <p><strong>Paper Name:</strong> {{ paper_name }}</p>
    </div>
    <div class="btn-group" role="group" aria-label="Basic example">
        <button type="button" class="btn btn-secondary">上一篇</button>
        <button type="button" class="btn btn-secondary">下一篇</button>
    </div>

    <br>
    <button @click="goToAnotherPage">button "SearchResult"</button>
    <br>


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
import router from '../router';

export default {
    data() {
        return {
            component_title: "get Requset",
            already_searched: false,
            paper_id: "NULL id",
            paper_name: "NULL name",
        };
    },
    methods: {
        search() {
            // 重定向到另一个 html 页面
            axios.get('http://10.80.135.205:8080/api/v1/paper/info', {
                params: {
                    id: this.searchTerm
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    // console.log(response);
                    this.already_searched = true;
                    this.paper_id = response.data.id;
                    this.paper_name = response.data.title;
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                });
        },

        goToAnotherPage() {
            this.$router.push("/searchResult");
        }

    },
    watch: {
        paper_id: function (val) {
            console.log("paper_id changed to " + val);
        },
        paper_name: function (val) {
            console.log("paper_name changed to " + val);
        }
    },
    components: { router }
}
</script>

