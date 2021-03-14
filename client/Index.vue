<template lang="pug">
header
  h1.heading1.indexTitle
    span Kartoffel&#8203;Cheetah's
    span.heading2 website
main.indexMain
  router-view
  p qwertzuiopőúasdfghjkléáűíyxcvbnmöüó
  p QWERTZUIOPŐÚASDFGHJKLÉÁŰÍYXCVBNMÖÜÓ
  br
  p I'm a front-end developer.
    | adgnafg dhguifgfigiof experience as a programmer.
    | I enjoy programming in JavaScript and Python3, designing websites and doing 2D art.
    | Whenever possible I use open-source software on Linux. 🐧
footer
  p i want some icons to the links
  ul.indexContact
    li
      a.link(href="https://github.com/KartoffelCheetah") GitHub
    li
      a.link(href="https://gitlab.com/KartoffelCheetah") GitLab
</template>
<script lang="ts">
  import { defineComponent } from 'vue';

  export default defineComponent({
    name: 'Index',
  });
</script>
<style scoped>
  .index
    &Title
      display flex
      flex-direction column
      padding-left 8px
      border-bottom 1em solid var(--brown)
      border-left .3em solid var(--wheat)
      margin-bottom 5px
      color black
      text-shadow 1px 1px 2px var(--wheat)
    &Contact
      display flex
      padding-top 2em
      gap .8em
    &Main
      padding 0 3px
</style>
