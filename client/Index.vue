<template lang="pug">
header
  h1.heading1 header
  h2.heading2 header
  h3.heading3 header
  h4.heading4 header
  h5.heading5 header
  h6.heading6 header
main
  router-view
    p qwertzuiopőúasdfghjkléáűíyxcvbnmöüó
    p QWERTZUIOPŐÚASDFGHJKLÉÁŰÍYXCVBNMÖÜÓ
    br
    p I'm a front-end developer.
      | adgnafg dhguifgfigiof experience as a programmer.
      | I enjoy programming in JavaScript and Python3, designing websites and doing 2D art.
      | Whenever possible I use open-source software on Linux. 🐧
footer footer
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  export default defineComponent({
    name: 'Index',
  });
</script>
