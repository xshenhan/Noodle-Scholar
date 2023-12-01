<template>
    <div>
        <button @click="changeVisible" class="btn btn-dark">Display / Hide</button>
        <div v-if="paper_display">
            <br><br>

            <!-- <div class="media">
                <img src="../assets/img/N标.png" class="marigin_lr" alt="..." :width="30">
                <div class="media-body">
                    <h5 class=""><span v-html="paper_title"></span></h5>
                    <p><strong>Abstract :</strong>&nbsp; <span v-html="paper_abstract"></span></p>
                </div>
            </div> -->

            <div class="media" v-for="(paper, key) in response_data" :key='key'>
                <img src="../assets/img/N标.png" class="marigin_lr" alt="..." :width="30">
                <div class="media-body">
                    <h5 class=""><span v-html="paper.title[0]"></span></h5>
                    <p><strong>Abstract :</strong>&nbsp; <span v-html="paper.abstract"></span></p>
                </div>
            </div>


            <!-- Call to action -->
            <div class=" bg-light large_padding">
                <div class="container h-100">
                    <div class="row justify-content-between align-items-center text-md-center text-lg-left">
                        <div class="col-lg-9">
                            <h5 class="font-weight-light text-black">Free Bootstrap 4.1.3<strong> UI Kit</strong> with
                                <strong><i class="fab fa-sass fa-2x"></i></strong> for rapid development</h5>
                        </div>
                        <div class="col-lg-3 text-md-center text-lg-right mt-4 mb-4">
                            <a href="#" class="btn btn-lg btn-info">Call to action</a>
                        </div>
                    </div>
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

            paper_number: 10,

            already_searched: false,
            paper_id: "NULL",
            paper_title: "NULL",
            paper_abstract: "NULL",

            responses: {},
            response_data: {},

            paper_display: true,
        }
    },

    mounted() {
        this.search_field = this.$route.query.field;
        this.search_info = this.$route.query.info;
        console.log("field = " + this.search_field);
        console.log("info = " + this.search_info);
        this.getAllPaperInfo();
        // this.getLimitedPaperInfo();
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
                    this.paper_id = response.data["0"]._id;
                    this.paper_title = response.data["0"].title[0];
                    this.paper_abstract = response.data["0"].abstract;
                    console.log("finish changing data");
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                });
        },

        getAllPaperInfo() {
            axios.get('http://10.80.135.205:8001/api/v1/search', {
                params: {
                    field: this.search_field,
                    query: this.search_info,
                }
            })
                .then((response) => {
                    this.responses = response;
                    this.response_data = Object.fromEntries(Object.entries(this.responses.data).slice(0, this.paper_number));
                    // 打印response_data长度
                    console.log(Object.keys(this.response_data).length);
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                })

        },

        getLimitedPaperInfo() {
            response_data = Object.fromEntries(Object.entries(this.responses.data).slice(0, this.paper_number));
            // 打印response_data长度
            console.log(Object.keys(response_data).length);
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

.large_padding {
    padding-left: 100px !important;
    padding-right: 300px !important;
    margin-bottom: 0px !important;
    margin-left: 50px !important;
    margin-right: 50px !important;
}

.paper_title {
    font-size: 20px;
}
</style>

