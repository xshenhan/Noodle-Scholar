<template>
    <div>
        <p>Paper information</p>
        <button @click="changeVisible">Display / Hide</button>
        <div v-if="paper_display">
            <p>
                <strong>searching</strong> {{ paper_id }} : <br>
                <strong>《{{ paper_title }}》</strong> <br>
                <strong>Abstract :</strong> {{ paper_abstract }}
            </p>
        </div>
    </div>

</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            search_id: "",
            component_title: "get Requset",
            already_searched: false,
            paper_id: "NULL",
            paper_title: "NULL",
            paper_abstract: "NULL",
            paper_doc_type: "NULL",

            paper_display: true,
        }
    },

    mounted() {
        this.search_id = this.$route.query.id;
        console.log(this.search_id);
        this.search();
    },

    methods: {
        search() {
            axios.get('http://10.80.135.205:8080/api/v1/paper/info', {
                params: {
                    id: this.search_id,
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    console.log(response);
                    this.already_searched = true;
                    this.paper_id = response.data.id;
                    this.paper_title = response.data.title;
                    this.paper_abstract = response.data.abstract;
                    this.paper_doc_type = response.data.doc_type;
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
        },
    }
}
</script>

