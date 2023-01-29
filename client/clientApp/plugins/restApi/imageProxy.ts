import { EntrypointApiType } from './entrypointApi.ts';

export function createImageProxy (entrypointApi: EntrypointApiType) {
	return new Proxy({}, {
		async get (target: {[key: string]: Promise<ImageObject>}, prop: string) {
			if (!target[prop]) {
				target[prop] = fetch(
					`${await entrypointApi('get_image_resource_resource')}ROOT/${prop}`,
					{
						method: 'GET',
					}
				)
					.then(r => r.json())
				;
			}
			return target[prop];
		},
	});
}

export interface ImageObject {
	"@context": string;
	"@type": string;
	"@id": string;
	name: string;
	contentUrl: string;
	thumbnail: ImageObject[];
	height: number;
	width: number;
}
