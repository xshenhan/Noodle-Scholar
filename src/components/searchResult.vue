<template>
    <div>
        <button @click="changeVisible" class="btn btn-dark">Display / Hide</button>
        <div v-if="paper_display">
            <br><br>

            <div class="media">
                <img src="../assets/img/N标.png" class="marigin_lr" alt="..." :width="30">
                <div class="media-body">
                    <h5 class=""><span v-html="paper_title"></span></h5>
                    <p><strong>Abstract :</strong>&nbsp; <span v-html="paper_abstract"></span></p>
                </div>
            </div>

            <div class="media">
                <img src="../assets/img/N标.png" class="marigin_lr" alt="..." :width="30">
                <div class="media-body">
                    <h5 class=""><span v-html="paper_title2"></span></h5>
                    <p><strong>Abstract :</strong>&nbsp; <span v-html="paper_abstract2"></span></p>
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
            search_field: "",
            search_info: "",

            already_searched: false,
            paper_id: "NULL",
            paper_title: "NULL",
            paper_abstract: "NULL",

            paper_id2: "NULL",
            paper_title2: "NULL",
            paper_abstract2: "NULL",
            
            paper_display: true,
        }
    },

    mounted() {
        this.search_field = this.$route.query.field;
        this.search_info = this.$route.query.info;
        console.log("field = " + this.search_field);
        console.log("info = " + this.search_info);
        this.searchInfo();
    },

    methods: {

        searchInfo() {
            axios.get('http://10.80.135.205:8001/api/v1/search', {
                params: {
                    field: this.search_field,
                    query: this.search_info,
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    console.log(response);
                    this.already_searched = true;
                    this.paper_id = response.data[0]._id;
                    this.paper_title = response.data[0].title[0];
                    this.paper_abstract = response.data[0].abstract;
                    console.log("finish changing data");
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                });
        },

        searchInfo2() {
            axios.get('http://10.80.135.205:8001/api/v1/search', {
                params: {
                    field: this.search_field,
                    query: this.search_info,
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    console.log(response);
                    this.already_searched = true;
                    this.paper_id2 = response.data[1]._id;
                    this.paper_title2 = response.data[1].title[0];
                    this.paper_abstract2 = response.data[1].abstract;
                    console.log("finish changing data");
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                });
        },

        changeVisible() {
            this.paper_display = !this.paper_display;
            console.log(this.paper_display);
        }
    }
}
</script>


<style>
.marigin_lr {
    margin-left: 1rem;
    margin-right: 2rem;
}
</style>

