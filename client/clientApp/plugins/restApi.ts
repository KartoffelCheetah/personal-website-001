import { App } from 'vue';
import { ComponentCustomProperties } from 'vue';

type ApiType = (opId: string) => Promise<string>;

export default {
  async install (app: App, serverHost: string) {

    app.config.globalProperties.$serverHost = serverHost;

    const routingInit: Promise<SwaggerRouting> = fetch(`${serverHost}/api/swagger.json`).then(r => r.json());

    app.config.globalProperties.$api = apiUrl;

    const images = new Proxy({}, {
      async get (target: {[key: string]: Promise<ImageObject>}, prop: string) {
        if (!target[prop]) {
          target[prop] = fetch(`${await apiUrl('get_image_resource_resource')}${prop}`, {
            method: 'GET',
          })
            .then(r => r.json())
          ;
        }
        return target[prop];
      },
    });

    app.config.globalProperties.$images = images;

    async function apiUrl (opId: string): Promise<string> {
      const routing: SwaggerRouting = await routingInit;
      for (const [url, methods] of Object.entries(routing.paths)) {
        for (const [method, { operationId }] of Object.entries(methods)) {
          if (operationId === opId) {
            return `${serverHost}${routing.basePath}${url}`;
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
    $images: {[key: string]: Promise<ImageObject>};
  }
}
