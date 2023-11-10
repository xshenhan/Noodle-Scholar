<template>
    <div>
        <p>search</p>
        <p>search {{ paper_id }} : <br>{{ paper_name }} <br> {{ paper_abstract }}</p>
    </div>

    <router-link to="../../index.html">
        <button class="btn btn-default">jump to index.html</button>
    </router-link>


    <div v-if="already_searched">
        <div class="card bg-dark overlay overlay-black text-white shadow-lg border-0">
            <img class="card-img" src="../assets/img/demo/7.jpg" alt="Card image">
            <div class="card-img-overlay d-flex align-items-center text-center">
                <div class="card-body">
                    <h3 class="card-title">Overlay center align</h3>
                    <p class="card-text text-muted">
                        With supporting text below as a natural lead-in to additional content.
                    </p>
                    <a href="#" class="btn btn-info btn-round">Do anything</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            search_id: "6532290ad507ea15ca185e7f",
            component_title: "get Requset",
            already_searched: false,
            paper_id: "",
            paper_title: "",
            paper_abstract: "",
            paper_doc_type: "",

        }
    },

    mounted: {
        search() {
            axios.get('http://10.80.135.205:8001/api/v1/paper/info', {
                params: {
                    id: this.search_id,
                }
            })
                .then((response) => {
                    // 响应数据待处理
                    console.log(response);
                    this.already_searched = true;
                    this.paper_id = response.data.id;
                    this.paper_name = response.data.title;
                    this.paper_abstract = response.data.abstract;
                    this.paper_doc_type = response.data.doc_type;
                })
                .catch((error) => {
                    console.log(error);
                    this.already_searched = true;
                    this.paper_id = "!! ERROR !!";
                });
        }
    }
}
</script>

