<template lang="pug">
header.indexBox
  h1.heading1.indexTitle
    span Kartoffel&#8203;Cheetah's
    span.heading2 website
main.indexBox.indexMain
  router-view
  p qwertzuiopőúasdfghjkléáűíyxcvbnmöüó
  p QWERTZUIOPŐÚASDFGHJKLÉÁŰÍYXCVBNMÖÜÓ
  br
  image-resource(name="Circe_by_John_Collier.jpg", alt="circe")
  image-resource(name="Flamber-Bougault.jpg", alt="old ship")
  image-resource(name="Alma_Tadema_Spring.jpg", alt="high res classsical painting")
  p I'm a front-end developer.
    | adgnafg dhguifgfigiof experience as a programmer.
    | I enjoy programming in JavaScript and Python3, designing websites and doing 2D art.
    | Whenever possible I use open-source software on Linux. 🐧
footer.indexBox.indexFooter
  ul.indexContact
    li
      a.link(href="https://github.com/KartoffelCheetah") GitHub
    li
      a.link(href="https://gitlab.com/KartoffelCheetah") GitLab
    li TODO tanuki and octocat for the links
    li GPG?
</template>
<script lang="ts">
  import { defineComponent } from 'vue';
  import ImageResource from './components/ImageResource.vue';

  export default defineComponent({
    name: 'Index',
    components: { ImageResource },
  });
</script>
<style>
  #index
    display flex
    min-height 100vh
    flex-direction column
    align-items center
    background var(--darkgray)
  .index
    &Title
      display flex
      flex-direction column
      padding-left 8px
      border-bottom 10px solid var(--brown)
      border-left 5px solid var(--wheat)
      background var(--deepdarkbrown) url('./images/instrument.svg')!important;
      background-blend-mode saturation
      color black
      text-shadow 1px 1px 2px var(--wheat)
    &Contact
      display flex
      padding-top 2em
      gap .8em
    &Box
      width 600px
      max-width 100%
      background: var(--gray)
    &Footer
      overflow hidden
      border-bottom-left-radius 5px
      border-bottom-right-radius 5px
    &Main
      padding 5px 8px
      flex-grow .5
      @media(max-width: 400px)
        padding 5px 3px
</style>
