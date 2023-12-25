<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a href="./"><img src="../assets/img/N.png" alt="LOGO" style="width: 25px !important;"></a>
            &nbsp;&nbsp;&nbsp;
            <a class="navbar-brand" href="./"><i class="mr-2"></i><strong>Noodle</strong> Scholar</a>
            <button class="navbar-toggler collapsed" type="button" data-toggle="collapse" data-target="#navbarColor02"
                aria-controls="navbarColor02" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="navbar-collapse collapse" id="navbarColor02" style="">
                <ul class="navbar-nav mr-auto d-flex align-items-center">
                    <li class="nav-item">
                        <a class="nav-link" href="./">Home</a>
                    </li>
                </ul>


                <!-- </div> -->


                <!-- nav 中的搜索框 -->
                <div class="container" style="padding-left: 20px; padding-right: 0px;">
                    <div class="col d-flex">

                        <!-- 上方 -->
                        <div class="input-group under_border form-check-input">

                            <!-- Arxiv 选择器 -->
                            <button type="button" class=" btn btn_circle_home "
                                :class="{ btn_circle_home_active: this.agreed }"
                                @click="changeAgreement"><strong>Arxiv</strong>
                            </button>

                            <!-- 搜索框 -->
                            <input id="search-input" type="text" class="form-control form-control-rounded no_box_shadow"
                                v-model="search_info" @keyup.enter="SearchAndGoToResultPage"
                                aria-label="Text input with dropdown button"
                                :placeholder="`Search by ${search_type_print}`">

                            <!-- 搜索条件选择器 -->
                            <!-- BUG: 为什么尖叫向上 && 只能下拉一次菜单 -->
                            <div class="input-group-append">
                                <button class="btn btn-outline-secondary_rewrite dropdown-toggle btn-rounded" type="button"
                                    data-toggle="dropdown" aria-expanded="false">{{ search_type_print }}</button>
                                <div class="dropdown-menu">
                                    <a class="dropdown-item" @click="selectSearchType('All')"><strong>All</strong></a>
                                    <div role="separator" class="dropdown-divider"></div>
                                    <a class="dropdown-item" @click="selectSearchType('Title')"><strong>Title</strong></a>
                                    <a class="dropdown-item"
                                        @click="selectSearchType('Subject')"><strong>Subject</strong></a>
                                    <a class="dropdown-item" @click="selectSearchType('Author')"><strong>Author</strong></a>
                                    <a class="dropdown-item"
                                        @click="selectSearchType('Journal')"><strong>Journal</strong></a>
                                    <a class="dropdown-item" @click="selectSearchType('DOI')"><strong>DOI</strong></a>
                                    <a class="dropdown-item"
                                        @click="selectSearchType('Abstract')"><strong>Abstract</strong></a>
                                </div>
                            </div>
                        </div>


                        <!-- 下方 -->
                        <!-- 搜索按钮 -->
                        <div class="col">
                            <button type="button" @click="SearchAndGoToResultPage"
                                class="btn btn-primary btn-rounded button_white_border_search">Search</button>
                        </div>
                    </div>
                </div>
            </div>

            <ul class="navbar-nav ml-auto d-flex align-items-center">
                <li v-if="!this.isLogin" class="nav-item">
                    <span class="nav-link">
                        <a class="btn btn-secondary btn-round fade-down-left" href="/signup">Sign Up</a>&nbsp;
                        <a class="btn btn-secondary btn-round " href="/login">Log in</a>
                    </span>
                </li>
                <li v-else class="nav-item">
                    <span class="nav-link">
                        <a class="btn btn-outline-primary btn-round fade-down-left"
                            style="color:#c3a6cb !important; border-color: #c3a6cb !important;" @click="logOut">Log out</a>
                    </span>
                </li>
            </ul>
        </div>


    </nav>

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
                            <h5 class="text-black hoverable cursor_pointer"><strong><span @click="GoToPaperPage(paper._id)"
                                        v-html="paper.title"></span></strong></h5>

                            <p v-if="paper.doi != null && paper.doi != ''"><span
                                    class="badge badge-primary">DOI</span>&nbsp;
                                <span @click="copyLink(paper.doi, key)" :class="'copy-button copy-button-' + key"
                                    data-container="body" data-toggle="popover" data-placement="top" data-content="已复制DOI">
                                    <span class="badge badge-success cursor_pointer" v-html="paper.doi"></span>
                                </span>
                            </p>

                            <p><span class="badge badge-primary">Author</span>&nbsp;
                                <span v-if="this.search_source === '100pdfs'" v-for="(n, index) in paper.author.name"
                                    :key="index">
                                    <span v-if="index <= 10" @click="SearchAuthor(n)"
                                        class="color_blue font-weight-bold hoverable cursor_pointer" v-html="n"></span>
                                    <span v-if="index !== paper.author.length - 1"><strong>&nbsp;|&nbsp;</strong>
                                    </span>
                                </span>
                                <span v-if="this.search_source === 'arxiv'" v-for="(n, index) in paper.author" :key="index">
                                    <span v-if="index <= 10" @click="SearchAuthor(n)"
                                        class="color_blue font-weight-bold hoverable cursor_pointer" v-html="n"></span>
                                    <span
                                        v-if="index <= 10 && index !== paper.author.length - 1"><strong>&nbsp;|&nbsp;</strong>
                                    </span>
                                </span>
                            </p>

                            <p
                                v-if="(this.search_source === 'arxiv' && paper.tag !== null) || (this.search_source === '100pdfs' && paper.keywords.length !== 0)">
                                <span class="badge badge-primary">Keywords</span>&nbsp;
                                <span v-if="this.search_source === '100pdfs'" v-for="(n, index) in paper.keywords"
                                    :key="index">
                                    <span @click="SearchSubject(n)" class="badge cursor_pointer badge_outline"
                                        v-html="n"></span>
                                    <span v-if="index !== paper.keywords.length - 1"><strong>&nbsp;&nbsp;</strong>
                                    </span>
                                </span>
                                <span v-if="this.search_source === 'arxiv'" v-for="(n, index) in paper.tag.split(' ')"
                                    :key="index">
                                    <span @click="SearchSubject(n)" class="badge cursor_pointer badge_outline"
                                        v-html="n"></span>
                                    <span v-if="index !== paper.tag.split(' ').length - 1"><strong>&nbsp;&nbsp;</strong>
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
                                            <img :src="'' + paper.pics['0']"
                                                class="img-fluid mx-auto d-block fill-image">
                                        </div>
                                    </div> -->

                                    <div v-for="(url, index) in paper.pics" :key="index" class="carousel-item"
                                        :class="{ active: index === '0' }">
                                        <div class="card shadow-sm border-0">
                                            <img :src="'' + url"
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

        <div class="alert alert-cyan text_center" role="alert">
            <strong>已显示全部搜索结果</strong>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import ClipboardJS from 'clipboard';

export default {
    data() {
        return {
            isLogin: false,

            search_type: "all",
            search_type_print: "All",


            search_field: "all",
            search_info: "",
            search_source: "",

            paper_number: 30,

            agreed: false,
            searchArxiv: false,

            already_searched: false,
            paper_id: "NULL",
            paper_title: "NULL",
            paper_abstract: "NULL",

            responses: {},
            response_data: {},

            pictures_urls: {},
        }
    },

    async mounted() {
        await this.initialize();
    },

    methods: {

        async initialize() {
            await this.checkLogin();
            console.log("initializing...")
            $(this.$el).find('[data-toggle="dropdown"]').dropdown();
            this.search_field = this.$route.query.field;
            this.search_info = this.$route.query.info;
            this.search_source = this.$route.query.source;
            this.search_type = this.search_field[0].toUpperCase() + this.search_field.substring(1);
            console.log("field = " + this.search_field);
            console.log("info = " + this.search_info);
            console.log("source = " + this.search_source);
            this.getAllPaperInfo();
            $(function () {
                $('[data-toggle="popover"]').popover();
            });
        },

        SearchAndGoToResultPage() {
            var url = "/searchResult?field=" + this.search_type + "&info=" + encodeURIComponent(this.search_info);
            if (this.searchArxiv) {
                url += "&source=arxiv";
            } else {
                url += "&source=100pdfs";
            }
            this.$router.push(url);
            this.initialize();
        },

        changeAgreement() {
            this.agreed = !this.agreed;
            this.searchArxiv = !this.searchArxiv;
            // console.log("agreed changed to " + this.agreed);
            console.log("searchArxiv changed to " + this.searchArxiv);
        },

        selectSearchType(type) {
            this.search_type = type;
            this.$nextTick(() => {
                $(this.$el).find('[data-toggle="dropdown"]').dropdown('update');
            });
            if (type === "Subject") {
                this.search_type_print = "tag";
            } else {
                this.search_type_print = type.toLowerCase();
            }
            console.log("search_type changed to " + type);
            console.log("search_type_print: " + type);
        },

        getAllPaperInfo() {
            axios.get('/api/v1/search', {
                params: {
                    field: this.search_field,
                    query: this.search_info,
                    source: this.search_source,
                }
            })
                .then((response) => {
                    this.responses = response;

                    // Sort the data and then assign it directly
                    const sortedData = {};
                    Object.keys(this.responses.data)
                        .sort((a, b) => a - b)
                        .forEach(key => {
                            sortedData[key] = this.responses.data[key];
                        });

                    // Assign the sorted data to response_data
                    this.response_data = sortedData;

                    console.log(Object.keys(this.response_data).length);
                })
                .catch((error) => {
                    console.error('Error:', error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                });
        },


        // getLimitedPaperInfo() {
        //     response_data = Object.fromEntries(Object.entries(this.responses.data).slice(0, this.paper_number));
        //     // 打印response_data长度
        //     console.log(Object.keys(response_data).length);
        // },

        getPicUrls(_ID) {
            axios.get('/api/v1/paper/pics', {
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
                const response = await axios.get(`/api/v1/paper/pics?id=${paper.id}`);
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
            const downloadURL = "/api/v1/paper/download?id=" + ID;
            return downloadURL;
        },

        SearchAuthor(_name) {
            var _url = "/searchResult?field=author" + "&info=" + encodeURIComponent(_name) + "&source=" + this.search_source;
            window.open(_url, "_blank");
        },

        SearchSubject(_subject) {
            var _url = "/searchResult?field=tag" + "&info=" + encodeURIComponent(_subject) + "&source=" + this.search_source;
            window.open(_url, "_blank");
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

        async checkLogin() {
            return axios.get('/api/v1/user/check_login')
                .then((response) => {
                    this.isLogin = response.data.login_in;
                    console.log("log in status: " + response.data.login_in);
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        async logOut() {
            axios.get('/api/v1/user/logout')
                .then((response) => {
                    console.log("log out status: " + response.data.logout);
                    this.isLogin = false;

                })
                .catch((error) => {
                    console.log(error);
                });
            await this.initialize();
        }
    },

    watch: {
        '$route': {
            immediate: true,
            handler() {
                this.initialize();
            }
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

.text_center {
    text-align: center !important;
    width: auto !important;
    margin-left: 70.852px;
    margin-right: 70.852px;
    margin-top: 10px;
    margin-bottom: 100px;
    background-color: #2578b5;
    color: #ffffff;
    border: none;
}

.cursor_pointer {
    cursor: pointer;
}

.button_white_border_search {
    border-color: #ffffff;
    top: 45%;
    transform: translate(-50%, -50%);
    right: -50%;
}

.badge_outline {
    border: 1px solid #2578b5 !important;
    color: black !important;
}
</style>

