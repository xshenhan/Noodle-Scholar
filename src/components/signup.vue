<template>
	<body>
		<div><br><br></div>
		<h1>user {{ this.username }} </h1>
		<div class="container d-flex">
			<div class="row justify-content-center align-self-center w-100">
				<div class="col-md-6">
						<h2 class="text-center">注册</h2>

						<div class="form-group">
							<label for="username">用户名</label>
							<input type="text" class="form-control" id="username" placeholder="用户名" v-model="username">
						</div>

						<div class="form-group">
							<label for="password">密码</label>
							<input type="password" class="form-control" id="password" placeholder="密码" v-model="password">
						</div>

						<button class="btn btn-primary" @click="register">提交</button>
				</div>
			</div>
		</div>
	</body>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			username: "",
			password: "",
		}
	},

	methods: {
		register() {
			axios.get("/api/v1/signup", {
				params: {
					username: this.username,
					password: this.password,
				}
			}).then(res => {
				// console.log(res);

				// let date = new Date();
				// date.setDate(date.getDate() + day);
				// document.cookie = 'selfusr=' + 'try1' + ';selfpwd=' + '12345';
				// const cookie = res;
				console.log("finish login request");
				// console.log(cookie);
				this.$router.push("/");
			})
			.catch((error) => {
                    console.log(error);
                });

		},

		setCookie() {
			let date = new Date();
			date.setDate(date.getDate() + day);
			document.cookie = 'username=' + "try1" + ';password=' + "12345";
		},
	}
}
</script>


<style>
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
</style>