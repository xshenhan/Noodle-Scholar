<template>
    <div>
        <button @click="changeVisible">Display / Hide</button>
        <div v-if="paper_display">
            <p>《<span v-html="paper_title"></span>》        <br>    </p> 
            <p> <strong>Abstract :</strong> {{ paper_abstract }}    </p> 
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            search_field: "",
            search_info: "",

            already_searched: false,
            paper_id: "NULL",
            paper_title: "NULL",
            paper_abstract: "NULL",

            paper_display: true,
        }
    },

    mounted() {
        this.search_field = this.$route.query.field;
        this.search_info = this.$route.query.info;
        console.log("field = " + this.search_field);
        console.log("info = " + this.search_info);
        this.searchInfo();
    },

    methods: {
        
        searchInfo() {
            axios.get('http://10.80.135.205:8001/api/v1/search', {
                params: {
                    field: this.search_field,
                    query: this.search_info,
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    console.log(response);
                    this.already_searched = true;
                    this.paper_id = response.data[0]._id;
                    this.paper_title = response.data[0].title[0];
                    this.paper_abstract = response.data[0].abstract;
                    console.log("finish changing data");
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                });
        },

        changeVisible() {
            this.paper_display = !this.paper_display;
            console.log(this.paper_display);
        }
    }
}
</script>

