<template>
	<body>
		<div><br><br></div>
		<!-- <div class="container d-flex">
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
		</div> -->
		<div class="container">
			<h2>Signup</h2>
			<form id="signupForm">
				<div class="mb-3">
					<label for="username" class="form-label">Username</label>
					<input type="text" class="form-control" id="username" name="username" required v-model="username">
				</div>
				<div class="mb-3">
					<label for="password" class="form-label">Password</label>
					<input type="password" class="form-control" id="password" name="password" required v-model="password">
				</div>
				<div class="cf-turnstile" data-sitekey="0x4AAAAAAAOBU1BK4T3OQONj" data-callback="javascriptCallback"></div>

				<!-- 提交按钮 -->
				<button type="submit" class="btn btn-primary" :disabled="!this.agreed">Submit</button>
				&nbsp;&nbsp;&nbsp;
				<!-- 是否同意协议 -->
				<button type="button" class="btn btn-outline-primary btn_circle" :class="{ active: this.agreed }" @click="changeAgreement">
					<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-check-square inner_btn_check" viewBox="0 0 16 16">
						<path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
						<path d="M10.97 4.97a.75.75 0 0 1 1.071 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.235.235 0 0 1 .02-.022z"/>
					</svg>
				</button>

		</form>
		<div id="responseMessage" class="mt-3"></div>
		</div>

		<!-- light footer -->
		<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
			x="0px" y="0px" viewBox="0 0 1440 126" style="enable-background:new 0 0 1440 126;" xml:space="preserve">
			<path class="bg-light" d="M685.6,38.8C418.7-11.1,170.2,9.9,0,30v96h1440V30C1252.7,52.2,1010,99.4,685.6,38.8z">
			</path>
		</svg>
		<footer class="bg-light pb-5">
			<div class="container">
				<div class="row">
					<div class="col-12 col-md mr-4">
						<i class="fas fa-copyright text-dark"></i>
						<small class="d-block mt-3 mb-3 text-muted">© 2021 Anchor Bootstrap</small>
					</div>
					<div class="col-6 col-md">
						<h5 class="mb-4 text-dark">Features</h5>
						<ul class="list-unstyled text-small">
							<li><a class="text-muted" href="#">Cool stuff</a></li>
							<li><a class="text-muted" href="#">Random feature</a></li>
							<li><a class="text-muted" href="#">Team feature</a></li>
							<li><a class="text-muted" href="#">Stuff for developers</a></li>
						</ul>
					</div>
					<div class="col-6 col-md">
						<h5 class="mb-4 text-dark">Resources</h5>
						<ul class="list-unstyled text-small">
							<li><a class="text-muted" href="#">Resource</a></li>
							<li><a class="text-muted" href="#">Resource name</a></li>
							<li><a class="text-muted" href="#">Another resource</a></li>
							<li><a class="text-muted" href="#">Final resource</a></li>
						</ul>
					</div>
					<div class="col-6 col-md">
						<h5 class="mb-4 text-dark">Utilities</h5>
						<ul class="list-unstyled text-small">
							<li><a class="text-muted" href="#">Business</a></li>
							<li><a class="text-muted" href="#">Education</a></li>
							<li><a class="text-muted" href="#">Government</a></li>
							<li><a class="text-muted" href="#">Gaming</a></li>
						</ul>
					</div>
					<div class="col-6 col-md">
						<h5 class="mb-4 text-dark">About</h5>
						<ul class="list-unstyled text-small">
							<li><a class="text-muted" href="#">Team</a></li>
							<li><a class="text-muted" href="#">Locations</a></li>
							<li><a class="text-muted" href="#">Privacy</a></li>
							<li><a class="text-muted" href="#">Terms</a></li>
						</ul>
					</div>
				</div>
			</div>
		</footer>

	</body>
</template>

<script>
import axios from 'axios';

export default {
	data() {
		return {
			username: "",
			password: "",
			agreed: false,
			isActive: false,
		}
	},

	mounted() {
		document.getElementById('signupForm').addEventListener('submit', function (event) {
			event.preventDefault();

			const formData = new FormData(this);

			fetch('/api/v1/signup', {
				method: 'POST',
				body: formData
			})
				.then(response => response.text())
				.then(text => {
					document.getElementById('responseMessage').textContent = text;
				})
				.catch((error) => {
					console.error('Error:', error);
					document.getElementById('responseMessage').textContent = 'Error: ' + error;
				});
		});
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

		// _submit() {
		// 	if (this.agreed) {
		// 		console.log("agree policy.")
		// 	} else {
		// 		this.$bvPopover.show('popover');
		// 	}
		// }

		changeAgreement() {
			this.agreed = !this.agreed;
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

.middle_title {
	text-align: center;
}

.no_under_margin {
	margin-bottom: 0;
}


.btn_circle {
	width: 36.781px;
	height: 36.781px;
	border-radius: 10%;
	position: relative;
	padding: 0;
	overflow: visible;
	border: none;
}

.btn_circle :active {
	border: 10px solid white;
}

.btn_circle span {
	position: absolute;
	top: 50%;
	left: 50%;
}

.inner_btn_check {
	width: 34.781px;
	height: 34.781px;
	position: relative !important;
}
</style>