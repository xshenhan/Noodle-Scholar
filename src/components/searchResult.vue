<template>
    <div>
        <div class="row align-items-center justify-content-center text-center">
            <div class="col-md-10">
            </div>
        </div>
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
                <div class="container reform_size_container">
                    <div class="row justify-content-between align-items-center text-md-center text-lg-left">
                        <div class="reform_size_content" :class="{ 'col-lg-9': paper.pic_num !== 0 }">
                            <h5 class=" text-black hoverable "><strong><span @click="GoToPaperPage(paper._id)"
                                        v-html="paper.title"></span></strong></h5>

                            <p v-if="paper.doi!=null && paper.doi!=''"><span class="badge badge-primary">DOI</span>&nbsp;
                                <span @click="copyLink(paper.doi, key)" :class="'copy-button copy-button-' + key"
                                    data-container="body" data-toggle="popover" data-placement="top" data-content="已复制DOI">
                                    <span class="badge badge-success" v-html="paper.doi"></span>
                                </span>
                            </p>

                            <p><span class="badge badge-primary">Author</span>&nbsp;
                                <span v-for="(n, index) in paper.author" :key="index">
                                    <!-- <span class="badge badge-success">{{ n }}</span> -->
                                    <span class="color_blue font-weight-bold" v-html="n"></span>
                                    <span v-if="index !== paper.author.length - 1"><strong>&nbsp;|&nbsp;</strong>
                                    </span>
                                </span>
                            </p>

                            <p><span class="badge badge-primary">Abstract</span>&nbsp; <span v-html="paper.abstract"></span>
                            </p>

                        </div>

                        <!-- 论文图片展示 -->
                        <div class="col-lg-3 text-md-right text-lg-right mt-4 mb-4">

                            <div :id="'paperPictureDisplay' + key" class="carousel slide" data-ride="carousel">

                                <div class="carousel-inner">

                                    <!-- <div class="carousel-item active">
                                        <div class="card shadow-sm border-0">
                                            <img :src="'http://10.80.135.205:8080' + paper.pics['0']"
                                                class="img-fluid mx-auto d-block fill-image">
                                        </div>
                                    </div> -->

                                    <div v-for="(url, index) in paper.pics" :key="index" class="carousel-item"
                                        :class="{ active: index === '0' }">
                                        <div class="card shadow-sm border-0">
                                            <img :src="'http://10.80.135.205:8080' + url"
                                                class="img-fluid mx-auto d-block fill-image">
                                        </div>
                                    </div>

                                    <a class="carousel-control-prev" :href="'#paperPictureDisplay' + key" role="button"
                                        data-slide="prev">
                                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                                        <span class="sr-only">Previous</span>
                                    </a>
                                    <a class="carousel-control-next" :href="'#paperPictureDisplay' + key" role="button"
                                        data-slide="next">
                                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                                        <span class="sr-only">Next</span>
                                    </a>
                                </div>
                            </div>

                        </div>

                        <!-- 下载按钮, 移到paper页面 -->
                        <!-- <div class="col-lg-4 text-md-center text-lg-left mt-4 mb-4">
                            <a :href="getDownloadLink(paper._id)" class="btn btn-lg btn-outline-primary">PDF</a>
                        </div> -->
                    </div>

                </div>
            </div>
        </div>


    </div>
</template>

<script>
import axios from 'axios';
import ClipboardJS from 'clipboard';

export default {
    data() {
        return {
            search_type: "NULL",
            search_type_print: "NULL",


            search_field: "",
            search_info: "",
            search_source: "",

            paper_number: 20,

            already_searched: false,
            paper_id: "NULL",
            paper_title: "NULL",
            paper_abstract: "NULL",

            responses: {},
            response_data: {},

            pictures_urls: {},
        }
    },

    mounted() {
        this.search_field = this.$route.query.field;
        this.search_info = this.$route.query.info;
        this.search_source = this.$route.query.source;
        console.log("field = " + this.search_field);
        console.log("info = " + this.search_info);
        console.log("source = " + this.search_source);
        this.getAllPaperInfo();
        // this.getLimitedPaperInfo();
        $(function () {
            $('[data-toggle="popover"]').popover();
        });
    },

    methods: {

        selectSearchType(type) {
            this.search_type = type;
            if (type === "Subject") {
                this.search_type_print = "tag";
            } else {
                this.search_type_print = type.toLowerCase();
            }
            console.log("search_type changed to " + type);
            console.log("search_type_print: " + type);
        },

        getAllPaperInfo() {
            axios.get('http://10.80.135.205:8080/api/v1/search', {
                params: {
                    field: this.search_field,
                    query: this.search_info,
                    source: this.search_source,
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

        getPicUrls(_ID) {
            axios.get('http://10.80.135.205:8080/api/v1/paper/pics', {
                params: {
                    id: _ID,
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    this.picture_urls = response.data;
                    return response.data;
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                });
        },

        async fetchImagesForPaper(paper) {
            console.log("enter");
            try {
                console.log("before axios");
                const response = await axios.get(`http://10.80.135.205:8080/api/v1/paper/pics?id=${paper.id}`);
                console.log("after axios");

                if (response.data) {
                    // 假设响应是一个对象，键是索引，值是URL
                    Vue.set(paper, 'imageUrls', Object.values(response.data));
                }
            } catch (error) {
                console.error('Error fetching images for paper:', error);
            }
        },

        getDownloadLink(ID) {
            const downloadURL = "http://10.80.135.205:8080/api/v1/paper/download?id=" + ID;
            return downloadURL;
        },

        GoToPaperPage(_ID) {
            const _url = "/paper?id=" + _ID + "&source=" + this.search_source
            // this.$router.push(_url);
            window.open(_url, "_blank");
        },

        copyLink(_doi, key) {
            const textToCopy = _doi;
            const selector = '.copy-button-' + key;
            const clipboard = new ClipboardJS(selector, {
                text: () => textToCopy
            });

            clipboard.on('success', () => {

                const temp = '[data-toggle="popover"]';
                $(temp).popover();
                const popoverElement = $(selector);

                popoverElement.popover('show');

                setTimeout(() => {
                    popoverElement.popover('hide');
                }, 1000); // 1秒后隐藏 popover
            });

            clipboard.onClick({
                target: document.querySelector(selector)
            });
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
    width: 90% !important;
    margin-bottom: 10px !important;
    margin: 0 auto;
    padding-top: 10px;
}

.reform_size_container {
    width: 100% !important;
    margin-top: 15px !important;
    margin-left: 2% !important;
    margin-right: 1% !important;
    margin: 0 0 10px 0;
}

.reform_size_content {
    width: 100% !important;
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

.hoverable:hover {
    text-decoration: underline;
}

.fill-image {
    object-fit: cover;
    width: 500px;
    height: 200px;
    padding: 10px;
}

.color_blue {
    color: #2578b5;
}

.color_purple {
    color: #8d4bbb;
}
</style>

