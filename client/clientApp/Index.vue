<template lang="pug">
header.indexBox.indexHeader
	h1.kcHeading1.indexTitle
		span Kartoffel&#8203;Cheetah's
		span.kcHeading2 Lair
	fractal-tree(:size-w="36", :size-h="60", style="position: absolute;top:0;right:22px;")
main.indexBox.indexMain
	router-view
	- for (var x = 0; x < 4; x++)
		div(class='indexCorner indexCorner' + x)
footer.indexBox.indexFooter
	ul.indexContact
		li(v-for=`
			i in [
				{ href: 'https://github.com/KartoffelCheetah', alt: 'My GitHub profile', img: githubLogo },
				{ href: 'https://gitlab.com/KartoffelCheetah', alt: 'My GitLab profile', img: gitlabLogo },
			]
			`
			:key="i.href"
		)
			a.kcLink.indexLink(target="_blank", :href="i.href")
				span.indexContactLogo(v-html="i.img")
				| {{ i.alt }}
		li.indexLink GPG?
</template>
<script lang="ts">
	import { defineComponent } from 'vue';
	import FractalTree from './components/FractalTree.vue';
	import gitlabLogo from '!kc_inline_svg_loader!./images/gitlab_logo.svg';
	import githubLogo from '!kc_inline_svg_loader!./images/github_logo.svg';

	export default defineComponent({
		name: 'Index',
		components: {
			FractalTree,
		},
		data () {
			return {
				gitlabLogo,
				githubLogo,
			};
		},
	});
</script>
<style>
	#index
		display flex
		min-height 100vh
		gap 12px
		flex-direction column
		align-items center
		background var(--darkmahagony)
		@media(max-width: 600px)
			gap 0
	.index
		&Title
			font-family var(--font-decorated)
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
			padding-top 20px
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
			position sticky
			top 100vh
			overflow hidden
			border-bottom-left-radius 5px
			border-bottom-right-radius 5px
		&Main
			position relative
			padding 45px
			background #400000
			box-shadow inset 0 0 8px var(--wheat)
			@media(max-width: 600px)
				padding 36px 8px 5px
				box-shadow inset 0 0 1px var(--wheat)
			@media(max-width: 400px)
				padding 5px 3px
		&Link
			display inline-flex !important
			align-items center
			gap 6px
		&ContactLogo > svg
			width 40px
			height 40px
			fill currentColor
		&Corner
			--cornerSize 63px
			--cornerOffset -5px
			position absolute
			width var(--cornerSize)
			height var(--cornerSize)
			background url('./images/corner_small.png')
			background-size var(--cornerSize)

			@media(max-width: 600px)
				display none

			&0
				top var(--cornerOffset)
				left var(--cornerOffset)
			&1
				top var(--cornerOffset)
				right var(--cornerOffset)
				transform rotate(90deg)
			&2
				bottom var(--cornerOffset)
				right var(--cornerOffset)
				transform rotate(180deg)
			&3
				bottom var(--cornerOffset)
				left var(--cornerOffset)
				transform rotate(270deg)
</style>
