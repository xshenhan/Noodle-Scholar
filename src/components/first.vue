<template>
  <div>
    <p>{{ title }}</p>
    <p v-html="Vue3Website"></p>
    <div v-bind="css_type">动态绑定属性名</div>
    <div v-show="isShow">条件判断的渲染</div>
    <div v-if="flag == 'A'">flag 为 A</div>
    <div v-else>flag 不为 A</div>
  </div>
  <button :disabled="isDisabled">A button</button>
</template>

<script>
export default {
  data() {
    return {
      title: "Noodle Scholar",
      Vue3Website: "<a href='https://cn.vuejs.org/guide/quick-start.html'>Vue 3 Docs</a>",
      css_type: {
        class: "Myclass",
        id: "Myid",
      },
      isDisabled: true,
      isShow: true,
      flag: "A"
    }
  }
}
</script>

<style>
.Myclass {
  color: blue;
  font-size: 30px;
}
</style>