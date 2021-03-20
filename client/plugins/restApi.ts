import { App } from 'vue';
import { ComponentCustomProperties } from 'vue';

type ApiType = (opId: string, fetchParams: Object) => Promise<Response>;

export default {
  async install (app: App, serverHost: string) {

    app.config.globalProperties.$serverHost = serverHost;

    const routingInit: Promise<SwaggerRouting> = fetch(`${serverHost}/api/swagger.json`).then(r => r.json());

    app.config.globalProperties.$api = api;

    const images: Promise<ImageObject[]> = api('get_image_resource_resource', {}).then(r => r.json());

    app.config.globalProperties.$images = images;

    async function api (opId: string, fetchParams: Object): Promise<Response> {
      const routing: SwaggerRouting = await routingInit;
      for (const [url, methods] of Object.entries(routing.paths)) {
        for (const [method, { operationId }] of Object.entries(methods)) {
          if (operationId === opId) {
            return fetch(`${serverHost}${routing.basePath}${url}`, {
              method,
              ...fetchParams,
            });
          }
        }
      }
      throw TypeError(`opId: "${opId}" not found`);
    }
  },
};

interface SwaggerRouting {
  basePath: string;
  paths: { [key: string]: SwaggerRoutingPaths };
}

interface SwaggerRoutingPaths {
  operationId: string;
}

interface ImageObject {
  "@context": string;
  "@type": string;
  "@id": string;
  name: string;
  contentUrl: string;
  thumbnailUrl: string[];
  height: number;
  width: number;
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $api: ApiType;
    $serverHost: string;
    $images: Promise<ImageObject[]>;
  }
}
