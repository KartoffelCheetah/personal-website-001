export type EntrypointApiType = (opId: string) => Promise<string>;

export function createEntrypointApi (serverHost: string): EntrypointApiType {
  const routingInit: Promise<SwaggerRouting> = fetch(`${serverHost}/api/swagger.json`).then(r => r.json());

  return async function (opId: string): Promise<string> {
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
}

interface SwaggerRouting {
  basePath: string;
  paths: { [key: string]: SwaggerRoutingPaths };
}

interface SwaggerRoutingPaths {
  operationId: string;
}
