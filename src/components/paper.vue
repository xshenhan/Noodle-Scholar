<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a href="/"><img src="/img/N.png" alt="LOGO" style="width: 25px !important;"></a>
            &nbsp;&nbsp;&nbsp;
            <a class="navbar-brand" href="./"><i class="mr-2"></i><span style="font-weight: bold">Noodle</span> Scholar</a>
            <button class="navbar-toggler collapsed" type="button" data-toggle="collapse" data-target="#navbarColor02"
                aria-controls="navbarColor02" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="navbar-collapse collapse" id="navbarColor02" style="">
                <ul class="navbar-nav mr-auto d-flex align-items-center">
                    <li class="nav-item">
                        <a class="nav-link" href="./" style="font-weight: none; font-size: 15px">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./searchresult" style="font-weight: none; font-size: 15px">Search</a>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto d-flex align-items-center">
                    <li class="nav-item">
                    </li>
                </ul>
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


    <div class="jumbotron jumbotron-fluid set_margin set_padding">
        <div class="container">
            <h2 class="text-left">{{ this.paper_title }}&nbsp;<span class="badge reform_badge_outline">{{ this.paper_year
            }}</span></h2>
            <!-- <br> -->
            <p class="lead"><span class="badge badge-primary">Author</span>&nbsp;
                <span v-for="(aut, i) in this.paper_author" :key="i">
                    <span @click="SearchAuthor(n)" class="color_blue font-weight-bold hoverable cursor_pointer">{{ aut
                    }}</span>
                    <span v-if="i !== this.paper_author.length - 1"><strong>&nbsp;|&nbsp;</strong></span>
                </span>
            </p>
            <p class="lead"><span class="badge badge-primary">Abstract</span>&nbsp;
                <span v-html="htmlText"></span>
            </p>


            <div class="col-lg-12 text-md-center text-lg-left mt-4 mb-4">
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
                <button @click.prevent="modelSummary" class="btn btn-outline-primary">
                    GPT Summary
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-chat-square-text-fill" viewBox="0 0 16 16">
                        <path
                            d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.5a1 1 0 0 0-.8.4l-1.9 2.533a1 1 0 0 1-1.6 0L5.3 12.4a1 1 0 0 0-.8-.4H2a2 2 0 0 1-2-2V2zm3.5 1a.5.5 0 0 0 0 1h9a.5.5 0 0 0 0-1h-9zm0 2.5a.5.5 0 0 0 0 1h9a.5.5 0 0 0 0-1h-9zm0 2.5a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5z" />
                    </svg>
                </button>
                &nbsp;
                <a :href="getOriginWebsite(this.paper_id)" target="_blank" class="btn btn-outline-primary">Website
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-browser-safari" viewBox="0 0 16 16">
                        <path
                            d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16Zm.25-14.75v1.5a.25.25 0 0 1-.5 0v-1.5a.25.25 0 0 1 .5 0Zm0 12v1.5a.25.25 0 1 1-.5 0v-1.5a.25.25 0 1 1 .5 0ZM4.5 1.938a.25.25 0 0 1 .342.091l.75 1.3a.25.25 0 0 1-.434.25l-.75-1.3a.25.25 0 0 1 .092-.341Zm6 10.392a.25.25 0 0 1 .341.092l.75 1.299a.25.25 0 1 1-.432.25l-.75-1.3a.25.25 0 0 1 .091-.34ZM2.28 4.408l1.298.75a.25.25 0 0 1-.25.434l-1.299-.75a.25.25 0 0 1 .25-.434Zm10.392 6 1.299.75a.25.25 0 1 1-.25.434l-1.3-.75a.25.25 0 0 1 .25-.434ZM1 8a.25.25 0 0 1 .25-.25h1.5a.25.25 0 0 1 0 .5h-1.5A.25.25 0 0 1 1 8Zm12 0a.25.25 0 0 1 .25-.25h1.5a.25.25 0 1 1 0 .5h-1.5A.25.25 0 0 1 13 8ZM2.03 11.159l1.298-.75a.25.25 0 0 1 .25.432l-1.299.75a.25.25 0 0 1-.25-.432Zm10.392-6 1.299-.75a.25.25 0 1 1 .25.433l-1.3.75a.25.25 0 0 1-.25-.434ZM4.5 14.061a.25.25 0 0 1-.092-.341l.75-1.3a.25.25 0 0 1 .434.25l-.75 1.3a.25.25 0 0 1-.342.091Zm6-10.392a.25.25 0 0 1-.091-.342l.75-1.299a.25.25 0 1 1 .432.25l-.75 1.3a.25.25 0 0 1-.341.09ZM6.494 1.415l.13.483a.25.25 0 1 1-.483.13l-.13-.483a.25.25 0 0 1 .483-.13ZM9.86 13.972l.13.483a.25.25 0 1 1-.483.13l-.13-.483a.25.25 0 0 1 .483-.13ZM3.05 3.05a.25.25 0 0 1 .354 0l.353.354a.25.25 0 0 1-.353.353l-.354-.353a.25.25 0 0 1 0-.354Zm9.193 9.193a.25.25 0 0 1 .353 0l.354.353a.25.25 0 1 1-.354.354l-.353-.354a.25.25 0 0 1 0-.353ZM1.545 6.01l.483.13a.25.25 0 1 1-.13.483l-.483-.13a.25.25 0 1 1 .13-.482Zm12.557 3.365.483.13a.25.25 0 1 1-.13.483l-.483-.13a.25.25 0 1 1 .13-.483Zm-12.863.436a.25.25 0 0 1 .176-.306l.483-.13a.25.25 0 1 1 .13.483l-.483.13a.25.25 0 0 1-.306-.177Zm12.557-3.365a.25.25 0 0 1 .176-.306l.483-.13a.25.25 0 1 1 .13.483l-.483.13a.25.25 0 0 1-.306-.177ZM3.045 12.944a.299.299 0 0 1-.029-.376l3.898-5.592a.25.25 0 0 1 .062-.062l5.602-3.884a.278.278 0 0 1 .392.392L9.086 9.024a.25.25 0 0 1-.062.062l-5.592 3.898a.299.299 0 0 1-.382-.034l-.005-.006Zm3.143 1.817a.25.25 0 0 1-.176-.306l.129-.483a.25.25 0 0 1 .483.13l-.13.483a.25.25 0 0 1-.306.176ZM9.553 2.204a.25.25 0 0 1-.177-.306l.13-.483a.25.25 0 1 1 .483.13l-.13.483a.25.25 0 0 1-.306.176Z" />
                    </svg>
                </a>
            </div>
        </div>
    </div>


    <div v-show="display_summary_window" class="fullscreen_popover">
        <div class="popover_content">
            <h3>Summary</h3>
            <button @click.prevent="modelSummary" class="close-btn">关闭</button>
            <div class="chat-container">
                <!-- 对话内容 -->
                <div class="chat-content">
                    <!-- 这里放置对话消息 -->
                    <!-- 更多消息 -->
                </div>
            </div>
            <div class="chat-input-container">
                <input type="text" id="chatInput" v-on:keyup.enter="sendMessage" placeholder="输入消息...">
                <button @click="sendMessage" class="send_btn">发送</button>
            </div>
        </div>
    </div>


    <!-- 下方的左右两栏布局 -->
    <div class="container-fluid">
        <div class="row">

            <!-- 左侧栏: 图片+表格 -->
            <div class="col-8">
                <div class="constainer outside_border" style="margin-right: 0 !important;">
                    <div class="container add_bottom_margin" id="tabs">
                        <!-- bootstrap 导航栏 -->
                        <ul class="nav nav-tabs" id="myTab" role="tablist">
                            <li class="nav-item">
                                <a class="nav-link my_text_font active" id="table-tab" data-toggle="tab" href="#table"
                                    role="tab" aria-controls="table" aria-selected="true">Tables</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link my_text_font" id="picture-tab" data-toggle="tab" href="#picture"
                                    role="tab" aria-controls="picture" aria-selected="false">Pictures</a>
                            </li>
                        </ul>
                    </div>
                    <div class="container">
                        <div class="tab-content" id="myTabContent">
                            <!-- 渲染全部表格 -->
                            <div class="tab-pane fade show active" id="table" role="tabpanel" aria-labelledby="table-tab">
                                <div v-if="this.paper_source != 'arxiv'" v-for="key in (this.paper_tables_num)" :key="key">
                                    <h3><span class="badge badge-secondary reform_table_index">Table {{ key }}</span></h3>
                                    <div :id="'table' + (key - 1)" style="overflow-x: auto;"></div>
                                    <br><br>
                                </div>
                            </div>
                            <!-- 渲染全部图片 -->
                            <div class="tab-pane fade" id="picture" role="tabpanel" aria-labelledby="picture-tab">
                                <div v-for="key in (this.paper_pictures_num)" :key="key">
                                    <div class="container my_cont">
                                        <img class="full_screen"
                                            :src="'http://10.80.135.205:8080' + this.paper_pictures[key - 1]">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 右侧栏: 其他元数据+可视化 -->
            <div class="col-4">
                <div class="constainer outside_border" style="margin-left: 0 !important;">
                    <h2>Data + Visualization</h2>
                </div>
            </div>
        </div>
    </div>
</template>
    
<script>
import axios from 'axios';
import ClipboardJS from 'clipboard';
// import Papa from 'papaparse';
// import * as marked from 'marked';
import { marked } from 'marked';
import katex from 'katex';

export default {
    data() {
        return {
            isLogin: false,

            displayTable: true,

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
            paper_url: "NULL",
            paper_affiliation: [],


            display_summary_window: false,
            model_model_type: "NULL",
            model_message: "NULL",
            last_chat_history: {},
            isPopoverVisible: false,

            paper_tables: {},
            paper_tables_num: 0,
            paper_pictures: {},
            paper_pictures_num: 0,

            DEVGPT: {
                "model": "gpt-3.5-turbo",
                "message": [
                    {
                        "role": "system",
                        "content": "The user will give you a url of a paper, you should first read it and then write a summary of it in about 100 words. And then you should help the user with some questions about this paper"
                    },
                    {
                        "role": "user",
                        "content": "Here is the url of the paper: https://arxiv.org/pdf/2210.07349.pdf"
                    },
                    {
                        "role": "assistant",
                        "content": "I apologize, but I am currently unable to access external URLs or download files. However, if you provide me with relevant information or specific questions about the paper, I'll be more than happy to assist you in any way I can."
                    },
                ]
            },
        }
    },

    async mounted() {
        await this.initialize();
    },

    methods: {
        async initialize() {
            await this.checkLogin();
            $(function () {
                $("#tabs").tabs();
            });
            this.paper_id = this.$route.query.id;
            this.paper_source = this.$route.query.source;
            $(function () {
                $('[data-toggle="popover"]').popover();
            });
            this.getPaperInfo();
            if (this.paper_source != "arxiv") {
                this.getTableData();    // 获取全部标签, 并分别加到元素标签上
            };
            this.getPicturesData();
        },

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
                    this.paper_url = response.data.url;
                    this.paper_doi = response.data.doi;
                    for (var i = 0; i < response.data.author.length; i++) {
                        if (this.paper_author.indexOf(response.data.author[i]) == -1)
                            this.paper_author.push(response.data.author[i]);
                    }
                    if (this.paper_source != "arxiv") {
                        for (var i = 0; i < response.data.affiliation.length; i++) {
                            if (this.paper_affiliation.indexOf(response.data.affiliation[i]) == -1)
                                this.paper_affiliation.push(response.data.affiliation[i]);
                        }
                    }
                    console.log("Got paper [" + _ID + "] data");
                })
                .catch((error) => {
                    console.log(error);
                    this.paper_id = "!! ERROR !!";
                });
        },

        SearchAuthor(_name) {
            var _url = "/searchResult?field=author" + "&info=" + encodeURIComponent(_name) + "&source=" + this.search_source;
            window.open(_url, "_blank");
        },

        getTableData() {
            console.log("Begin getting table data of [" + this.paper_id + "]");
            axios.get('http://10.80.135.205:8080/api/v1/paper/tables', {
                params: {
                    id: this.paper_id,
                }
            })
                .then((response) => {
                    this.paper_tables = response.data;
                    this.paper_tables_num = Object.keys(response.data).length;
                    console.log(this.paper_tables);
                    console.log("tables number: " + this.paper_tables_num);
                    for (let i = 0; i < this.paper_tables_num; i++) {
                        this.getSingleTableData(i, this.paper_tables[i]);
                    }
                })
                .catch((error) => {
                    console.log("Something wrong when tables in [" + this.paper_id + "]");
                    console.log(error);
                })
        },

        getPicturesData() {
            console.log("Begin getting picture data of [" + this.paper_id + "]");
            axios.get('http://10.80.135.205:8080/api/v1/paper/pics', {
                params: {
                    id: this.paper_id,
                }
            })
                .then((response) => {
                    this.paper_pictures = response.data;
                    this.paper_pictures_num = Object.keys(response.data).length;
                    // console.log(this.paper_pictures);
                    console.log("pictures number: " + this.paper_pictures_num);
                })
                .catch((error) => {
                    console.log("Something wrong when pictures in [" + this.paper_id + "]");
                    console.log(error);
                })
        },

        getSingleTableData(_i, _url) {
            console.log("begin add table" + _i);
            console.log("url: http://10.80.135.205:8080" + _url);
            axios.get("http://10.80.135.205:8080" + _url)
                .then((response) => {
                    const csvData = response.data;
                    console.log("get single table csv data");
                    // console.log(csvData);

                    // 解析 CSV 数据
                    Papa.parse(csvData, {
                        delimiter: ",", // 指定 CSV 文件中的分隔符
                        header: true, // 第一行作为表头
                        skipEmptyLines: true, // 跳过空行
                        complete: function (results) {
                            const data = results.data;

                            // 创建表格元素
                            const table = document.createElement('table');
                            table.className = "table table-hover full_screen";

                            // 创建表头行
                            const thead = document.createElement('thead');
                            const headerRow = document.createElement('tr');
                            Object.keys(data[0]).forEach(key => {
                                const th = document.createElement('th', { scope: "col" });
                                th.textContent = key;
                                headerRow.appendChild(th);
                            });
                            thead.appendChild(headerRow);
                            table.appendChild(thead);

                            // 创建数据行
                            const tbody = document.createElement('tbody');
                            data.forEach(row => {
                                const dataRow = document.createElement('tr');
                                Object.values(row).forEach(value => {
                                    const td = document.createElement('td');
                                    td.textContent = value;
                                    dataRow.appendChild(td);
                                });
                                tbody.appendChild(dataRow);
                            });
                            table.appendChild(tbody);

                            // 将表格添加到页面中
                            const tableContainer = document.getElementById('table' + _i);
                            console.log("add style to table" + _i);
                            tableContainer.appendChild(table);
                        }
                    })
                })
                .catch((error) => {
                    console.log("get single data when [" + this.paper_id + "] wrong");
                    console.log(error);
                })
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

        togglePopover() {
            this.isPopoverVisible = !this.isPopoverVisible;
        },

        modelSummary() {
            this.display_summary_window = !this.display_summary_window;
            if (this.paper_source != "arxiv") {
                this.addMessageToChat("gpt-message", "暂不支持该论文源, 请查询 Arxiv 论文");
                return;
            }

            axios.get('http://10.80.135.205:8080/api/v1/model/summary', {
                params: {
                    id: this.paper_id,
                    // id: "6569d4442c9d068894e2ac4c",
                    source: this.paper_source,
                }
            })
                .then((response) => {
                    this.last_chat_history = response.data;
                    console.log("set history to: " + this.last_chat_history);
                    this.addMessageToChat("gpt-message", response.data.message[2].content);
                })
                .catch((error) => {
                    console.log(error);
                });

            // 测试
            // this.model_model_type = this.DEVGPT.model;
            // this.model_message = this.DEVGPT.message;
            // this.addMessageToChat("user-message", this.model_message[1].content);
            // this.addMessageToChat("gpt-message", this.model_message[2].content);
        },

        sendMessage() {
            const input = document.getElementById("chatInput");
            const message = input.value;
            input.value = ""; // 清空输入框

            // 将用户消息添加到聊天内容
            console.log("user message: " + message);
            this.addMessageToChat("user-message", message);

            // 调用 GPT 接口获取回复（这里需要您自己实现API调用逻辑）
            // this.getGPTResponse(message).then(response => {
            //     console.log("response: " + response);
            //     this.addMessageToChat("gpt-message", "response 112");
            // });
            this.getGPTResponse(message).then(lastMessageContent => {
                console.log("Last Message Content: ", lastMessageContent);
                this.addMessageToChat("gpt-message", lastMessageContent);
            }).catch(error => {
                console.error("Error occurred: ", error);
            });

        },

        addMessageToChat(type, text) {
            const chatContent = document.querySelector(".chat-content");
            const newMessage = document.createElement("p");
            newMessage.classList.add("chat-message", type);
            newMessage.textContent = text;
            chatContent.appendChild(newMessage);

            // 自动滚动到最新消息
            this.scrollToBottom();
        },

        scrollToBottom() {
            const chatContainer = document.querySelector(".chat-container");
            chatContainer.scrollTop = chatContainer.scrollHeight;
        },
        // 模拟调用 GPT 接口
        // async getGPTResponse(input_message) {
        //     if (this.paper_source != "arxiv") {
        //         return "暂不支持该论文源, 请查询 Arxiv 论文";
        //     }

        //     console.log("question: " + input_message);
        //     console.log("history: " + JSON.stringify(this.last_chat_history));

        //     axios.post('http://10.80.135.205:8080/api/v1/model/qa', {
        //         question: input_message,
        //         history: this.last_chat_history,
        //     })
        //         .then(function (response) {
        //             // this.last_chat_history = response.data;
        //             // console.log("set history in gpt-response to: " + this.last_chat_history);
        //             console.log("response: " + "here before response");
        //             console.log("response: " + response);
        //             return response;
        //         })
        //         .catch((error) => {
        //             console.log(error);
        //             return error;
        //         });
        //     // return "测试--不发送请求";
        // },
        getGPTResponse(input_message) {
            if (this.paper_source != "arxiv") {
                return Promise.resolve("暂不支持该论文源, 请查询 Arxiv 论文");
            }

            console.log("question: " + input_message);
            console.log("history: " + JSON.stringify(this.last_chat_history));

            // Return the Promise here
            return axios.post('http://10.80.135.205:8080/api/v1/model/qa', {
                question: input_message,
                history: this.last_chat_history,
            })
                .then(response => {
                    this.last_chat_history = response.data;
                    console.log("response: ", response);

                    // Extract the content of the last message
                    const messages = response.data.message;
                    const lastMessageContent = messages[messages.length - 1].content;
                    return lastMessageContent;
                })
                .catch(error => {
                    console.error("Error: ", error);
                    return error.message;
                });
        },



        getOriginWebsite() {
            if (this.paper_source == "arxiv") {
                return this.paper_url;
            } else {
                return "https://doi.org/" + this.paper_doi;
            }
        },

        async logOut() {
            axios.get('http://10.80.135.205:8080/api/v1/user/logout')
                .then((response) => {
                    console.log("log out status: " + response.data.logout);
                    this.isLogin = false;

                })
                .catch((error) => {
                    console.log(error);
                });
            await this.initialize();
        },

        async checkLogin() {
            return axios.get('http://10.80.135.205:8080/api/v1/user/check_login')
                .then((response) => {
                    this.isLogin = response.data.login_in;
                    console.log("log in status: " + response.data.login_in);
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        removeKatexHtmlElements() {
            // 获取所有的 span.katex-html 元素
            console.log("remove katex");
            var elements = document.querySelectorAll('span.katex-html');

            // 遍历这些元素并逐个移除
            elements.forEach(function (element) {
                element.parentNode.removeChild(element);
            });
        }
    },

    watch: {
        paperAbstractHTML(newValue, oldValue) {
            // 每当computedData更新时，这个函数将被调用
            this.removeKatexHtmlElements();
        }
    },

    computed: {
        paperAbstractHTML() {
            return marked(this.paper_abstract);
        },

        // htmlText() {
        //     // Split the text into parts that are inside $...$ and parts that are outside
        //     const parts = this.paper_abstract.split(/(\$.*?\$)/g);

        //     // Render the parts that are inside $...$ with katex
        //     const renderedParts = parts.map(part => {
        //         if (part.startsWith('$') && part.endsWith('$')) {
        //             // Remove the $ symbols and render with katex
        //             const latex = part.slice(1, -1).replace(/\$/g, '');
        //             return katex.renderToString(latex);
        //         } else {
        //             // Leave the parts that are outside $...$ unchanged
        //             return part;
        //         }
        //     });

        //     // Join the parts back together
        //     return renderedParts.join('');
        // },

        htmlText() {
            const regex = /(\$\$?[^$]+\$?\$)/g;
            const text = this.paper_abstract;
            let lastIndex = 0;
            let result = '';

            text.replace(regex, (match, tex, index) => {
                result += text.slice(lastIndex, index);
                const latex = tex.slice(tex.startsWith('$$') ? 2 : 1, tex.endsWith('$$') ? -2 : -1);

                // Create a dummy div element to parse the HTML string
                const dummyDiv = document.createElement('div');
                dummyDiv.innerHTML = katex.renderToString(latex, { throwOnError: false });

                // Remove the <span class="katex-html"> element
                const katexHtml = dummyDiv.querySelector('.katex-html');
                if (katexHtml) {
                    katexHtml.remove();
                }

                // Append the modified HTML to the result
                result += dummyDiv.innerHTML;

                lastIndex = index + tex.length;
                return match;
            });

            result += text.slice(lastIndex);


            return result;
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

.popover_content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    height: 100%;
}


.agree-section {
    margin-top: 20px;
}

/* 弹出框内按钮的容器 */
.popover-buttons {
    margin-left: auto;
    /* 将按钮组推到右侧 */
}


/* .popover-content {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    } */

/* 按钮容器的样式 */
.buttons-container {
    margin-top: 20px;
    /* 在内容和按钮之间添加一些空间 */
    align-self: flex-end;
    /* 将按钮组推到右侧 */
}

.centered-text {
    line-height: 30px;
    /* 设置行高为与父元素高度相等 */
    height: 30px;
    /* 设置高度为与父元素相等 */
}

.send_btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
}

.close-btn {
    position: absolute;
    /* 相对于 .fullscreen_popover 定位 */
    top: 15px;
    /* 距离弹窗顶部的距离 */
    right: 15px;
    /* 距离弹窗右侧的距离 */
    padding: 5px 10px;
    /* 按钮内边距，根据需要调整 */
    background: #f5f5f5;
    /* 按钮背景颜色，根据需要调整 */
    border: 1px solid #ddd;
    /* 按钮边框，根据需要调整 */
    cursor: pointer;
    /* 使鼠标悬停时呈现为手型指针 */
    font-size: 15px;
    /* 根据需要调整字体大小 */
    border-radius: 4px;
    /* 如果您希望按钮角是圆的 */
    /* 也可以直接设置宽度和高度 */
    width: 55px;
    /* 根据需要调整宽度 */
    height: 40px;
    /* 根据需要调整高度 */
}

.fullscreen_popover {
    position: fixed;
    /* 固定定位 */
    top: 50%;
    /* 垂直居中 */
    left: 80%;
    /* 水平居中 */
    transform: translate(-50%, -50%);
    /* 调整定位以确保完全居中 */
    width: 400px;
    /* 固定宽度 */
    height: 700px;
    /* 固定高度 */
    background-color: white;
    z-index: 1000;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
}

.popover_content {
    padding: 20px;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    height: 100%;
}

.chat-container {
    flex-grow: 1;
    /* 使聊天内容区域占据剩余空间 */
    overflow-y: auto;
    /* 仅使聊天内容可滚动 */
    padding: 10px;
}

.chat-content {
    padding: 10px;
    /* 内边距 */
}

.chat-message {
    margin-bottom: 10px;
    /* 信息间距 */
    padding: 5px;
    /* 内边距 */
    border-radius: 5px;
    /* 圆角边框 */
}

.user-message {
    background-color: #e0e0e0;
    /* 用户消息背景颜色 */
    text-align: right;
    /* 用户消息右对齐 */
}

.gpt-message {
    background-color: #f0f0f0;
    /* GPT 消息背景颜色 */
    text-align: left;
    /* GPT 消息左对齐 */
}

.chat-input-container {
    display: flex;
    /* 水平布局 */
    padding: 10px;
    /* 内边距 */
}

.table {
    margin: 20px auto;
    border-collapse: collapse;
    width: 80%;
    background-color: #fff;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

.caption {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    padding-bottom: 10px;
}

/* 设置奇偶行的背景色 */
.tr:nth-child(odd) {
    background-color: #f2f2f2;
}

/* 设置表格列的边框样式和文本居中 */
.th,
.td {
    border: 1px solid #ccc;
    text-align: center;
    padding: 8px;
}

#chatInput {
    flex-grow: 1;
    /* 输入框占据剩余空间 */
    margin-right: 10px;
    /* 与发送按钮间距 */
}

.reform_table_index {
    margin-left: 10px !important;
    background-color: #4c8dae !important;
}

.reform_badge_outline {
    color: #2578b5;
    background-color: transparent !important;
    border: solid 1px #2578b5 !important;
    border-color: #2578b5 !important;
    padding: 0.1rem 0.3rem !important;
}

.not {
    display: none;
}

.full_screen {
    width: 100% !important;
}

.my_text_font {
    font-weight: 700 !important;
    color: #2578b5 !important;
}

.outside_border {
    border: 10px solid #dee2e6 !important;
    border-radius: 1rem;
    margin-top: 20px !important;
    margin-right: 20px;
    margin-left: 20px;
    margin-bottom: 50px !important;
    padding: 20px !important;
}

.add_bottom_margin {
    margin-bottom: 20px;
}

.pic_gap {
    border-color: #643441;
    background-color: #643441;
    margin-top: 16px !important;
    margin-bottom: 16px !important;
    padding-top: 3px !important;
    padding-bottom: 3px !important;
}
</style>