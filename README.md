# ICE2604 项目概述

## 运行

* clone 整个文件夹
* 在根目录运行 `npm install`，如有报错，再次运行 `npm install --no-fund`
* 在根目录运行 `npm run dev`
* 打开浏览器窗口预览结果

## 问题与解决
1. 挂载函数的异步问题

在 `mounted()` 挂载中，本意是先运行 `searchInfo()` 再运行 `searchId()`，但在前者中未来及向 `_id` 赋值就运行了后者。这可能是因为异步操作导致的问题。异步操作是非阻塞的，意味着它们会在后台执行，并且不会等待其完成而继续执行后续代码。

为了解决这个问题，可以使用回调函数、Promise 或 async/await 等方式来确保在 `searchInfo` 完成后再调用 `searchId`
以下是使用 Promise 的示例代码
```js
function searchInfo(callback) {
  // 在异步操作完成后调用回调函数
  setTimeout(function() {
    const _id = "12345"; // 这里是赋值 _id 的逻辑
    callback(_id);
  }, 1000); // 模拟异步操作的延迟
}

function searchId() {
  searchInfo(function(_id) {
    console.log("searchId: " + _id);
  });
}

searchId();
```
在上述代码中，searchInfo 函数中使用了 setTimeout 来模拟异步操作，并在操作完成后调用了回调函数，并将 _id 作为参数传递给回调函数。然后，searchId 函数通过传递一个回调函数给 searchInfo 函数来获取 _id，并在回调函数中打印 _id。