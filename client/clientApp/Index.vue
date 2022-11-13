<template lang="pug">
header.indexBox.indexHeader
  h1.heading1.indexTitle
    span Kartoffel&#8203;Cheetah's
    span.heading2 Lair
  fractal-tree(:size-w="36", :size-h="60", style="position: absolute;top:0;right:22px;")
main.indexBox.indexMain
  router-view
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
  import FractalTree from './components/FractalTree.vue';

  export default defineComponent({
    name: 'Index',
    components: {
      FractalTree,
    },
  });
</script>
<style>
  #index
    display flex
    min-height 100vh
    flex-direction column
    align-items center
    background var(--darkmahagony)
  .index
    &Title
      display flex
      flex-direction column
      padding-left 8px
      border-bottom 10px double var(--brown)
      border-right 6px double var(--wheat)
      border-left 5px double var(--wheat)
      background var(--deepdarkbrown) url('./images/instrument.svg');
      background-blend-mode saturation
      color var(--darksalmon)
      text-shadow 1px 1px black
    &Contact
      display flex
      padding-top 32px
      padding-bottom 8px
      gap .8em
    &Box
      width 600px
      max-width 100%
    &Header
      position relative
      &::before
        content ''
        position absolute
        top 0
        right 20px
        bottom 0
        width 40px
        opacity .2
        background var(--wheat)
    &Footer
      overflow hidden
      border-bottom-left-radius 5px
      border-bottom-right-radius 5px
    &Main
      padding 48px 8px 5px
      flex-grow .5
      @media(max-width: 400px)
        padding 5px 3px
</style>
