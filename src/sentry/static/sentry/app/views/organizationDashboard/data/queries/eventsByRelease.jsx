/**
 * Events by Release
 */
const eventsByRelease = {
  fields: ['sentry:release'],
  conditions: [],
  aggregations: [['count()', null, 'Events']],
  limit: 10000,

  orderby: '-time',
  groupby: ['time'],
  rollup: 86400,
};

export default eventsByRelease;
