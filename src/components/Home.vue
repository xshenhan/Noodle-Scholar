<template>
    <div class="jumbotron jumbotron-lg jumbotron-fluid mb-3 bg-primary position-relative">
        <div class="container text-white h-100 tofront">
            <h1 class="middle_title">你的下一个搜索引擎<br><strong>何必是你的</strong></h1><br>

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
    <a href="http://10.80.135.205:8001/api/v1/paper/download?id=185e7f" class="btn btn-outline-primary btn-round">Download
        PDF</a>


    <h1>Home Page</h1>
    <input type="text" v-model="searchTerm" placeholder="paper id">

    <button @click="SearchId" class="btn btn-outline-primary btn-round">button "SearchResult"</button>
    <br>
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

.middle_title {
    text-align: center;
}

.under_border {
    border-bottom: 10px solid #ff;
}

.btn-rounded {
    border-radius: 20px;
}

.button_white_border {
    border-color: #ffffff !important;
}

.form-control-rounded {
    border-radius: 20px;
}

.search_button_color {
    background-color: #1b54f2 !important;
}

.btn-outline-secondary_rewrite {
    color: #7832e2;
    background-image: none;
    font-weight: bold;
}</style>