    <!-- Paper.vue -->
<template>
    <div class="jumbotron jumbotron-fluid set_margin set_padding">
        <div class="container">
            <h2 class="text-left">{{ this.paper_title }}</h2>
            <br>
            <p class="lead"><span class="badge badge-pill badge-primary">Abstract</span>&nbsp;
                {{ this.paper_abstract }}
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
                </button>

                <!-- <div v-show="display_summary_window" class="fullscreen_popover">
                        <div class="popover_content">
                            <div class="popover_content">
                                <h3>GPT_4</h3>
                                <button @click.prevent="modelSummary" class="close-btn">关闭</button>
                            </div>
                            <div class="popover_content">
                                <p>隐私政策

    生效日期：[填写日期]

    1. 引言

    欢迎您使用我们的服务。我们非常重视您的隐私，并致力于保护您的个人信息。本隐私政策旨在向您解释我们如何收集、使用、披露和保护您的个人信息。请在使用我们的服务之前仔细阅读本政策。

    2. 收集的信息

    在提供服务过程中，我们可能会收集以下类型的个人信息：

    - 姓名
    - 电子邮件地址
    - 联系信息
    - 设备信息（例如，IP地址、浏览器类型、操作系统）
    - 使用情况数据（例如，访问日期和时间、浏览页面、点击信息）
    - 其他根据法律和法规要求的信息

    3. 信息的使用

    我们可能会使用您的个人信息来：

    - 向您提供所请求的服务
    - 处理您的付款
    - 向您发送与服务相关的通知和更新
    - 改进我们的服务
    - 解决争议和解决问题
    - 遵守法律和法规的要求

    4. 信息的披露

    我们不会出售、租赁或以其他方式向第三方披露您的个人信息，除非获得您的明确同意或受法律要求。我们可能会与以下第三方分享您的信息：

    - 与我们合作提供服务的供应商和合作伙伴
    - 法律要求披露信息的情况下

    5. 信息的保护

    我们采取合理的安全措施来保护您的个人信息，以防止未经授权的访问、使用或披露。然而，互联网上的数据传输永远不是100%安全的，因此我们无法保证信息的绝对安全。

    6. 隐私权的选择

    您可以选择提供或不提供个人信息。如果您选择不提供某些信息，可能会影响我们提供的服务。

    7. 隐私政策的变更

    我们可能会不时更新本隐私政策，以反映我们的实践和法律要求的变化。我们将在生效日期前通知您有关更新。请定期查看本政策以了解最新信息。

    8. 联系我们

    如果您对本隐私政策有任何疑问或疑虑，或者希望行使与您的个人信息相关的权利，请通过以下联系方式与我们联系：

    [您的联系信息]

    感谢您阅读我们的隐私政策，我们将继续致力于保护您的隐私和个人信息。</p>
                            </div>
                        </div>

                    </div> -->

            </div>

            <div v-show="display_summary_window" class="fullscreen_popover">
                <div class="popover_content">
                    <h3>GPT_4</h3>
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
        </div>
    </div>

    <!-- 渲染全部表格 (已预加载过全部标签) -->
    <div v-for="key in (this.paper_tables_num)" :key="key">
        <h1><span class="badge badge-secondary reform_table_index">Table {{ key }}</span></h1>
        <div :id="'table' + (key)"></div>
    </div>
</template>
    
<script>
import axios from 'axios';
import ClipboardJS from 'clipboard';
// import Papa from 'papaparse';

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

            display_summary_window: false,
            model_model_type: "NULL",
            model_message: "NULL",
            last_chat_history: {},
            isPopoverVisible: false,

            paper_tables: {},
            paper_tables_num: 0,

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

    mounted() {
        this.paper_id = this.$route.query.id;
        this.paper_source = this.$route.query.source;
        $(function () {
            $('[data-toggle="popover"]').popover();
        });
        this.getPaperInfo();
        this.getTableData();    // 获取全部标签, 并分别加到元素标签上

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
                    console.log("Got paper [" + _ID + "] data");
                })
                .catch((error) => {
                    console.log(error);
                    this.paper_id = "!! ERROR !!";
                });
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
                    console.log("number: " + this.paper_tables_num);
                    for (let i = 0; i < this.paper_tables_num; i++) {
                        this.getSingleTableData(i, this.paper_tables[i]);
                    }
                })
                .catch((error) => {
                    console.log("Something wrong when [" + this.paper_id + "]");
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
                            table.className = "table table-hover";

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
                    this.addMessageToChat("gpt-message", response.data.message[2].content);
                })
                .catch((error) => {
                    console.log(error);
                    this.paper_id = "!! ERROR !!";
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
            this.addMessageToChat("user-message", message);

            // 调用 GPT 接口获取回复（这里需要您自己实现API调用逻辑）
            this.getGPTResponse(message).then(response => {
                this.addMessageToChat("gpt-message", response);
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
        async getGPTResponse(input_message) {
            if (this.paper_source != "arxiv") {
                return "暂不支持该论文源, 请查询 Arxiv 论文";
            }

            console.log("question: " + input_message);
            console.log("history: " + this.last_chat_history);

            axios.post('http://10.80.135.205:8080/api/v1/model/qa', {
                body: {
                    question: input_message,
                    history: this.last_chat_history,
                }
            })
                .then((response) => {
                    this.last_chat_history = response.data;
                    return response.data;
                })
                .catch((error) => {
                    console.log(error);
                    return error;
                });
            // return "测试--不发送请求";
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
    margin-left: 140px !important;
    background-color: #4c8dae !important;
}
</style>