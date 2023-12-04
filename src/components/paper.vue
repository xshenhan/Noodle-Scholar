<!-- Paper.vue -->
<template>
    <div class="jumbotron jumbotron-fluid set_margin set_padding">
        <div class="container">
            <h2 class="text-left">{{ this.paper_title }}</h2>
            <br>
            <p class="lead"><span class="badge badge-pill badge-primary">Abstract</span>&nbsp;
                {{ this.paper_abstract }}
            </p>


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
            paper_title: "NULL",
            paper_abstract: "NULL",
            paper_doc_type: "NULL",
            paper_year: "NULL",
            paper_volume: "NULL",
            paper_cite: "NULL",
            paper_kqi: "NULL",
            paper_tag: "NULL",
        }
    },

    mounted() {
        this.paper_id = this.$route.query.id;
        $(function () {
            $('[data-toggle="popover"]').popover();
        });
        this.getPaperInfo();
    },

    methods: {
        getDownloadLink(id) {
            return "/api/v1/paper/download?id=" + id;
        },

        getPaperInfo() {
            const _ID = this.$route.query.id;
            axios.get('http://10.80.135.205:8001/api/v1/paper/info', {
                params: {
                    id: _ID,
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
</style>