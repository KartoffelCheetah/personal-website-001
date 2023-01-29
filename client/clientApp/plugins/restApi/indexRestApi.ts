import { App } from 'vue';
import { ComponentCustomProperties } from 'vue';
import { createImageProxy, ImageObject } from './imageProxy.ts';
import { createEntrypointApi, EntrypointApiType } from './entrypointApi.ts';

export default {
	async install (app: App, serverHost: string) {
		const entrypointApi = createEntrypointApi(serverHost);
		const imagesProxy = createImageProxy(entrypointApi);

		app.config.globalProperties.$serverHost = serverHost;

		// app.config.globalProperties.$api = entrypointApi;

		app.config.globalProperties.$images = imagesProxy;

	},
};

declare module '@vue/runtime-core' {
	interface ComponentCustomProperties {
		// $api: EntrypointApiType;
		$serverHost: string;
		$images: {[key: string]: Promise<ImageObject>};
	}
}
