<template>
    <div class="jumbotron jumbotron-lg jumbotron-fluid mb-3 bg-primary position-relative">
        <div class="container text-white h-100 tofront">
            <div class="row align-items-center justify-content-center text-center">
                <div class="col-md-10">
                    <h1 class="display-3">This is a title</h1>
                </div>
            </div>
        </div>
    </div>
    <a href="http://10.80.135.205:8001/api/v1/paper/download?id=185e7f" class="btn btn-outline-primary btn-round">Download
        PDF</a>


    <h1>Home Vue</h1>
    <input type="text" v-model="searchTerm" placeholder="paper id">
    <button @click="goToAnotherPage" class="btn btn-outline-primary btn-round">button "SearchResult"</button>
    <br>
</template>


<script>
// import axios from 'axios';
// import router from '../router';

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
            axios.get('http://10.80.135.205:8001/api/v1/paper/info', {
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
            this.$router.push("/searchResult" + "?id=" + this.searchTerm);
        }

    },
    watch: {
        paper_id: function (val) {
            console.log("paper_id changed to " + val);
        },
        paper_name: function (val) {
            console.log("paper_name changed to " + val);
        }
    }
}
</script>
