<template>
    <div class="jumbotron jumbotron-lg jumbotron-fluid mb-0 bg-primary position-relative scratch_high up_padding_small">
        <div class="container text-white h-100 tofront">
            <!-- <img src="https://z1.ax1x.com/2023/11/02/piK4OA0.png" :width="300"> -->
            <h1 class="middle_title">
                NOODLE SCHOLAR &nbsp;
                <!-- <img src="../assets/noodle_yellow.png" :width="50"> -->
                <img src="../assets/img/N.png" :width="60">
                &nbsp; 开搜未来
            </h1>
            <br><br>
            <!-- <h1 class="display-4 middle_title">唯一的不同，<br><span class="font-weight-bold">是处处都不同。</span></h1><br> -->

            <div class="row align-items-center justify-content-center text-center">
                <div class="col-md-10 ">

                    <!-- 上方 -->
                    <div class="input-group under_border form-check-input reform_margin">

                        <!-- Arxiv 选择器 -->
                        <button type="button" class="btn btn_circle_home " :class="{ btn_circle_home_active: this.agreed }"
                            @click="changeAgreement"><strong>Arxiv</strong>
                        </button>

                        <!-- 搜索框 -->
                        <input id="search-input" type="text" class="form-control form-control-rounded no_box_shadow"
                            v-model="search_info" @keyup.enter="SearchAndGoToResultPage"
                            aria-label="Text input with dropdown button" :placeholder="`Search by ${search_type}`">

                        <!-- 搜索条件选择器 -->
                        <!-- BUG: 为什么尖叫向上 && 只能下拉一次菜单 -->
                        <div class="input-group-append">
                            <button class="btn btn-outline-secondary_rewrite dropdown-toggle btn-rounded" type="button"
                                data-toggle="dropdown" aria-expanded="false">{{ search_type }}</button>
                            <div class="dropdown-menu">
                                <a class="dropdown-item" @click="selectSearchType('All')"><strong>All</strong></a>
                                <div role="separator" class="dropdown-divider"></div>
                                <a class="dropdown-item" @click="selectSearchType('Title')"><strong>Title</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('Subject')"><strong>Subject</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('Author')"><strong>Author</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('Journal')"><strong>Journal</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('DOI')"><strong>DOI</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('Abstract')"><strong>Abstract</strong></a>
                            </div>
                        </div>
                    </div>


                    <!-- 下方 -->
                    <!-- 搜索按钮 -->
                    <div class="row col-md-13 reform_margin">
                        <button type="button" @click="SearchAndGoToResultPage"
                            class="btn btn-primary btn-lg btn-block btn-rounded button_white_border">Search</button>

                    </div>
                </div>
            </div>
        </div>

        <br><br><br><br>
        <div class="container">
            <div class="row">
                <!-- 第一栏 -->
                <div class="col-4">
                    <div class="home_table_container">
                        <h3 class="home_table_title text-center">test展示图表</h3>
                        <div id="brand_share" style="width: 100%; height: 100%;"></div>
                    </div>
                </div>

                <!-- 第二栏 -->
                <div class="col-8">
                    <div class="home_table_container">
                        <h3 class="home_table_title text-center">Author with most Papers</h3>
                        <div id="chart" style="width: 100%; height: 300px;"></div>

                        <div class="d-flex justify-content-center">
                            <nav aria-label="nav" class="my_nav">
                                <ul class="pagination">
                                    <li class="page-item" :class="{ disabled: activePage === 0 }">
                                        <a class="page-link" @click="changeChart(activePage - 1)">&laquo;</a>
                                    </li>

                                    <li class="page-item" :class="{ active: activePage === index }"
                                        v-for="(item, index) in 5" :key="index">
                                        <a class="page-link" @click="changeChart(index)">{{ index + 1 }}</a>
                                    </li>

                                    <li class="page-item" :class="{ disabled: activePage === 4 }">
                                        <a class="page-link" @click="changeChart(activePage + 1)">&raquo;</a>
                                    </li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>


            </div>
        </div>
    </div>



    <div class="jumbotron jumbotron-fluid no_under_margin">
        <div class="container">
            <h1 class="display-4"><span class="font-weight-bold">搜</span>不搜在你，<br>准不<span
                    class="font-weight-bold">准</span>在我。</h1>

            <p class="lead text-right">
                无论搜索词是否存在，<span class="font-weight-bold">都给你返回。</span>
                <img src="../assets/noodle.svg" width="5%">
            </p>
        </div>
    </div>


    <div class="jumbotron jumbotron-fluid no_under_margin">
        <div class="container">
            <h1 class="display-4 text-right">你的下一个搜索引擎，<br><span class="font-weight-bold">何必是你的。</span></h1>
            <p class="lead text-left">
                用户信息完全泄漏，搜索记录数据库可见。<br><span class="font-weight-bold">你的隐私，我说了算。</span>
            </p>
        </div>
    </div>


    <div class="jumbotron jumbotron-fluid no_under_margin">
        <div class="container">
            <h1 class="display-4">
                一身<span class="font-weight-bold">轻</span>，<br>
                更举重若轻。
                <br><br>
                <picture>
                    <img class="float-left" src="../assets/img/N标G标.png" width="30%">
                </picture>
            </h1>
            <br>

            <p class="lead text-right">
                全网信息检索，并行加速数据，<br>
                遵循设计模式，周到异常处理，<br><br>
                <!-- ......&nbsp;&nbsp;&nbsp;&nbsp;<br> -->
                <span class="font-weight-bold">统统没有。</span>
            </p>
        </div>
    </div>


    <div class="jumbotron jumbotron-fluid no_under_margin">
        <div class="container">
            <h1 class="display-4 text-right">虽然轻，<br>但<span class="font-weight-bold">代码</span>分量<span
                    class="font-weight-bold">重。</span></h1>
            <p class="lead text-left">
                5个人8个分支，无用代码与有用代码共同管理。<br>
                大小驼峰随意使用，<br>
                <span class="font-weight-bold">生怕你看得懂。</span>
            </p>
        </div>
    </div>


    <div class="jumbotron jumbotron-fluid no_under_margin">
        <div class="container">
            <h1 class="display-4 text-left">全新用户登录协议，<br><span class="font-weight-bold">只许协，<br>不许议。</span></h1>

            <p class="lead text-right">

            </p>
        </div>
    </div>


    <div class="jumbotron jumbotron-fluid no_under_margin">
        <div class="container">
            <h1 class="display-4 text-right"><span class="font-weight-bold">满载动力</span>，<br>满足你的无理。</h1>
            <p class="lead text-left">
                <img src="../assets/img/intel.png" width="10%">
            </p>
        </div>
    </div>
</template>


<script>
// 6532290ad507ea15ca185e7f
// arxiv: 6569d4442c9d068894e2ac4c
import axios from 'axios';
import * as echarts from 'echarts';
// import echarts from 'echarts';
// Vue.prototype.$echarts = echarts;

export default {
    data() {
        return {
            component_title: "get Requset",
            already_searched: false,
            paper_id: "NULL id",
            paper_name: "NULL name",

            search_type: "All",
            search_type_print: "all",
            search_info: "",

            agreed: false,
            searchArxiv: false,

            authors_rank: [[1], [2], [3], [4], [5]],
            papers_rank: [[1], [2], [3], [4], [5]],
            activePage: 0,
            chart: null,
        };
    },

    async mounted() {
        await this.getAuthorPapers(0, 50);
        this.setBrandShare();
        this.chart = echarts.init(document.getElementById('chart'));
        this.setChart();
        this.chart.on('click', this.searchAuthor_in_rank);
    },


    methods: {
        // SearchId() {
        //     this.$router.push("/searchResult" + "?id=" + this.searchTerm);
        // },
        SearchAndGoToResultPage() {
            var url = "/searchResult?field=" + this.search_type_print + "&info=" + encodeURIComponent(this.search_info);
            if (this.searchArxiv) {
                url += "&source=arxiv";
            } else {
                url += "&source=100pdfs";
            }
            this.$router.push(url);
        },

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

        changeAgreement() {
            this.agreed = !this.agreed;
            this.searchArxiv = !this.searchArxiv;
            // console.log("agreed changed to " + this.agreed);
            console.log("searchArxiv changed to " + this.searchArxiv);
        },

        getAutoComplement() {
            var cache = {};
            var search_source = this.searchArxiv ? "arxiv" : "100pdfs";

            $("#search-input").autocomplete({
                minLength: 2,
                source: (request, response) => {
                    var term = request.term;
                    if (term.length < this.minLength) {
                        response([]);
                        return;
                    }
                    // 以前搜索过, 在缓存中直接返回
                    if (term in cache) {
                        response(cache[term]);
                        return;
                    }

                    axios.get('http://10.80.135.205:8080/api/v1/search/autocomplete', {
                        params: {
                            field: this.search_type.toLowerCase(),
                            query: this.search_info,
                            source: search_source,
                        }
                    })
                        .then((response) => {
                            cache[term] = res.data;
                            response(res.data);
                        })
                        .catch((error) => {
                            console.log(error);
                            this.already_searched = true;
                        })
                }
            });
        },

        setBrandShare() {
            var brand_share = echarts.init(document.getElementById('brand_share'));
            var brand_share_option = {
                title: {
                    text: '',
                    left: 'center',
                    top: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    position: "inside",
                    formatter: function (params) {
                        let data = params.data; // 获取当前数据项的数据对象
                        return `销量: ${data.sale}  份额: ${data.value}%`; // 使用数据对象中的属性值作为数据标签
                    }
                },
                series: [
                    {
                        type: 'pie',
                        data: [
                            { value: 8.47, name: '吉利', sale: 18210 },
                            { value: 8.01, name: '大众', sale: 17218 },
                            { value: 6.90, name: '日产', sale: 14841 },
                            { value: 6.34, name: '奇瑞', sale: 13625 },
                            { value: 5.60, name: '丰田', sale: 12035 },
                            { value: 5.26, name: '长安', sale: 11311 },
                            { value: 5.25, name: '奔驰', sale: 11295 },
                            { value: 3.77, name: '奥迪', sale: 8105 },
                            { value: 3.74, name: '宝马', sale: 8039 },
                            { value: 3.47, name: '本田', sale: 7459 },
                            { value: 43.19, name: '其他', sale: 92856 },
                        ],
                        radius: ['50%', '80%']
                    }
                ]
            };
            brand_share.setOption(brand_share_option);
        },

        async getAuthorPapers(_start, _end) {
            return axios.get('http://10.80.135.205:8080/api/v1/vis/author/papers', {
                params: {
                    start: _start,
                    end: _end
                }
            })
                .then((response) => {
                    // 已 10 为一个循环, 将数据分为 5 个组
                    for (let i = 0; i < 5; i++) {
                        this.authors_rank[i] = [];
                        this.papers_rank[i] = [];
                        for (let j = 0; j < 10; j++) {
                            this.authors_rank[i].push(response.data[i * 10 + j].author);
                            this.papers_rank[i].push(response.data[i * 10 + j].num_papers);
                        }
                        // console.log(i + ": " + this.authors_rank[i]);
                        // console.log(i + ": " + this.papers_rank[i]);
                    }
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        changeChart(index) {
            if (index >= 0 && index < 5) {
                this.activePage = index;
                this.setChart();
            }
        },

        setChart() {
            this.chart.setOption({
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow',
                    },
                    position: function (point, params, dom, rect, size) {
                        // point: 鼠标位置
                        // params: 同 formatter 的参数
                        // dom: 提示框的 DOM 对象
                        // rect: 提示框的大小
                        // size: echarts 容器的大小
                        return [point[0] + 10, point[1] - size.contentSize[1] - 10];
                    },
                    formatter: function (params) {
                        return `Author: ${params.name}  ${params.value} papers`;
                    }
                },
                xAxis: {
                    name: "论文数量",
                    type: 'value',
                    axisLine: {
                        lineStyle: {
                            color: '#ffffff',
                            width: 3,
                            type: "solid",
                        },
                    },
                    axisLabel: {
                        margin: 20,
                        rich: {
                            a: {
                                color: '#000',
                                lineHeight: 10,
                            },
                        },
                    },
                },
                yAxis: {
                    name: "排名",
                    type: 'category',
                    // data: this.authors_rank[this.activePage].slice(0).reverse(),
                    data: this.yAxisData,
                    axisLine: {
                        lineStyle: {
                            color: '#fff',
                            width: 15,
                            type: "solid",
                            // shadowColor: "#a1afc9",
                            // shadowOffsetX: 5,
                            // shadowOffsetY: -5,
                        }
                    },
                    axisLabel: {
                        margin: 15,
                        rich: {
                            a: {
                                // 好像这里没什么用
                                color: '#ffffff',
                                fontWeight: 'bold',
                                backgroundColor: '#bacac6',
                                padding: [5, 5, 5, 5],
                                lineHeight: 20,
                            },
                        },
                    },
                },
                series: [{
                    data: this.papers_rank[this.activePage].slice(0).reverse(),
                    type: 'bar',
                    itemStyle: {
                        color: '#801dae',
                    },
                }],
            });
        },

        searchAuthor_in_rank(params) {
            console.log(params.name, params.value);
            var _url = "/searchResult?field=author" + "&info=" + encodeURIComponent(params.name) + "&source=" + "arxiv";
            window.open(_url, "_blank");
        },
    },

    watch: {
        paper_id: function (val) {
            console.log("paper_id changed to " + val);
        },
        paper_name: function (val) {
            console.log("paper_name changed to " + val);
        },

        authors_rank(newData, oldData) {
            this.setChart();
        },
    },

    computed: {
        yAxisData() {
            let start = this.activePage * 10 + 1;
            let end = this.activePage * 10 + 10;
            return Array(end - start + 1).fill().map((_, idx) => end - idx);
        }
    },
};
</script>

<!-- 额外样式 -->
<style>
.up_padding_small {
    padding-top: 70px;
}

.middle_title {
    text-align: center !important;
}

.under_border {
    border-bottom: 10px solid #502c6c;
}

.no_under_margin {
    margin-bottom: 0;
}

.scratch_high {
    padding-bottom: 700px !important;
}

.display_inline {
    display: inline-block !important;
    /* 或者 display: inline-block; */
}

.btn-rounded {
    border-radius: 20px;
}

.button_white_border {
    border-color: #ffffff;
}

.form-control-rounded {
    border-radius: 20px;
}

.search_button_color {
    background-color: #1b54f2;
}

.btn-outline-secondary_rewrite {
    color: #7832e2;
    background-image: none;
    font-weight: bold;
}

.btn_circle_home {
    width: 60px !important;
    height: 38.797px !important;
    border-radius: 20px 0 0 20px !important;
    position: relative !important;
    padding: 0 !important;
    overflow: inherit !important;
    border: none !important;
    background-color: #ffffff;
    color: #7832e2;
}

.btn_circle_home_active {
    background-color: #7832e2 !important;
    color: #ffffff !important;
}

.btn_circle:hover {
    background-color: #7832e2 !important;

}

.no_box_shadow {
    box-shadow: none !important;
}

.reform_margin {
    margin: auto;
}

.home_table_title {
    color: #e9e7ef;
    font-weight: bold;
    border: #e9e7ef 3px solid;
    padding-top: 8px;
    padding-bottom: 8px;
    border-radius: 20px;
}

.my_nav {
    color: #000000;
    font-weight: bold;
}

.home_table_container {
    background-color: #725e82;
    border: 2px solid #e3f9fd;
    border-radius: 10px;
    padding: 20px;
}
</style>