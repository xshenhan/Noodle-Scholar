<template>
    <div>
        <br><br>

        <!-- <div class="media" v-for="(paper, key) in response_data" :key='key'>
                <img src="../assets/img/N.png" class="marigin_lr" alt="..." :width="30">
                <div class="media-body">
                    <h5 class=""><span v-html="paper.title[0]"></span></h5>
                    <p><strong>Abstract :</strong>&nbsp; <span v-html="paper.abstract"></span></p>
                </div>
            </div> -->


        <div class="media" v-for="(paper, key) in response_data" :key='key'>
            <div class=" bg-light reform_size_frame">
                <div class="container h-100">
                    <div class="row justify-content-between align-items-center text-md-center text-lg-left">
                        <div class="col-lg-9 reform_size_content">
                            <h5 class="font-weight-light text-black"><span class="font-weight-bold"
                                    v-html="paper.title[0]"></span></h5>
                            <p><span class="badge badge-pill badge-purple">Author</span>&nbsp; 
                                <span v-for="(n, index) in paper.author.name" :key="index">
                                    <span class="badge badge-success">{{ n }}</span>
                                    <span v-if="index !== paper.author.name.length - 1"><strong>&nbsp;|&nbsp;</strong> </span>
                                </span>
                            </p>
                            <p><span class="badge badge-pill badge-purple">Abstract</span>&nbsp; <span v-html="paper.abstract"></span></p>
                        </div>

                        <!-- 论文图片展示 -->
                        <div class="col-lg-3 text-md-right text-lg-right mt-4 mb-4">

                            <div id="carouselExampleFade" class="carousel slide carousel-fade" data-ride="carousel">
                                <div class="carousel-inner">
                                  <div class="carousel-item active">
                                    <div class="card shadow-sm border-0">
                                        <img src="../assets/img/论文1.png" class="img-fluid mx-auto d-block" alt="...">
                                    </div>
                                  </div>
                                  <div class="carousel-item">
                                    <div class="card shadow-sm border-0">
                                        <img src="../assets/img/论文2.png" class="img-fluid mx-auto d-block" alt="...">
                                    </div>
                                  </div>
                                  <div class="carousel-item">
                                    <div class="card shadow-sm border-0">
                                        <img src="../assets/img/论文3.png" class="img-fluid mx-auto d-block" alt="...">
                                    </div>
                                  </div>
                                </div>
                                <button class="btn btn-white btn-round shadow-lg reform_img_button button-left" type="button" data-target="#carouselExampleFade" data-slide="prev" placeholder="<">
                                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                  <span class="sr-only">Previous</span>
                                </button>
                                <button class="btn btn-white btn-round shadow-lg reform_img_button button-right" type="button" data-target="#carouselExampleFade" data-slide="next">
                                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                  <span class="sr-only">Next</span>
                                </button>
                              </div>
                        </div>

                        <!-- 下载按钮 -->
                        <div class="col-lg-4 text-md-center text-lg-left mt-4 mb-4">
                            <a :href="getDownloadLink(paper._id)" class="btn btn-lg btn-outline-primary">PDF</a>
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

        // getLimitedPaperInfo() {
        //     response_data = Object.fromEntries(Object.entries(this.responses.data).slice(0, this.paper_number));
        //     // 打印response_data长度
        //     console.log(Object.keys(response_data).length);
        // },

        getDownloadLink(ID) {
            const downloadURL = "http://10.80.135.205:8001/api/v1/paper/download?id=" + ID;
            return downloadURL;
        },
    }
}
</script>


<style>
.marigin_lr {
    margin-left: 1rem;
    margin-right: 2rem;
}

.reform_size_frame {
    padding-top: 20px !important;
    padding-bottom: 10px !important;
    padding-left: 20px !important;
    padding-right: 100px !important;
    margin-bottom: 10px !important;
    margin-left: 50px !important;
    margin-right: 30px !important;
}

.reform_size_content {
    width: 700px !important;
    height: auto !important;
}

.reform_img_button {
    position: absolute !important;
    top: 30% !important;
    height: 30px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 5px !important;
    text-align: center;
    opacity: 0.5;
}

.button-right {
    right: 0 !important;
}

.button-left {
    left: 0 !important;
}

.paper_title {
    font-size: 20px;
}
</style>

