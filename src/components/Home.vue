<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a href="/"><img src="/img/N.png" alt="LOGO" width="25px"></a>
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
                <li v-if="this.isLogin" class="nav-item">
                    <span class="nav-link">
                        <a class="btn btn-outline-secondary btn-round fade-down-left" href="/signup">Log out</a>
                    </span>
                </li>
            </ul>


        </div>
    </nav>

    <div class="jumbotron jumbotron-lg jumbotron-fluid mb-0 bg-primary position-relative scratch_high up_padding_small">
        <div class="container text-white h-100 tofront">
            <!-- <img src="https://z1.ax1x.com/2023/11/02/piK4OA0.png" :width="300"> -->
            <h1 class="middle_title">
                NOODLE SCHOLAR <i class="mr-4"></i>
                <img src="../assets/img/N.png" :width="60">
                <i class="mr-4"></i> 开搜未来
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
                    <!-- 第一栏的上侧 -->
                    <div class="col">
                        <div class="home_table_container">
                            <!-- <h4 class="home_table_title text-center">Year Trend</h4> -->
                            <div id="year_paper" style="width: 100%; height: 260px;"></div>
                        </div>
                    </div>
                    <br>
                    <!-- 第一栏的中侧 -->
                    <div class="col">
                        <div class="home_table_container">
                            <!-- <h4 class="home_table_title text-center">Subject Distribution</h4> -->
                            <div id="sub_paper" style="width: 100%; height: 260px;"></div>
                        </div>
                    </div>
                    <br>
                    <!-- 第一栏下侧 -->
                    <div class="col">
                        <div class="home_table_container" v-cloak>
                            <!-- <h4 class="home_table_title text-center">SubDomain Distribution</h4> -->
                            <div id="subsub_paper" style="width: 100%; height: 260px;"></div>
                        </div>
                    </div>
                </div>

                <br>
                <!-- 第二栏 -->
                <div class="col-8">
                    <!-- 第二栏上侧 -->
                    <div class="col">
                        <div class="home_table_container">
                            <h3 class="home_table_title text-center">Author with most Papers</h3>
                            <div id="author_paper" style="width: 100%; height: 300px;"></div>

                            <div class="d-flex justify-content-center">
                                <nav aria-label="nav1" class="my_nav">
                                    <ul class="pagination">
                                        <li class="page-item" :class="{ disabled: activePage_author_paper === 0 }">
                                            <a class="page-link"
                                                @click="changeChart_author_paper(activePage_author_paper - 1)">&laquo;</a>
                                        </li>

                                        <li class="page-item" :class="{ active: activePage_author_paper === index }"
                                            v-for="(item, index) in 5" :key="index">
                                            <a class="page-link" @click="changeChart_author_paper(index)">{{ index + 1
                                            }}</a>
                                        </li>

                                        <li class="page-item" :class="{ disabled: activePage_author_paper === 4 }">
                                            <a class="page-link"
                                                @click="changeChart_author_paper(activePage_author_paper + 1)">&raquo;</a>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        </div>
                    </div>
                    <br>
                    <!-- 第二栏下侧 -->
                    <div class="col">
                        <div class="home_table_container">

                            <div class="modal" v-show="showModal">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title">Subsub Paper Distribution</h5>
                                            <button type="button" class="close" @click="showModal = false">
                                                <span>&times;</span>
                                            </button>
                                        </div>
                                        <div class="modal-body">
                                            <div id="pie-chart" style="width: 100%; height: 400px;"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <button type="button" class="close" @click="closeModal">
                                <span>&times;</span>
                            </button>

                            <h3 class="home_table_title text-center">Subject with most Papers</h3>
                            <div id="sub_paper_bar" style="width: 100%; height: 300px;"></div>

                            <div class="d-flex justify-content-center">
                                <nav aria-label="nav2" class="my_nav">
                                    <ul class="pagination">
                                        <li class="page-item" :class="{ disabled: activePage_subject_paper === 0 }">
                                            <a class="page-link"
                                                @click="changeChart_subject_paper(activePage_subject_paper - 1)">&laquo;</a>
                                        </li>

                                        <li class="page-item" :class="{ active: activePage_subject_paper === index }"
                                            v-for="(item, index) in 5" :key="index">
                                            <a class="page-link" @click="changeChart_subject_paper(index)">{{ index + 1
                                            }}</a>
                                        </li>

                                        <li class="page-item" :class="{ disabled: activePage_subject_paper === 4 }">
                                            <a class="page-link"
                                                @click="changeChart_subject_paper(activePage_subject_paper + 1)">&raquo;</a>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
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
                搜到了就有，<span class="font-weight-bold">没搜到也有。</span>
                <img src="../assets/noodle.svg" width="5%">
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
            <h1 class="display-4 text-right">你的下一个搜索引擎，<br><span class="font-weight-bold">何必是你的。</span></h1>
            <p class="lead text-left">
                用户信息完全泄漏，搜索记录数据库可见。<br><span class="font-weight-bold">你的隐私，我说了算。</span>
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
            isLogin: false,

            component_title: "get Requset",
            already_searched: false,
            paper_id: "NULL id",
            paper_name: "NULL name",

            search_type: "All",
            search_type_print: "all",
            search_info: "",

            agreed: false,
            searchArxiv: false,


            sub_paper: [],
            subsub_paper: [],

            year_paper: [],
            year_paper_chart: null,

            authors_rank: [[1], [2], [3], [4], [5]],
            papers_rank: [[1], [2], [3], [4], [5]],
            activePage_author_paper: 0,
            author_paper_chart: null,

            activePage_subject_paper: 0,
            subject_paper_chart: null,

            showModal: true,
            currentSubPaper: null,
        };
    },

    async mounted() {
        await this.checkLogin();

        await this.getAuthorPapers(0, 50);
        await this.getSubjectPapers_in_arxiv(0, 37);    // 总共 38 个
        await this.getSubsubjectPapers_in_arxiv(0, 175); // 总共 176 个
        await this.getYearPaper();

        $(this.$el).find('[data-toggle="dropdown"]').dropdown();

        this.setYearPaper();
        this.setSubjectPaper();
        this.setSubsubjectPaper();

        this.setYearPaper();
        this.year_paper_chart.on('click', this.searchYear_in_pie);

        this.setAuthorPaper();
        this.author_paper_chart.on('click', this.searchAuthor_in_rank);

        this.setSubjectPaper();
        this.subject_paper_chart.on('click', this.searchSubject_in_rank);
    },


    methods: {
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

        async getYearPaper() {
            return axios.get('http://10.80.135.205:8080/api/v1/vis/paper/year')
                .then((response) => {
                    for (const [key, value] of Object.entries(response.data)) {
                        this.year_paper.push({
                            name: key,
                            value: value
                        });
                    }
                    // console.log(this.year_paper);
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        setYearPaper() {
            this.year_paper_chart = echarts.init(document.getElementById('year_paper'));
            var year_paper_data = this.year_paper;
            year_paper_data.sort(function (a, b) {  // 按照年份排序
                return a.name - b.name;
            });
            var year_paper_option = {
                title: {
                    text: 'Year Trend',
                    left: 'center',
                    top: 'center',
                    textStyle: {
                        color: '#ffffff',
                        fontSize: 20,
                        fontWeight: 'bold',
                    },
                },
                tooltip: {
                    trigger: 'item',
                    position: function (point, params, dom, rect, size) {
                        // point: 鼠标位置
                        // params: 同 formatter 的参数
                        // dom: 提示框的 DOM 对象
                        // rect: 提示框的大小
                        // size: echarts 容器的大小
                        return [point[0] + 10, point[1] - size.contentSize[1] - 10];
                    },
                    formatter: function (params) {
                        let data = params.data; // 获取当前数据项的数据对象
                        return `${data.name} 年 ${data.value} 篇`; // 使用数据对象中的属性值作为数据标签
                    }
                },
                series: [
                    {
                        type: 'pie',
                        label: {
                            show: false
                        },
                        data: year_paper_data,
                        radius: ['70%', '100%']
                    }
                ]
            };
            this.year_paper_chart.setOption(year_paper_option);
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
                        console.log(i + ": " + this.authors_rank[i]);
                        console.log(i + ": " + this.papers_rank[i]);
                    }
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        async getSubjectPapers_in_arxiv(_start, _end) {
            return axios.get("http://10.80.135.205:8080/api/v1/vis/subject/papers?start=0&end=36", {
                params: {
                    start: _start,
                    end: _end
                }
            })
                .then((response) => {
                    for (const [key, value] of Object.entries(response.data)) {
                        this.sub_paper.push({
                            name: value["main_subject"],      // main_subject
                            value: value["num_papers"]    // num_papers
                        });
                    }
                    console.log("get subject papers in arxiv");
                    // console.log(this.sub_paper);
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        async getSubsubjectPapers_in_arxiv(_start, _end) {
            return axios.get("http://10.80.135.205:8080/api/v1/vis/subsubject/papers", {
                params: {
                    start: _start,
                    end: _end
                }
            })
                .then((response) => {
                    for (const [key, value] of Object.entries(response.data)) {
                        this.subsub_paper.push({
                            name: value["sub_subject"],      // sub_subject
                            value: value["num_papers"]    // num_papers
                        });
                    }
                    console.log("get sub-subject papers in arxiv");
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        setSubjectPaper() {
            this.subject_paper_chart = echarts.init(document.getElementById('sub_paper'));
            var sub_paper_data = this.sub_paper;
            sub_paper_data.sort(function (a, b) {  // 按照比例排序
                return a.value - b.value;
            });
            var sub_paper_option = {
                title: {
                    text: 'Subject Distribution',
                    left: 'center',
                    top: 'center',
                    textStyle: {
                        color: '#ffffff',
                        fontSize: 20,
                        fontWeight: 'bold',
                    },
                },
                tooltip: {
                    trigger: 'item',
                    position: function (point, params, dom, rect, size) {
                        return [point[0] + 10, point[1] - size.contentSize[1] - 10];
                    },
                    formatter: function (params) {
                        let data = params.data;
                        return `${data.value} papers in ${data.name}`;
                    }
                },
                series: [
                    {
                        type: 'pie',
                        label: {
                            show: false
                        },
                        data: sub_paper_data,
                        radius: ['70%', '100%']
                    }
                ]
            };
            this.subject_paper_chart.setOption(sub_paper_option);
        },

        setSubsubjectPaper() {
            var subsub_paper_chart = echarts.init(document.getElementById('subsub_paper'));
            var subsub_paper_data = this.subsub_paper;
            subsub_paper_data.sort(function (a, b) {  // 按照比例排序
                return a.value - b.value;
            });
            var subsub_paper_option = {
                title: {
                    text: 'SubDomain Distribution',
                    left: 'center',
                    top: 'center',
                    textStyle: {
                        color: '#ffffff',
                        fontSize: 20,
                        fontWeight: 'bold',
                    },
                },
                tooltip: {
                    trigger: 'item',
                    position: function (point, params, dom, rect, size) {
                        return [point[0] + 10, point[1] - size.contentSize[1] - 10];
                    },
                    formatter: function (params) {
                        let data = params.data;
                        return `${data.value} papers in ${data.name}`;
                    }
                },
                series: [
                    {
                        type: 'pie',
                        label: {
                            show: false
                        },
                        data: subsub_paper_data,
                        radius: ['70%', '100%']
                    }
                ]
            };
            subsub_paper_chart.setOption(subsub_paper_option);
        },

        changeChart_author_paper(index) {
            if (index >= 0 && index < 5) {
                this.activePage_author_paper = index;
                this.setAuthorPaper();
            }
        },

        changeChart_subject_paper(index) {
            // 未完成--按照subject的页面顺序做
            if (index >= 0 && index < 5) {
                this.activePage_subject_paper = index;
                this.setAuthorPaper();
            }
        },

        setAuthorPaper() {
            this.author_paper_chart = echarts.init(document.getElementById('author_paper'));
            this.author_paper_chart.setOption({
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
                    formatter: (params) => {
                        var block = Math.floor((params.name - 1) / 10);
                        var index = (params.name - 1) % 10;
                        return `Author: ${this.authors_rank[block][index]} -- ${params.value} papers`;
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
                    data: this.papers_rank[this.activePage_author_paper].slice(0).reverse(),
                    type: 'bar',
                    itemStyle: {
                        color: '#c3a6cb',
                    },
                }],
            });
        },

        searchAuthor_in_rank(params) {
            console.log(params.name, params.value);
            var block = Math.floor((params.name - 1) / 10);
            var index = (params.name - 1) % 10;
            var _url = "/searchResult?field=author" + "&info=" + encodeURIComponent(this.authors_rank[block][index]) + "&source=" + "arxiv";
            window.open(_url, "_blank");
        },

        searchYear_in_pie(params) {
            // ===============还没改需要 encode 的内容===============
            console.log(params.name, params.value);
            var _url = "/searchResult?field=year" + "&info=" + encodeURIComponent(params.data.name) + "&source=" + "arxiv";
            window.open(_url, "_blank");
        },

        searchSubject_in_rank(params) {
            // ===============还没改需要 encode 的内容===============
            console.log(params.name, params.value);
            var _url = "/searchResult?field=categories" + "&info=" + encodeURIComponent(params.name) + "&source=" + "arxiv";
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
            this.setAuthorPaper();
        },
    },

    computed: {
        yAxisData() {
            let start = this.activePage_author_paper * 10 + 1;
            let end = this.activePage_author_paper * 10 + 10;
            return Array(end - start + 1).fill().map((_, idx) => end - idx);
        }
    },
};
</script>

<!-- 额外样式 -->
<style>
[v-cloak] {
    display: none;
}

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
    padding-bottom: 200px !important;
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