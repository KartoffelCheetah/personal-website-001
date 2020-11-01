// @ts-ignore
import ROUTING_JSON from '../../../static/routing.json';

export const ROUTING = ROUTING_JSON;

export function getRoute(routes: string[], isApi: boolean=true) {
  const paths: any = routes.reduce(
    (
      acc: any,
      cur: string
    ):any => {
      const prevStr = acc[0];
      const curVal = acc[1][cur];
      switch(typeof curVal) {
        case 'object':
          if (curVal.namespace) {
            return [ prevStr+curVal.namespace, curVal ];
          }
          return [ prevStr, curVal ];
        case 'string':
          return [ prevStr+curVal, curVal ];
        default:
          throw Error('routing error: ' + cur);
      }
    }, ['', ROUTING]
  );
  const path = [isApi ? ROUTING.API_PREFIX : '', paths[0]].join('/').replace(/\/+/g, '/');
  return path;
}
