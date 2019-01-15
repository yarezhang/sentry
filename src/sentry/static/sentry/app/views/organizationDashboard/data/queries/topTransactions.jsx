/**
 * Top Events by URL
 */
const eventsQuery = {
  fields: ['url'],
  conditions: [],
  aggregations: [['count()', null, 'count']],
  limit: 10000,

  orderby: '-time',
  groupby: ['time'],
  rollup: 86400,
};

export default eventsQuery;
