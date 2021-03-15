import { App } from 'vue';
import { ComponentCustomProperties } from 'vue';

type ApiType = (opId: string, fetchParams: Object) => Promise<Response>;

export default {
  async install (app: App, baseUrl: string) {
    const routingInit: Promise<SwaggerRouting> = fetch(`${baseUrl}/api/swagger.json`).then(r => r.json());

    app.config.globalProperties.$api = async (opId: string, fetchParams: Object): Promise<Response> => {
      const routing: SwaggerRouting = await routingInit;
      for (const [url, methods] of Object.entries(routing.paths)) {
        for (const [method, { operationId }] of Object.entries(methods)) {
          if (operationId === opId) {
            return fetch(`${baseUrl}${routing.basePath}${url}`, {
              method,
              ...fetchParams,
            });
          }
        }
      }
      throw TypeError(`opId: "${opId}" not found`);
    };
  },
};

interface SwaggerRouting {
  basePath: string;
  paths: { [key: string]: SwaggerRoutingPaths };
}

interface SwaggerRoutingPaths {
  operationId: string;
}

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $api: ApiType;
  }
}
