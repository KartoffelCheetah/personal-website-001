// @ts-ignore
import ROUTING from '../../../static/routing.json';

export default {
  ROUTING: ROUTING,
  apiRoute(routes: string[]) {
    let paths: any = routes.reduce(
      (
        acc: any,
        cur: string
      ):any => {
        if (typeof ROUTING[cur] === 'object') {
          return [ acc[0]+acc[1][cur].namespace, acc[1][cur] ];
        } else {
          return [ acc[0]+acc[1][cur], acc[1][cur] ];
        }
      }, ['', ROUTING]
    );
    let path = [ROUTING.API_PREFIX, paths[0]].join('/').replace(/\/+/g, '/');
    return path;
  },
}
