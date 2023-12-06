<template>
	<body>

		<!-- <div class="login-background"> -->
		<div><br></div>



		<div class="container resize">
			<div class="middle_title">
				<h2>Log in</h2>
			</div>
			<div><br></div>
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


				<!-- 是否同意协议 -->
				<div class="container2">
					<div class="button-with-text">
						<button type="button" class="btn btn-outline-primary btn_circle_login"
							:class="{ btn_circle_login_active: this.agreed }" @click="changeAgreement">
							<svg v-if="agreed" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
								class="bi bi-check-square inner_btn_check" viewBox="0 0 30 30">
								<path
									d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z" />
								<path
									d="M10.97 4.97a.75.75 0 0 1 1.071 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.235.235 0 0 1 .02-.022z" />
							</svg>
						</button>
						&nbsp;&nbsp;&nbsp;
						<span class="centered-text">请被迫接收<a href="#" @click.prevent="togglePopover">用户协议</a></span>
						&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

					</div>
				</div>


				<div><br></div>
				<!-- 提交按钮 -->
				<div class="submit_button">
					<button type="submit" class="btn btn-primary submit_btn_longer" :disabled="!this.agreed">Submit</button>
				</div>


			</form>
			<div id="responseMessage" class="mt-3"></div>
		</div>


		<!-- </div> -->


		<!-- 全屏弹出框 -->
		<div v-if="isPopoverVisible" class="fullscreen-popover">
			<div class="popover-content">
				<p>隐私政策

					生效日期：[填写日期]

					1. 引言

					欢迎您使用我们的服务。我们非常重视您的隐私，并致力于保护您的个人信息。本隐私政策旨在向您解释我们如何收集、使用、披露和保护您的个人信息。请在使用我们的服务之前仔细阅读本政策。

					2. 收集的信息

					在提供服务过程中，我们可能会收集以下类型的个人信息：

					- 姓名
					- 电子邮件地址
					- 联系信息
					- 设备信息（例如，IP地址、浏览器类型、操作系统）
					- 使用情况数据（例如，访问日期和时间、浏览页面、点击信息）
					- 其他根据法律和法规要求的信息

					3. 信息的使用

					我们可能会使用您的个人信息来：

					- 向您提供所请求的服务
					- 处理您的付款
					- 向您发送与服务相关的通知和更新
					- 改进我们的服务
					- 解决争议和解决问题
					- 遵守法律和法规的要求

					4. 信息的披露

					我们不会出售、租赁或以其他方式向第三方披露您的个人信息，除非获得您的明确同意或受法律要求。我们可能会与以下第三方分享您的信息：

					- 与我们合作提供服务的供应商和合作伙伴
					- 法律要求披露信息的情况下

					5. 信息的保护

					我们采取合理的安全措施来保护您的个人信息，以防止未经授权的访问、使用或披露。然而，互联网上的数据传输永远不是100%安全的，因此我们无法保证信息的绝对安全。

					6. 隐私权的选择

					您可以选择提供或不提供个人信息。如果您选择不提供某些信息，可能会影响我们提供的服务。

					7. 隐私政策的变更

					我们可能会不时更新本隐私政策，以反映我们的实践和法律要求的变化。我们将在生效日期前通知您有关更新。请定期查看本政策以了解最新信息。

					8. 联系我们

					如果您对本隐私政策有任何疑问或疑虑，或者希望行使与您的个人信息相关的权利，请通过以下联系方式与我们联系：

					[您的联系信息]

					感谢您阅读我们的隐私政策，我们将继续致力于保护您的隐私和个人信息。
				</p>

				<div class="popover-buttons">
					<button @click="toggleAccept" class="button-agree">我已阅读并同意</button>
					<button @click="toggleNotAccept" class="button-cancel">取消</button>
				</div>

			</div>
		</div>




		<!-- light footer -->
		<!-- <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 1440 126" style="enable-background:new 0 0 1440 126;" xml:space="preserve">
		<path class="bg-light" d="M685.6,38.8C418.7-11.1,170.2,9.9,0,30v96h1440V30C1252.7,52.2,1010,99.4,685.6,38.8z"></path>
		</svg> -->
		<footer class="bg-light pb-5 foot-container">
			<div>
				<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"
					xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 1440 126"
					style="enable-background:new 0 0 1440 126;" xml:space="preserve" class="footer-svg">
					<path class="bg-light"
						d="M685.6,38.8C418.7-11.1,170.2,9.9,0,30v96h1440V30C1252.7,52.2,1010,99.4,685.6,38.8z">
					</path>
				</svg>

			</div>
			<div class="container">
				<div class="row justify-content-center">
					<div class="col-12">
						<h3 class="middle_title">
							NOODLE SCHOLAR &nbsp;
							<img src="../assets/img/N.png" :width="40">
							&nbsp; 开搜未来
						</h3>
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
			isPopoverVisible: false,
		}
	},

	mounted() {
		document.getElementById('loginForm').addEventListener('submit', function (event) {
			event.preventDefault();

			const formData = new FormData(this);

			fetch('/api/v1/login', {
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
			axios.get("/api/v1/login", {
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


		changeAgreement() {
			this.agreed = !this.agreed;
		},

		togglePopover() {
			this.isPopoverVisible = !this.isPopoverVisible;
		},
		toggleAccept() {
			this.isPopoverVisible = !this.isPopoverVisible;
			this.agreed = true;
		},
		toggleNotAccept() {
			this.isPopoverVisible = !this.isPopoverVisible;
			this.agreed = false;
		}

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
	text-align: center !important;
}

.no_under_margin {
	margin-bottom: 0;
}


.btn_circle_login {
	width: 20.781px;
	height: 20.781px;
	border-radius: 10%;
	position: relative;
	padding: 0;
	overflow: visible;
	border: 1px solid #000000;
	box-shadow: none !important;
}

.btn_circle_login_active {
	border: 1px solid white;
	box-shadow: none !important;
}


.inner_btn_check {
	width: 20.781px;
	height: 20.781px;
	position: relative !important;
}

.resize {
	width: 30%;
	height: 150%;
	margin: 0 auto;
	padding-bottom: 150px;
	/* 足够覆盖 footer 的高度 */
}

.button-with-text {
	display: flex;
	align-items: center;
}

.submit_button {
	display: flex;
	justify-content: center;
}


.fullscreen-popover {
	position: fixed;
	/* 固定定位 */
	top: 50%;
	/* 垂直居中 */
	left: 50%;
	/* 水平居中 */
	transform: translate(-50%, -50%);
	/* 调整定位以确保完全居中 */
	width: auto;
	/* 或者设定具体宽度 */
	height: auto;
	/* 或者设定具体高度 */
	background-color: white;
	z-index: 1000;
	box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}


.popover-content {
	background-color: white;
	padding: 20px;
	border-radius: 10px;
	box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}


.agree-section {
	margin-top: 20px;
}

/* 自定义复选框样式
input[type="checkbox"] {
    accent-color: green; /* 设置复选框的主题颜色 
}

自定义标签样式 
label {
    margin-left: 8px;
} */
/*
.popover-content {
    display: flex;  使用 Flexbox 
    justify-content: space-between;  内容两侧对齐 
    align-items: center;  垂直居中 
}
*/
/* 弹出框内按钮的容器 */
.popover-buttons {
	margin-left: auto;
	/* 将按钮组推到右侧 */
}


.popover-content {
	/* 其他样式 */
	display: flex;
	flex-direction: column;
	/* 子元素垂直排列 */
	align-items: flex-start;
	/* 子元素向左对齐 */
}

/* 按钮容器的样式 */
.buttons-container {
	margin-top: 20px;
	/* 在内容和按钮之间添加一些空间 */
	align-self: flex-end;
	/* 将按钮组推到右侧 */
}

/* “我已阅读并同意”按钮的样式 */
.button-agree {
	background-color: black;
	color: white;
	border: none;
	padding: 10px 20px;
	margin-right: 10px;
	cursor: pointer;
}

/* “取消”按钮的样式 */
.button-cancel {
	background-color: red;
	color: white;
	border: none;
	padding: 10px 20px;
	cursor: pointer;
}

footer {
	position: fixed;
	left: 0;
	bottom: 0;
	width: 100%;
	z-index: 100;
	/* 确保它在页面上的其他内容之上 */
}

.footer-container {
	position: relative;
}

.footer-svg {
	margin-top: -150px;
	/* 向上移动 SVG */
	width: 100%;
	height: auto;
}



.footer-container {
	position: relative;
	z-index: 102;
	/* 确保文本内容在 SVG 下方 */
	/* 适当的背景颜色或样式，以确保文本可读 */
	/* background: rgba(255, 255, 255, 0.8); 可选：提供半透明背景 */
}

.login-background {
	background-image: url('..\assets\img\pic.png');
	background-size: contain;
	background-repeat: no-repeat;
	background-position: center;
	/* height: 70vh;  */
	/* width: 100vw;  */
	max-width: 150%;
	/* 最大宽度为父元素的100% */
	max-height: 50vh;
	/* 最大高度为视口高度的90% */
	height: auto;
	/* 高度自动调整以保持纵横比 */
}

.submit_btn_longer {
	width: 100%;
}

.container2 {
	display: flex;
	align-items: center;
	/* 垂直居中 */
	justify-content: center;
	/* 水平居中 */
	height: 30px;
	/* 设置容器高度 */
}

.centered-text {
	line-height: 30px; /* 设置行高为与父元素高度相等 */
	height: 30px; /* 设置高度为与父元素相等 */
  }
</style>