# ICE2604 项目概述

## 运行

* clone 整个文件夹
* 在根目录运行 `npm install --no-fund`
* 在根目录运行 `npm run dev`
* 打开浏览器窗口预览结果

## Performance Optimization

1. 挂载函数的异步问题

在 `mounted()` 挂载函数中，Javascript 会将所有的包含 `Axios` 请求的函数全部同步执行，浏览器中 JavaScript 是单线程的，这意味并没有提供线程锁。

这意味着在 HTTP 请求没有处理完就进行了下面的元素绑定或者其他查询。为了解决这个问题，可以使用 Promise 和 async/await 等方式来确保所有的请求都上锁执行：

一方面将 `mounted()` 声明为异步函数，同时将所有需要优先完成的函数（即需要上锁的函数）前也加上`await`声明
```js
async mounted {
  await this.getAuthorPapers(0, 50);
  this.chart = echarts.init(document.getElementById('chart'));
  this.setChart();
}
```
另一方面在声明的异步函数中返回 `Promise` 类型，即直接返回 `Axios` 的请求结果。这样保证了对上面元素 `id` 的绑定严格在请求数据处理完成后
```js
async getAuthorPapers(_start, _end) {
            return axios.get('http://10.80.135.205:8080/api/v1/vis/author/papers', {
                params: {}
            })
                .then((response) => {})
                .catch((error) => {})
      },
```

2. 优化回流和重绘次数
下面是浏览器对 DOM树 和 CSSOM树 的渲染流程
![![DOM树和CSSOM树渲染流程](https://juejin.cn/post/7281581471897387071)](https://s11.ax1x.com/2023/12/29/piLB6ne.png)

网页会在一些情况下触发回流，比如以下三方面
* 页面的首次渲染（例如：刷新）
  这一部分回流，即第一次渲染页面，是无法避免的，我们只能通过 `v-cloak` 在插值表达式未计算完成时，阻止其显示未编译的原始数据内容，消除渲染时的闪烁问题
* 添加或删除可见的 DOM 元素
  考虑到我们较多的可视化数据和较多的论文数量，这是我们需要主要考虑回流的性能消耗的地方。比如首页的柱状图的翻页效果，为了防止翻页造成的多次 HTTP 请求，我们对可视化数据做了**离线处理**，这样每次翻页就只是对 DOM元素 **可见性的修改和拷贝替换**，因此不会触发页面回流。

* 激活 CSS 伪类，例如 `:hover` `:active` `:focus`

最终，我们将网页中的所有潜在的回流都转化成了重绘。

3. 页面布局策略

我们对搜索结果页面和论文页面做了屏幕尺寸适应性调整，所有的元素都被包裹在多层 `div` 构成的容器中，其中一部分容器使用 `fixed` 和 `relative` 进行位置固定，这使得外围的元素可以灵活适应页面布局；另一部分容器使用 `absolute` 位置固定，这使得内围元素脱离文档流，在样式修改时，只有该元素本身及其子元素会触发重绘，减小了重绘的范围。

## Basic Features

Generally speaking，我们的设计理念是接近搜索引擎的实际使用需求。因此我们重点设计了多次搜索，namely在任何位置的任意潜在搜索词都可以链接到新的页面展示搜索结果。

1. 支持 6 种方式搜索 `All` `Title` `Abstract` `DOI` `Keyword` `Author`
2. 支持搜索页面二次搜索
3. 作者、领域等信息都可以点击以继续搜索
4. Preview of image-parsing in sliding window
5. Click to copy DOI and website's URL
6. Download PDF with account
7. Accurate, completed, powerful table-parsing

## Special Features

1. 支持特殊字符的搜索：搜索内容进行了 URI 编码，并在后端解码
2. Support Latex render <img src="https://s11.ax1x.com/2023/12/26/pib9DBT.png" width=60%>
3. Sufficient database with more than 2,000,000 arxiv parpers, covers numerous fields, such as CS, PHY, STAT, MATH, etc.
4. Support summary of the paper by GPT model. It's as well limited to authorized users currently.

## Art

1. 我们统一了网站前端的设计风格，使用紫色 as theme color，并全部元素采用扁平化设计，风格简约、大气
2. 除了首页的可视化图表外，所有的页面支持移动端访问，即适配任意尺寸大小的屏幕
3. 我们拟写了全新的用户登录隐私协议，以表达我们对用户隐私的重视
4. 我们仿照 Apple Inc. 拟写了 6 条令人印象深刻的宣传标语


## Visualization

我们着重对2,000,000篇 Arxiv 文章的作者和领域做了可视化图表。我们对每年的文章数量做了排序；对前50名作者的论文数量做了排序；对收录的所有论文的领域和子领域的比例做了分析 by pie charts；对每个领域所包含的子领域文章比例做了分析 by pie charts.

These charts在展示数据的同时，均可以点击并跳转到新的search-result page，展示对该作者或该领域的搜索结果。


## 功能与展示

1. 一：展示搜索功能和基础信息展示
  * 选项搜索下拉框
  * arxiv 论文源
  * 搜索页面的二次搜索
  * 搜索页面的论文展示--作者可继续搜、DOI可复制、图片展示
  * 点进论文具体页面：
    * latex渲染
    * 图片和表格解析和原理
    * 作者可继续搜、几个按钮的功能、下载pdf
    * 登出账号，无法下载->重新注册、登录
    * GPT模型总结
2. 二：展示首页可视化
  * 每张图的内容
  * 每张图鼠标悬浮和点击效果
  * 具体说明两个柱状图的翻页和点击效果
  * （可视化的重绘问题）
3. 三：展示艺术效果
  * 我们的竞争对手，Google
  * 搜索界面和论文页面的适应屏幕布局



## 广告

```
1. 上半句和下半句都要有同样的字。比如说 Macbook 的「满载动力，满足你的一天。」和「一身轻，更举重若轻。」以及说照片的「照过的再多，照样轻松找到。 」
2. 用完全不对仗但字数相同还押韵的句式，比如说 Retina 屏的「每一像素颗粒，尽显澎湃动力。」和说 iMessage 的「想说的，亲手写。」
3. 幼童式的口语化，比如说 iPad 的「Retina 的大作，一款又一款。」和母亲节活动宣传的「让妈妈开心的礼物，开了又开。」
4. 各种反义词。比如说 iPad mini 的「小身型，大有身手。」和说耳机的「无线，无繁琐，只有妙不可言。」
```
1. 唯一的不同，是处处都不同。（大标题）
2. 一身轻，更举重若轻。（功能少）
3. 满载动力，满足你乱想的词。（服务器）
4. 搜不搜在你，准不准在我。
5. 你的下一个搜索引擎，何必是你的。（用户信息完全泄漏，搜索记录数据库可见。你的隐私，我说了算。）
6. 快，比慢更快。（搜索后时间较长）
7. 全新用户登录协议，只许协，不许议。（注册登录页面）
8. （压力测试）

## 代办

## 可视化

- [x] 两个饼图，分别展示 subject 和 subsubject 的比例分配（不能点击）（arxiv）
- [x] 再加一个大的柱状图，展示 subject，点击可以搜索相应领域（arxiv）
- [x] 并且鼠标悬停可以展示 其 subsubject 的柱状图（arxiv）
- [x] 第三个饼图，展示年份-年份论文数的比例分配（arxiv）
- [ ] 一个柱状图，展示100pdfs的年份-论文数量，并且可以切换按照年份排序还是按照论文数排序 （*）（100pdfs）