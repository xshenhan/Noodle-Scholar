<template>
	<body>
		<div><br><br></div>
		<div class="container">
			<h2>Login Form</h2>
			<form id="loginForm">
				<div class="mb-3">
					<label for="username" class="form-label">Username</label>
					<input type="text" class="form-control" id="username" name="username" required v-model="username">
				</div>
				<div class="mb-3">
					<label for="password" class="form-label">Password</label>
					<input type="password" class="form-control" id="password" name="password" required v-model="password">
				</div>
				<div class="cf-turnstile" data-sitekey="0x4AAAAAAAOBU1BK4T3OQONj" data-callback="javascriptCallback"></div>
				<button type="submit" class="btn btn-primary">Submit</button>
			</form>
			<button type="button" class="btn btn-primary">Primary</button>
			<div id="responseMessage" class="mt-3"></div>
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

	mounted() {
		document.getElementById('loginForm').addEventListener('submit', function (event) {
			event.preventDefault();

			const formData = new FormData(this);

			fetch('/api/v1/user/login', {
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