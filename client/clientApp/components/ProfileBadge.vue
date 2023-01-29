<template lang="pug">
img(class="profileBadge", v-bind="profileBadge", :alt="altTag")
</template>

<script lang="ts">
	import { defineComponent } from 'vue';
	import type { PropType } from 'vue';
	import profileBadgeKartoffelCheetah from '../images/ProfileBadge_KartoffelCheetah.png';

	class ProfileBadge {
		src: String;
		alt: String;
		style: String;
		constructor (src: string, alt: string, style: string) {
			this.src = src;
			this.alt = alt;
			this.style = style;
		}
	}

	export const KCProfileBadge = new ProfileBadge(
		profileBadgeKartoffelCheetah,
		'KartoffelCheetah',
		'padding-right: 3px;',
	);

	export default defineComponent({
		name: 'ProfileBadge',
		props: {
			profileBadge: {
				type: ProfileBadge as PropType<ProfileBadge>,
				required: true,
			},
			altOverride: {
				type: String,
				default: undefined,
			},
		},
		computed: {
			altTag (): String {
				return typeof this.altOverride === 'string' ? this.altOverride : this.profileBadge.alt;
			},
		},
	});
</script>

<style>
	.profileBadge
		height 1em
		background var(--wheat)
		border-radius 3px
</style>
