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
                        <a class="nav-link" href="./searchresult?field=all&info=%20&source=100pdfs" style="font-weight: none; font-size: 15px">Search</a>
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
                        <!-- BUG: 为什么只能下拉一次菜单 -->
                        <div class="input-group-append">
                            <button class="btn btn-outline-secondary_rewrite dropdown-toggle btn-rounded" type="button"
                                data-toggle="dropdown" aria-expanded="false">{{ search_type }}</button>
                            <div class="dropdown-menu">
                                <a class="dropdown-item" @click="selectSearchType('All')"><strong>All</strong></a>
                                <div role="separator" class="dropdown-divider"></div>
                                <a class="dropdown-item" @click="selectSearchType('Title')"><strong>Title</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('Subject')"><strong>Subject</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('Author')"><strong>Author</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('Abstract')"><strong>Abstract</strong></a>
                                <a class="dropdown-item" @click="selectSearchType('DOI')"><strong>DOI</strong></a>
                            </div>
                        </div>
                    </div>


                    <!-- 下方 -->
                    <!-- 搜索按钮 -->
                    <div class="row col-md-13 reform_margin">
                        <button type="button" @click="SearchAndGoToResultPage"
                            class="btn btn-primary btn-lg btn-block btn-rounded button_white_border_home">Search</button>

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
                                            v-for="(item, index) in 4" :key="index">
                                            <a class="page-link" @click="changeChart_subject_paper(index)">{{ index + 1
                                            }}</a>
                                        </li>

                                        <li class="page-item" :class="{ disabled: activePage_subject_paper === 3 }">
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
        <!-- Bootstrap modal for sub-subject pie chart -->
        <div class="modal fade" id="subSubjectModal" tabindex="-1" role="dialog" aria-labelledby="modalLabel"
            aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalLabel">Sub-Subject Details</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <!-- Container for the ECharts pie chart -->
                        <div id="subSubjectPieChart" style="width: 500%; height: 400%;"></div>
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

            year_paper: [],
            year_paper_chart: null,

            authors_rank: [[1], [2], [3], [4], [5]],
            papers_rank: [[1], [2], [3], [4], [5]],
            activePage_author_paper: 0,
            author_paper_chart: null,

            sub_paper: [],
            subject_paper_chart: null,

            subsub_paper: [],
            subsub_paper_chart: null,

            main_subject_rank: [[1], [2], [3], [4]],
            subject_papers_rank: [[1], [2], [3], [4]],
            activePage_subject_paper: 0,
            subject_paper_bar_chart: null,

            subsub_paper_bar_chart: null,

            json: {
                "hep-ph": [
                    {
                        "sub_subject": "hep-ph",
                        "full_name": "High Energy Physics - Phenomenology",
                        "num_papers": 175652
                    }
                ],
                "math": [
                    {
                        "sub_subject": "math.CO",
                        "full_name": "Combinatorics",
                        "num_papers": 62691
                    },
                    {
                        "sub_subject": "math.CA",
                        "full_name": "Classical Analysis and ODEs",
                        "num_papers": 21365
                    },
                    {
                        "sub_subject": "math.FA",
                        "full_name": "Functional Analysis",
                        "num_papers": 29626
                    },
                    {
                        "sub_subject": "math.NT",
                        "full_name": "Number Theory",
                        "num_papers": 39835
                    },
                    {
                        "sub_subject": "math.AG",
                        "full_name": "Algebraic Geometry",
                        "num_papers": 50490
                    },
                    {
                        "sub_subject": "math.AT",
                        "full_name": "Algebraic Topology",
                        "num_papers": 14962
                    },
                    {
                        "sub_subject": "math.PR",
                        "full_name": "Probability",
                        "num_papers": 53597
                    },
                    {
                        "sub_subject": "math.NA",
                        "full_name": "Numerical Analysis",
                        "num_papers": 35194
                    },
                    {
                        "sub_subject": "math.RA",
                        "full_name": "Rings and Algebras",
                        "num_papers": 16598
                    },
                    {
                        "sub_subject": "math.OA",
                        "full_name": "Operator Algebras",
                        "num_papers": 12155
                    },
                    {
                        "sub_subject": "math.QA",
                        "full_name": "Quantum Algebra",
                        "num_papers": 18442
                    },
                    {
                        "sub_subject": "math.MP",
                        "full_name": "Mathematical Physics",
                        "num_papers": 76640
                    },
                    {
                        "sub_subject": "math.IT",
                        "full_name": "Information Theory",
                        "num_papers": 44508
                    },
                    {
                        "sub_subject": "math.DG",
                        "full_name": "Differential Geometry",
                        "num_papers": 40499
                    },
                    {
                        "sub_subject": "math.CV",
                        "full_name": "Complex Variables",
                        "num_papers": 16325
                    },
                    {
                        "sub_subject": "math.DS",
                        "full_name": "Dynamical Systems",
                        "num_papers": 34801
                    },
                    {
                        "sub_subject": "math.RT",
                        "full_name": "Representation Theory",
                        "num_papers": 25011
                    },
                    {
                        "sub_subject": "math.GR",
                        "full_name": "Group Theory",
                        "num_papers": 21221
                    },
                    {
                        "sub_subject": "math.AC",
                        "full_name": "Commutative Algebra",
                        "num_papers": 12363
                    },
                    {
                        "sub_subject": "math.SG",
                        "full_name": "Symplectic Geometry",
                        "num_papers": 8734
                    },
                    {
                        "sub_subject": "math.KT",
                        "full_name": "K-Theory and Homology",
                        "num_papers": 5691
                    },
                    {
                        "sub_subject": "math.GT",
                        "full_name": "Geometric Topology",
                        "num_papers": 21988
                    },
                    {
                        "sub_subject": "math.AP",
                        "full_name": "Analysis of PDEs",
                        "num_papers": 58766
                    },
                    {
                        "sub_subject": "math.MG",
                        "full_name": "Metric Geometry",
                        "num_papers": 10674
                    },
                    {
                        "sub_subject": "math.SP",
                        "full_name": "Spectral Theory",
                        "num_papers": 9291
                    },
                    {
                        "sub_subject": "math.ST",
                        "full_name": "Statistics Theory",
                        "num_papers": 21776
                    },
                    {
                        "sub_subject": "math.OC",
                        "full_name": "Optimization and Control",
                        "num_papers": 44895
                    },
                    {
                        "sub_subject": "math.CT",
                        "full_name": "Category Theory",
                        "num_papers": 8074
                    },
                    {
                        "sub_subject": "math.LO",
                        "full_name": "Logic",
                        "num_papers": 12595
                    },
                    {
                        "sub_subject": "math.GM",
                        "full_name": "General Mathematics",
                        "num_papers": 3799
                    },
                    {
                        "sub_subject": "math.GN",
                        "full_name": "General Topology",
                        "num_papers": 4918
                    },
                    {
                        "sub_subject": "math.HO",
                        "full_name": "History and Overview",
                        "num_papers": 3480
                    }
                ],
                "cs": [
                    {
                        "sub_subject": "cs.CG",
                        "full_name": "Computational Geometry",
                        "num_papers": 6487
                    },
                    {
                        "sub_subject": "cs.IT",
                        "full_name": "Information Theory",
                        "num_papers": 44508
                    },
                    {
                        "sub_subject": "cs.NE",
                        "full_name": "Neural and Evolutionary Computing",
                        "num_papers": 13295
                    },
                    {
                        "sub_subject": "cs.AI",
                        "full_name": "Artificial Intelligence",
                        "num_papers": 75694
                    },
                    {
                        "sub_subject": "cs.DS",
                        "full_name": "Data Structures and Algorithms",
                        "num_papers": 22802
                    },
                    {
                        "sub_subject": "cs.CE",
                        "full_name": "Computational Engineering, Finance, and Science",
                        "num_papers": 6334
                    },
                    {
                        "sub_subject": "cs.MS",
                        "full_name": "Mathematical Software",
                        "num_papers": 2117
                    },
                    {
                        "sub_subject": "cs.NA",
                        "full_name": "Numerical Analysis",
                        "num_papers": 21218
                    },
                    {
                        "sub_subject": "cs.CC",
                        "full_name": "Computational Complexity",
                        "num_papers": 10222
                    },
                    {
                        "sub_subject": "cs.DM",
                        "full_name": "Discrete Mathematics",
                        "num_papers": 12699
                    },
                    {
                        "sub_subject": "cs.LO",
                        "full_name": "Logic in Computer Science",
                        "num_papers": 15259
                    },
                    {
                        "sub_subject": "cs.CR",
                        "full_name": "Cryptography and Security",
                        "num_papers": 29579
                    },
                    {
                        "sub_subject": "cs.NI",
                        "full_name": "Networking and Internet Architecture",
                        "num_papers": 20763
                    },
                    {
                        "sub_subject": "cs.LG",
                        "full_name": "Machine Learning",
                        "num_papers": 157532
                    },
                    {
                        "sub_subject": "cs.PF",
                        "full_name": "Performance",
                        "num_papers": 3676
                    },
                    {
                        "sub_subject": "cs.SE",
                        "full_name": "Software Engineering",
                        "num_papers": 14783
                    },
                    {
                        "sub_subject": "cs.AR",
                        "full_name": "Hardware Architecture",
                        "num_papers": 4341
                    },
                    {
                        "sub_subject": "cs.SC",
                        "full_name": "Symbolic Computation",
                        "num_papers": 2401
                    },
                    {
                        "sub_subject": "cs.CY",
                        "full_name": "Computers and Society",
                        "num_papers": 16622
                    },
                    {
                        "sub_subject": "cs.IR",
                        "full_name": "Information Retrieval",
                        "num_papers": 15293
                    },
                    {
                        "sub_subject": "cs.CV",
                        "full_name": "Computer Vision and Pattern Recognition",
                        "num_papers": 108977
                    },
                    {
                        "sub_subject": "cs.OH",
                        "full_name": "Other Computer Science",
                        "num_papers": 2178
                    },
                    {
                        "sub_subject": "cs.DB",
                        "full_name": "Databases",
                        "num_papers": 8125
                    },
                    {
                        "sub_subject": "cs.DL",
                        "full_name": "Digital Libraries",
                        "num_papers": 4601
                    },
                    {
                        "sub_subject": "cs.HC",
                        "full_name": "Human-Computer Interaction",
                        "num_papers": 14975
                    },
                    {
                        "sub_subject": "cs.PL",
                        "full_name": "Programming Languages",
                        "num_papers": 7325
                    },
                    {
                        "sub_subject": "cs.GT",
                        "full_name": "Computer Science and Game Theory",
                        "num_papers": 10554
                    },
                    {
                        "sub_subject": "cs.DC",
                        "full_name": "Distributed, Parallel, and Cluster Computing",
                        "num_papers": 19872
                    },
                    {
                        "sub_subject": "cs.MA",
                        "full_name": "Multiagent Systems",
                        "num_papers": 6944
                    },
                    {
                        "sub_subject": "cs.CL",
                        "full_name": "Computation and Language",
                        "num_papers": 53451
                    },
                    {
                        "sub_subject": "cs.MM",
                        "full_name": "Multimedia",
                        "num_papers": 5793
                    },
                    {
                        "sub_subject": "cs.RO",
                        "full_name": "Robotics",
                        "num_papers": 28198
                    },
                    {
                        "sub_subject": "cs.ET",
                        "full_name": "Emerging Technologies",
                        "num_papers": 3751
                    },
                    {
                        "sub_subject": "cs.GL",
                        "full_name": "General Literature",
                        "num_papers": 210
                    },
                    {
                        "sub_subject": "cs.FL",
                        "full_name": "Formal Languages and Automata Theory",
                        "num_papers": 4701
                    },
                    {
                        "sub_subject": "cs.OS",
                        "full_name": "Operating Systems",
                        "num_papers": 838
                    },
                    {
                        "sub_subject": "cs.SD",
                        "full_name": "Sound",
                        "num_papers": 12529
                    },
                    {
                        "sub_subject": "cs.GR",
                        "full_name": "Graphics",
                        "num_papers": 5302
                    },
                    {
                        "sub_subject": "cs.SY",
                        "full_name": "Systems and Control",
                        "num_papers": 28621
                    },
                    {
                        "sub_subject": "cs.SI",
                        "full_name": "Social and Information Networks",
                        "num_papers": 18607
                    }
                ],
                "physics": [
                    {
                        "sub_subject": "physics.gen-ph",
                        "full_name": "General Physics",
                        "num_papers": 10166
                    },
                    {
                        "sub_subject": "physics.chem-ph",
                        "full_name": "Chemical Physics",
                        "num_papers": 20801
                    },
                    {
                        "sub_subject": "physics.optics",
                        "full_name": "Optics",
                        "num_papers": 43762
                    },
                    {
                        "sub_subject": "physics.comp-ph",
                        "full_name": "Computational Physics",
                        "num_papers": 21469
                    },
                    {
                        "sub_subject": "physics.plasm-ph",
                        "full_name": "Plasma Physics",
                        "num_papers": 15710
                    },
                    {
                        "sub_subject": "physics.space-ph",
                        "full_name": "Space Physics",
                        "num_papers": 6063
                    },
                    {
                        "sub_subject": "physics.ed-ph",
                        "full_name": "Physics Education",
                        "num_papers": 3670
                    },
                    {
                        "sub_subject": "physics.pop-ph",
                        "full_name": "Popular Physics",
                        "num_papers": 2336
                    },
                    {
                        "sub_subject": "physics.soc-ph",
                        "full_name": "Physics and Society",
                        "num_papers": 21116
                    },
                    {
                        "sub_subject": "physics.flu-dyn",
                        "full_name": "Fluid Dynamics",
                        "num_papers": 26509
                    },
                    {
                        "sub_subject": "physics.data-an",
                        "full_name": "Data Analysis, Statistics and Probability",
                        "num_papers": 9980
                    },
                    {
                        "sub_subject": "physics.class-ph",
                        "full_name": "Classical Physics",
                        "num_papers": 8243
                    },
                    {
                        "sub_subject": "physics.bio-ph",
                        "full_name": "Biological Physics",
                        "num_papers": 14597
                    },
                    {
                        "sub_subject": "physics.atom-ph",
                        "full_name": "Atomic Physics",
                        "num_papers": 20315
                    },
                    {
                        "sub_subject": "physics.ao-ph",
                        "full_name": "Atmospheric and Oceanic Physics",
                        "num_papers": 6015
                    },
                    {
                        "sub_subject": "physics.ins-det",
                        "full_name": "Instrumentation and Detectors",
                        "num_papers": 20085
                    },
                    {
                        "sub_subject": "physics.geo-ph",
                        "full_name": "Geophysics",
                        "num_papers": 6701
                    },
                    {
                        "sub_subject": "physics.atm-clus",
                        "full_name": "Atomic and Molecular Clusters",
                        "num_papers": 2661
                    },
                    {
                        "sub_subject": "physics.acc-ph",
                        "full_name": "Accelerator Physics",
                        "num_papers": 7483
                    },
                    {
                        "sub_subject": "physics.hist-ph",
                        "full_name": "History and Philosophy of Physics",
                        "num_papers": 4738
                    },
                    {
                        "sub_subject": "physics.med-ph",
                        "full_name": "Medical Physics",
                        "num_papers": 6407
                    },
                    {
                        "sub_subject": "physics.app-ph",
                        "full_name": "Applied Physics",
                        "num_papers": 16552
                    }
                ],
                "cond-mat": [
                    {
                        "sub_subject": "cond-mat.mes-hall",
                        "full_name": "Mesoscale and Nanoscale Physics",
                        "num_papers": 86893
                    },
                    {
                        "sub_subject": "cond-mat.mtrl-sci",
                        "full_name": "Materials Science",
                        "num_papers": 88039
                    },
                    {
                        "sub_subject": "cond-mat.str-el",
                        "full_name": "Strongly Correlated Electrons",
                        "num_papers": 71240
                    },
                    {
                        "sub_subject": "cond-mat.stat-mech",
                        "full_name": "Statistical Mechanics",
                        "num_papers": 71163
                    },
                    {
                        "sub_subject": "cond-mat.soft",
                        "full_name": "Soft Condensed Matter",
                        "num_papers": 38305
                    },
                    {
                        "sub_subject": "cond-mat.other",
                        "full_name": "Other Condensed Matter",
                        "num_papers": 15380
                    },
                    {
                        "sub_subject": "cond-mat.supr-con",
                        "full_name": "Superconductivity",
                        "num_papers": 41999
                    },
                    {
                        "sub_subject": "cond-mat.dis-nn",
                        "full_name": "Disordered Systems and Neural Networks",
                        "num_papers": 22848
                    },
                    {
                        "sub_subject": "cond-mat.quant-gas",
                        "full_name": "Quantum Gases",
                        "num_papers": 20280
                    },
                    {
                        "sub_subject": "cond-mat",
                        "full_name": "Condensed Matter",
                        "num_papers": 14215
                    }
                ],
                "gr-qc": [
                    {
                        "sub_subject": "gr-qc",
                        "full_name": "General Relativity and Quantum Cosmology",
                        "num_papers": 103494
                    }
                ],
                "astro-ph": [
                    {
                        "sub_subject": "astro-ph",
                        "full_name": "Astrophysics",
                        "num_papers": 105380
                    },
                    {
                        "sub_subject": "astro-ph.HE",
                        "full_name": "High Energy Astrophysical Phenomena",
                        "num_papers": 54703
                    },
                    {
                        "sub_subject": "astro-ph.EP",
                        "full_name": "Earth and Planetary Astrophysics",
                        "num_papers": 27487
                    },
                    {
                        "sub_subject": "astro-ph.SR",
                        "full_name": "Solar and Stellar Astrophysics",
                        "num_papers": 57666
                    },
                    {
                        "sub_subject": "astro-ph.CO",
                        "full_name": "Cosmology and Nongalactic Astrophysics",
                        "num_papers": 64733
                    },
                    {
                        "sub_subject": "astro-ph.IM",
                        "full_name": "Instrumentation and Methods for Astrophysics",
                        "num_papers": 27380
                    },
                    {
                        "sub_subject": "astro-ph.GA",
                        "full_name": "Astrophysics of Galaxies",
                        "num_papers": 60703
                    }
                ],
                "hep-th": [
                    {
                        "sub_subject": "hep-th",
                        "full_name": "High Energy Physics - Theory",
                        "num_papers": 162079
                    }
                ],
                "hep-ex": [
                    {
                        "sub_subject": "hep-ex",
                        "full_name": "High Energy Physics - Experiment",
                        "num_papers": 51928
                    }
                ],
                "nlin": [
                    {
                        "sub_subject": "nlin.PS",
                        "full_name": "Pattern Formation and Solitons",
                        "num_papers": 9397
                    },
                    {
                        "sub_subject": "nlin.CD",
                        "full_name": "Chaotic Dynamics",
                        "num_papers": 15288
                    },
                    {
                        "sub_subject": "nlin.SI",
                        "full_name": "Exactly Solvable and Integrable Systems",
                        "num_papers": 11566
                    },
                    {
                        "sub_subject": "nlin.CG",
                        "full_name": "Cellular Automata and Lattice Gases",
                        "num_papers": 1466
                    },
                    {
                        "sub_subject": "nlin.AO",
                        "full_name": "Adaptation and Self-Organizing Systems",
                        "num_papers": 6907
                    }
                ],
                "q-bio": [
                    {
                        "sub_subject": "q-bio.MN",
                        "full_name": "Molecular Networks",
                        "num_papers": 3604
                    },
                    {
                        "sub_subject": "q-bio.PE",
                        "full_name": "Populations and Evolution",
                        "num_papers": 10962
                    },
                    {
                        "sub_subject": "q-bio.CB",
                        "full_name": "Cell Behavior",
                        "num_papers": 2075
                    },
                    {
                        "sub_subject": "q-bio.QM",
                        "full_name": "Quantitative Methods",
                        "num_papers": 9746
                    },
                    {
                        "sub_subject": "q-bio.OT",
                        "full_name": "Other Quantitative Biology",
                        "num_papers": 1208
                    },
                    {
                        "sub_subject": "q-bio.BM",
                        "full_name": "Biomolecules",
                        "num_papers": 5194
                    },
                    {
                        "sub_subject": "q-bio.NC",
                        "full_name": "Neurons and Cognition",
                        "num_papers": 8914
                    },
                    {
                        "sub_subject": "q-bio.SC",
                        "full_name": "Subcellular Processes",
                        "num_papers": 1659
                    },
                    {
                        "sub_subject": "q-bio.GN",
                        "full_name": "Genomics",
                        "num_papers": 2982
                    },
                    {
                        "sub_subject": "q-bio.TO",
                        "full_name": "Tissues and Organs",
                        "num_papers": 2147
                    },
                    {
                        "sub_subject": "q-bio",
                        "full_name": "Quantitative Biology",
                        "num_papers": 1356
                    }
                ],
                "quant-ph": [
                    {
                        "sub_subject": "quant-ph",
                        "full_name": "Quantum Physics",
                        "num_papers": 141289
                    }
                ],
                "hep-lat": [
                    {
                        "sub_subject": "hep-lat",
                        "full_name": "High Energy Physics - Lattice",
                        "num_papers": 27204
                    }
                ],
                "nucl-th": [
                    {
                        "sub_subject": "nucl-th",
                        "full_name": "Nuclear Theory",
                        "num_papers": 55577
                    }
                ],
                "math-ph": [
                    {
                        "sub_subject": "math-ph",
                        "full_name": "Mathematical Physics",
                        "num_papers": 76640
                    }
                ],
                "nucl-ex": [
                    {
                        "sub_subject": "nucl-ex",
                        "full_name": "Nuclear Experiment",
                        "num_papers": 25030
                    }
                ],
                "stat": [
                    {
                        "sub_subject": "stat.TH",
                        "full_name": "Statistics Theory",
                        "num_papers": 21776
                    },
                    {
                        "sub_subject": "stat.ME",
                        "full_name": "Methodology",
                        "num_papers": 24706
                    },
                    {
                        "sub_subject": "stat.AP",
                        "full_name": "Applications",
                        "num_papers": 17224
                    },
                    {
                        "sub_subject": "stat.CO",
                        "full_name": "Computation",
                        "num_papers": 7710
                    },
                    {
                        "sub_subject": "stat.ML",
                        "full_name": "Machine Learning",
                        "num_papers": 62126
                    },
                    {
                        "sub_subject": "stat.OT",
                        "full_name": "Other Statistics",
                        "num_papers": 1254
                    }
                ],
                "q-fin": [
                    {
                        "sub_subject": "q-fin.CP",
                        "full_name": "Computational Finance",
                        "num_papers": 2234
                    },
                    {
                        "sub_subject": "q-fin.PR",
                        "full_name": "Pricing of Securities",
                        "num_papers": 1908
                    },
                    {
                        "sub_subject": "q-fin.RM",
                        "full_name": "Risk Management",
                        "num_papers": 2123
                    },
                    {
                        "sub_subject": "q-fin.GN",
                        "full_name": "General Finance",
                        "num_papers": 2569
                    },
                    {
                        "sub_subject": "q-fin.ST",
                        "full_name": "Statistical Finance",
                        "num_papers": 3413
                    },
                    {
                        "sub_subject": "q-fin.PM",
                        "full_name": "Portfolio Management",
                        "num_papers": 1745
                    },
                    {
                        "sub_subject": "q-fin.TR",
                        "full_name": "Trading and Market Microstructure",
                        "num_papers": 1659
                    },
                    {
                        "sub_subject": "q-fin.EC",
                        "full_name": "Economics",
                        "num_papers": 4112
                    },
                    {
                        "sub_subject": "q-fin.MF",
                        "full_name": "Mathematical Finance",
                        "num_papers": 2358
                    }
                ],
                "econ": [
                    {
                        "sub_subject": "econ.EM",
                        "full_name": "Econometrics",
                        "num_papers": 3208
                    },
                    {
                        "sub_subject": "econ.TH",
                        "full_name": "Theoretical Economics",
                        "num_papers": 2139
                    },
                    {
                        "sub_subject": "econ.GN",
                        "full_name": "General Economics",
                        "num_papers": 3545
                    }
                ],
                "eess": [
                    {
                        "sub_subject": "eess.SY",
                        "full_name": "Systems and Control",
                        "num_papers": 20166
                    },
                    {
                        "sub_subject": "eess.IV",
                        "full_name": "Image and Video Processing",
                        "num_papers": 20617
                    },
                    {
                        "sub_subject": "eess.AS",
                        "full_name": "Audio and Speech Processing",
                        "num_papers": 13017
                    },
                    {
                        "sub_subject": "eess.SP",
                        "full_name": "Signal Processing",
                        "num_papers": 24683
                    }
                ],
                "acc-phys": [
                    {
                        "sub_subject": "acc-phys",
                        "full_name": "Accelerator Physics",
                        "num_papers": 49
                    }
                ],
                "adap-org": [
                    {
                        "sub_subject": "adap-org",
                        "full_name": "Adaptation, Noise, and Self-Organizing Systems",
                        "num_papers": 584
                    }
                ],
                "chao-dyn": [
                    {
                        "sub_subject": "chao-dyn",
                        "full_name": "Chaotic Dynamics",
                        "num_papers": 2398
                    }
                ],
                "patt-sol": [
                    {
                        "sub_subject": "patt-sol",
                        "full_name": "Pattern Formation and Solitons",
                        "num_papers": 650
                    }
                ],
                "dg-ga": [
                    {
                        "sub_subject": "dg-ga",
                        "full_name": "Differential Geometry",
                        "num_papers": 732
                    }
                ],
                "solv-int": [
                    {
                        "sub_subject": "solv-int",
                        "full_name": "Exactly Solvable and Integrable Systems",
                        "num_papers": 1413
                    }
                ],
                "bayes-an": [
                    {
                        "sub_subject": "bayes-an",
                        "full_name": "Bayesian Analysis",
                        "num_papers": 16
                    }
                ],
                "comp-gas": [
                    {
                        "sub_subject": "comp-gas",
                        "full_name": "Cellular Automata and Lattice Gases",
                        "num_papers": 221
                    }
                ],
                "alg-geom": [
                    {
                        "sub_subject": "alg-geom",
                        "full_name": "Algebraic Geometry",
                        "num_papers": 1423
                    }
                ],
                "funct-an": [
                    {
                        "sub_subject": "funct-an",
                        "full_name": "Functional Analysis",
                        "num_papers": 427
                    }
                ],
                "q-alg": [
                    {
                        "sub_subject": "q-alg",
                        "full_name": "Quantum Algebra and Topology",
                        "num_papers": 1578
                    }
                ],
                "ao-sci": [
                    {
                        "sub_subject": "ao-sci",
                        "full_name": "Atmospheric-Oceanic Sciences",
                        "num_papers": 17
                    }
                ],
                "atom-ph": [
                    {
                        "sub_subject": "atom-ph",
                        "full_name": "Atomic, Molecular and Optical Physics",
                        "num_papers": 123
                    }
                ],
                "chem-ph": [
                    {
                        "sub_subject": "chem-ph",
                        "full_name": "Chemical Physics",
                        "num_papers": 251
                    }
                ],
                "plasm-ph": [
                    {
                        "sub_subject": "plasm-ph",
                        "full_name": "Plasma Physics",
                        "num_papers": 38
                    }
                ],
                "mtrl-th": [
                    {
                        "sub_subject": "mtrl-th",
                        "full_name": "Materials Theory",
                        "num_papers": 262
                    }
                ],
                "cmp-lg": [
                    {
                        "sub_subject": "cmp-lg",
                        "full_name": "Computation and Language",
                        "num_papers": 894
                    }
                ],
                "supr-con": [
                    {
                        "sub_subject": "supr-con",
                        "full_name": "Superconductivity",
                        "num_papers": 175
                    }
                ]
            }
        };
    },

    async mounted() {
        await this.initialize();
    },


    methods: {
        async initialize() {
            await this.checkLogin();

            await this.getAuthorPapers(0, 50);
            await this.getSubjectPapers_in_arxiv(0, 37);    // 总共 38 个
            await this.getSubsubjectPapers_in_arxiv(0, 175); // 总共 176 个
            await this.getYearPaper();

            $(this.$el).find('[data-toggle="dropdown"]').dropdown();

            this.setYearPaper();
            this.year_paper_chart.on('click', this.searchYear_in_pie);

            this.setAuthorPaper();
            this.author_paper_chart.on('click', this.searchAuthor_in_rank);

            this.setSubjectPaper();

            this.setSubsubjectPaper();
            this.subsub_paper_chart.on('click', this.searchSubsubject_in_rank);

            this.setSubjectPaperBar();
            this.subject_paper_bar_chart.on('click', this.showSubsubject_in_bar);
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

                    axios.get('/api/v1/search/autocomplete', {
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
            return axios.get('/api/v1/vis/paper/year')
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
            return axios.get('/api/v1/vis/author/papers', {
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
            return axios.get("/api/v1/vis/subject/papers?start=0&end=36", {
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

                    // 以 10 为一个循环, 将数据分为 4 组
                    for (let i = 0; i < 4; i++) {
                        this.main_subject_rank[i] = [];
                        this.subject_papers_rank[i] = [];
                        for (let j = 0; j < 10; j++) {
                            // 如果索引大于 37 就跳出循环
                            // BUG: 如果把最后一组 index==37 加上就会报错, 只能这里特判
                            if (i * 10 + j >= 37) {
                                this.main_subject_rank[i].push("bayes-an");
                                this.subject_papers_rank[i].push(Math.max(0, -(10 * i + j - 38) * 16));
                                continue;
                            }
                            this.main_subject_rank[i].push(response.data[i * 10 + j].main_subject);
                            this.subject_papers_rank[i].push(response.data[i * 10 + j].num_papers);
                        }
                    }
                    console.log("main_subject: " + this.main_subject_rank);
                    console.log("subject_papers: " + this.subject_papers_rank);
                })
                .catch((error) => {
                    console.log(error);
                })
        },

        async getSubsubjectPapers_in_arxiv(_start, _end) {
            return axios.get("/api/v1/vis/subsubject/papers", {
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
            this.subsub_paper_chart = echarts.init(document.getElementById('subsub_paper'));
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
            this.subsub_paper_chart.setOption(subsub_paper_option);
        },

        changeChart_author_paper(index) {
            if (index >= 0 && index < 5) {
                this.activePage_author_paper = index;
                this.setAuthorPaper();
            }
        },

        changeChart_subject_paper(index) {
            if (index >= 0 && index < 4) {
                this.activePage_subject_paper = index;
                this.setSubjectPaperBar();
            }
        },

        setSubjectPaperBar() {
            this.subject_paper_bar_chart = echarts.init(document.getElementById('sub_paper_bar'));
            this.subject_paper_bar_chart.setOption({
                tooltip: {
                    trigger: 'item',
                    axisPointer: {
                        type: 'shadow',
                    },
                    position: function (point, params, dom, rect, size) {
                        return [point[0] + 10, point[1] - size.contentSize[1] - 10];
                    },
                    formatter: (params) => {
                        var block = Math.floor((params.name - 1) / 10);
                        var index = (params.name - 1) % 10;
                        return `${params.value} papers in ${this.main_subject_rank[block][index]}`;
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
                    name: "领域",
                    type: 'category',
                    data: this.subject_data_to_rank,
                    axisLine: {
                        lineStyle: {
                            color: '#fff',
                            width: 1,
                            type: "solid",
                        }
                    },
                    axisLabel: {
                        margin: 15,
                        rich: {
                            a: {
                                // 好像这里没什么用
                            },
                        },
                    },
                },

                series: [{
                    data: this.subject_papers_rank[this.activePage_subject_paper].slice(0).reverse(),
                    type: 'bar',
                    itemStyle: {
                        color: '#c3a6cb',
                    },
                }],
            });
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
                    data: this.author_data_to_rank,
                    axisLine: {
                        lineStyle: {
                            color: '#fff',
                            // y轴的线条宽度
                            width: 1,
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
            console.log(params.name, params.value);
            var _url = "/searchResult?field=all" + "&info=the" + "&source=arxiv" + "&start_year=" + params.name + "&end_year=" + params.name;
            window.open(_url, "_blank");
        },

        searchSubsubject_in_rank(params) {
            console.log(params.name, params.value);
            var _url = "/searchResult?field=tag" + "&info=" + encodeURIComponent(params.name) + "&source=" + "arxiv";
            window.open(_url, "_blank");
        },

        searchSubsubject_in_pie(params) {
            console.log(params.name, params.value);
            var _url = "/searchResult?field=tag" + "&info=" + encodeURIComponent(params.data.sub_subject) + "&source=" + "arxiv";
            window.open(_url, "_blank");
        },

        showSubsubject_in_bar(params) {
            // 弹窗展示该 subject 的所有 sub-subject 的数据
            $('#subSubjectModal').modal('show');

            // Find the selected main subject
            const mainSubject = this.main_subject_rank[Math.floor((params.name - 1) / 10)][(params.name - 1) % 10];

            // Get the data for the sub-subjects
            const subSubjectsData = this.json[mainSubject];

            // Map the data to the format ECharts expects for pie charts
            const pieChartData = subSubjectsData.map(sub => ({
                name: sub.full_name,
                value: sub.num_papers,
                sub_subject: sub.sub_subject
            }));

            let subSubjectPieChart = echarts.init(document.getElementById('subSubjectPieChart'));

            subSubjectPieChart.setOption({
                legend: {
                    show: false // 不显示图例
                },
                title: {
                    text: '',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item'
                },
                series: [
                    {
                        name: 'Number of Papers',
                        type: 'pie',
                        radius: '50%',
                        data: pieChartData,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            });

            subSubjectPieChart.on('click', this.searchSubsubject_in_pie);
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
        author_data_to_rank() {
            let start = this.activePage_author_paper * 10 + 1;
            let end = this.activePage_author_paper * 10 + 10;
            return Array(end - start + 1).fill().map((_, idx) => end - idx);
        },

        subject_data_to_rank() {
            let start = this.activePage_subject_paper * 10 + 1;
            let end = this.activePage_subject_paper * 10 + 10;
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

.button_white_border_home {
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