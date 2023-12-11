<!-- Paper.vue -->
<template>
    <div class="jumbotron jumbotron-fluid set_margin set_padding">
        <div class="container">
            <h2 class="text-left">{{ this.paper_title }}</h2>
            <br>
            <p class="lead"><span class="badge badge-primary">Author</span>&nbsp;
                <span v-for="(aut, i) in this.paper_author" :key="i">
                    <span class="color_blue font-weight-bold">{{ aut }}</span>
                    <span v-if="i !== this.paper_author.length - 1"><strong>&nbsp;|&nbsp;</strong></span>
                </span>
            </p>
            <p class="lead"><span class="badge badge-primary">Abstract</span>&nbsp;
                {{ this.paper_abstract }}</p>


            <div class="col-lg-4 text-md-center text-lg-left mt-4 mb-4">
                <button @click="copyLink" class="copy-button btn btn-outline-primary" data-container="body"
                    data-toggle="popover" data-placement="top" data-content="已复制链接">Share
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-share-fill" viewBox="0 0 16 16">
                        <path
                            d="M11 2.5a2.5 2.5 0 1 1 .603 1.628l-6.718 3.12a2.499 2.499 0 0 1 0 1.504l6.718 3.12a2.5 2.5 0 1 1-.488.876l-6.718-3.12a2.5 2.5 0 1 1 0-3.256l6.718-3.12A2.5 2.5 0 0 1 11 2.5z" />
                    </svg>
                </button>
                &nbsp;
                <a :href="getDownloadLink(this.paper_id)" class="btn btn-outline-primary">PDF
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-cloud-download-fill" viewBox="0 0 16 16">
                        <path fill-rule="evenodd"
                            d="M8 0a5.53 5.53 0 0 0-3.594 1.342c-.766.66-1.321 1.52-1.464 2.383C1.266 4.095 0 5.555 0 7.318 0 9.366 1.708 11 3.781 11H7.5V5.5a.5.5 0 0 1 1 0V11h4.188C14.502 11 16 9.57 16 7.773c0-1.636-1.242-2.969-2.834-3.194C12.923 1.999 10.69 0 8 0zm-.354 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V11h-1v3.293l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z" />
                    </svg>
                </a>
                &nbsp;

                <!-- <button @click.prevent="modelSummary" class="btn btn-outline-primary">GPT Sumaary

                    <div v-if="display_summary_window" class="fullscrenn-popover">
                        <div class="popover-content">
                            <p>{{ this.model_message }}</p>
                        </div>
                    </div>
                </button> -->

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
            paper_id: "NULL",
            paper_source: "NULL",

            paper_title: "NULL",
            paper_abstract: "NULL",
            paper_doc_type: "NULL",
            paper_year: "NULL",
            paper_volume: "NULL",
            paper_cite: "NULL",
            paper_kqi: "NULL",
            paper_tag: "NULL",
            paper_doi: "NULL",
            paper_author: [],
            paper_affiliation: [],


            display_summary_window: false,
            model_model_type: "NULL",
            model_message: "NULL",
        }
    },

    mounted() {
        this.paper_id = this.$route.query.id;
        this.paper_source = this.$route.query.source;
        $(function () {
            $('[data-toggle="popover"]').popover();
        });
        this.getPaperInfo();
    },

    methods: {
        getDownloadLink(id) {
            return "http://10.80.135.205:8080/api/v1/paper/download?id=" + id;
        },

        getPaperInfo() {
            const _ID = this.$route.query.id;
            const _source = this.$route.query.source;
            axios.get('http://10.80.135.205:8080/api/v1/paper/info', {
                params: {
                    id: _ID,
                    source: _source,
                }
            })
                .then((response) => {
                    // 响应数据待处理\
                    this.paper_title = response.data.title;
                    this.paper_abstract = response.data.abstract;
                    this.paper_doc_type = response.data.doc_type;
                    this.paper_year = response.data.year;
                    this.paper_volume = response.data.volume;
                    this.paper_cite = response.data.cite;
                    this.paper_kqi = response.data.kqi;
                    this.paper_tag = response.data.tag;
                    for (var i = 0; i < response.data.author.length; i++) {
                        if (this.paper_author.indexOf(response.data.author[i]) == -1)
                            this.paper_author.push(response.data.author[i]);
                    }
                    for (var i = 0; i < response.data.affiliation.length; i++) {
                        if (this.paper_affiliation.indexOf(response.data.affiliation[i]) == -1)
                            this.paper_affiliation.push(response.data.affiliation[i]);
                    }
                    console.log("Got paper [" + _ID + "] data");
                })
                .catch((error) => {
                    console.log(error);
                    this.paper_id = "!! ERROR !!";
                });

        },

        copyLink() {
            const textToCopy = window.location.href;
            const clipboard = new ClipboardJS('.copy-button', {
                text: () => textToCopy
            });

            clipboard.on('success', () => {
                $('[data-toggle="popover"]').popover();
                const popoverElement = $('[data-toggle="popover"]');

                popoverElement.popover('show');

                setTimeout(() => {
                    popoverElement.popover('hide');
                }, 1000); // 1秒后隐藏 popover
            });

            clipboard.onClick({
                target: document.querySelector('.copy-button')
            });
        },

        modelSummary() {
            this.display_summary_window = !this.display_summary_window;

            // axios.get('http://10.80.135.205:8080/api/v1/model/summary', {
            //     params: {
            //         id: this.paper_id,
            //         source: this.paper_source,
            //     }
            // })
            //     .then((response) => {
            //         this.model_message = response.data.message;
            //         this.model_model_type = response.data.model;
            //     })
            //     .catch((error) => {
            //         console.log(error);
            //         this.paper_id = "!! ERROR !!";
            //     });
        }
    }
};
</script>


<style>
.set_margin {
    margin-top: 20px;
    margin-right: 20px;
    margin-left: 20px;
}

.set_padding {
    padding-top: 30px !important;
    padding-bottom: 10px !important;
}

html,
body {
    height: 100%;
}

.container,
.row {
    height: 100%;
}

.align-self-center {
    align-self: center;
}

.middle_title {
    text-align: center !important;
}

.no_under_margin {
    margin-bottom: 0;
}


.btn_circle_paper {
    width: 36.781px;
    height: 36.781px;
    border-radius: 10%;
    position: relative;
    padding: 0;
    overflow: visible;
    border: none;
}

.btn_circle_paper :active {
    border: 10px solid white;
}

.btn_circle_paper :active {
    position: absolute;
    top: 50%;
    left: 50%;
}

.inner_btn_check {
    width: 34.781px;
    height: 34.781px;
    position: relative !important;
}

.resize {
    width: 30%;
    height: 150%;
    margin: 0 auto;
    padding-bottom: 150px;
    /* 足够覆盖 footer 的高度 */
}

.button-with-text {
    display: flex;
    align-items: center;
}

.submit_button {
    display: flex;
    justify-content: center;
}


.fullscreen-popover {
    position: fixed;
    /* 固定定位 */
    top: 50%;
    /* 垂直居中 */
    left: 50%;
    /* 水平居中 */
    transform: translate(-50%, -50%);
    /* 调整定位以确保完全居中 */
    width: auto;
    /* 或者设定具体宽度 */
    height: auto;
    /* 或者设定具体高度 */
    background-color: white;
    z-index: 1000;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}


.popover-content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}


.agree-section {
    margin-top: 20px;
}

/* 自定义复选框样式
input[type="checkbox"] {
    accent-color: green; /* 设置复选框的主题颜色 
}

自定义标签样式 
label {
    margin-left: 8px;
} */
/*
.popover-content {
    display: flex;  使用 Flexbox 
    justify-content: space-between;  内容两侧对齐 
    align-items: center;  垂直居中 
}
*/
/* 弹出框内按钮的容器 */
.popover-buttons {
    margin-left: auto;
    /* 将按钮组推到右侧 */
}


.popover-content {
    /* 其他样式 */
    display: flex;
    flex-direction: column;
    /* 子元素垂直排列 */
    align-items: flex-start;
    /* 子元素向左对齐 */
}

/* 按钮容器的样式 */
.buttons-container {
    margin-top: 20px;
    /* 在内容和按钮之间添加一些空间 */
    align-self: flex-end;
    /* 将按钮组推到右侧 */
}
</style>