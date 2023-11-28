<template>
    <div class="jumbotron jumbotron-lg jumbotron-fluid mb-0 bg-primary position-relative scratch_high up_padding_small">
        <div class="container text-white h-100 tofront">
            <!-- <img src="https://z1.ax1x.com/2023/11/02/piK4OA0.png" :width="300"> -->
            <h1 class="middle_title">
                NOODLE SCHOLAR &nbsp;
                <!-- <img src="../assets/noodle_yellow.png" :width="50"> -->
                <img src="../assets/img/N标.png" :width="60">
                &nbsp; 开搜未来
            </h1>
            <br><br>
            <h1 class="display-4 middle_title">唯一的不同，<br><span class="font-weight-bold">是处处都不同。</span></h1><br>

            <div class="row align-items-center justify-content-center text-center">
                <div class="col-md-10">

                    <!-- 下拉搜索框 (不带搜索按钮) -->
                    <div class="input-group under_border">
                        <input type="text" class="form-control form-control-rounded" v-model="search_info"
                            aria-label="Text input with dropdown button" :placeholder="`Search by ${search_type}`">
                        <div class="input-group-append">
                            <button class="btn btn-outline-secondary_rewrite dropdown-toggle btn-rounded" type="button"
                                data-toggle="dropdown" aria-expanded="false">{{ search_type }}</button>
                            <div class="dropdown-menu">
                                <a class="dropdown-item" href="#" @click="selectSearchType('All')"><strong>All</strong></a>
                                <div role="separator" class="dropdown-divider"></div>
                                <a class="dropdown-item" href="#"
                                    @click="selectSearchType('Title')"><strong>Title</strong></a>
                                <a class="dropdown-item" href="#"
                                    @click="selectSearchType('Subject')"><strong>Subject</strong></a>
                                <a class="dropdown-item" href="#"
                                    @click="selectSearchType('Author')"><strong>Author</strong></a>
                                <a class="dropdown-item" href="#"
                                    @click="selectSearchType('Journal')"><strong>Journal</strong></a>
                                <a class="dropdown-item" href="#" @click="selectSearchType('DOI')"><strong>DOI</strong></a>
                            </div>
                        </div>
                    </div>

                    <!-- 搜索按钮 -->
                    <button type="button" @click="SearchAndGoToResultPage"
                        class="btn btn-primary btn-lg btn-block btn-rounded button_white_border">Search</button>

                </div>
            </div>
        </div>
    </div>


    <!-- <div class="container">
        <div class="spinner-border text-primary"></div>
    </div> -->



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
                登陆账号管理，个人信息档案，<br>
                并行加速数据，智能内容分析，<br>
                ......&nbsp;&nbsp;&nbsp;&nbsp;<br>
                <span class="font-weight-bold">统统没有。</span>
                <!-- <br><span class="font-weight-bold">轻的，未必更重。</span><br> -->
            </p>
        </div>
    </div>

</template>


<script>
// 6532290ad507ea15ca185e7f

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
        };
    },
    methods: {
        SearchId() {
            this.$router.push("/searchResult" + "?id=" + this.searchTerm);
        },
        SearchAndGoToResultPage() {
            this.$router.push("/searchResult?field=" + this.search_type_print + "&info=" + this.search_info);
        },
        selectSearchType(type) {
            this.search_type = type;
            this.search_type_print = type.toLowerCase();
            console.log("search_type changed to " + type);
            console.log("search_type_print: " + type);
        }
    },
    watch: {
        paper_id: function (val) {
            console.log("paper_id changed to " + val);
        },
        paper_name: function (val) {
            console.log("paper_name changed to " + val);
        }
    }
}
</script>

<!-- 额外样式 -->
<style>
.up_padding_small {
    padding-top: 70px;
}

.middle_title {
    text-align: center;
}

.under_border {
    border-bottom: 10px solid #502c6c;
}

.no_under_margin {
    margin-bottom: 0;
}

.scratch_high {
    padding-bottom: 500px !important;
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
</style>