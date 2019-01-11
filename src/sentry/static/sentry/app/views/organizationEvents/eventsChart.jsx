import {withRouter} from 'react-router';
import PropTypes from 'prop-types';
import React from 'react';
import moment from 'moment';

import {getFormattedDate} from 'app/utils/dates';
import {t} from 'app/locale';
import LineChart from 'app/components/charts/lineChart';
import SentryTypes from 'app/sentryTypes';
import withApi from 'app/utils/withApi';
import withChartZoom from 'app/components/charts/withChartZoom';

import EventsContext from './utils/eventsContext';
import EventsRequest from './utils/eventsRequest';

const DEFAULT_GET_CATEGORY = () => t('Events');

const getDate = date =>
  date ? moment.utc(date).format(moment.HTML5_FMT.DATETIME_LOCAL_SECONDS) : null;

const LineChartWithZoom = withChartZoom(LineChart);

class EventsChart extends React.Component {
  static propTypes = {
    organization: SentryTypes.Organization,
    router: PropTypes.object,
    period: PropTypes.string,
    query: PropTypes.string,
    start: PropTypes.instanceOf(Date),
    end: PropTypes.instanceOf(Date),
    utc: PropTypes.bool,
    zoom: PropTypes.bool,

    // Callback for when chart has been zoomed
    onZoom: PropTypes.func,
  };

  useHourlyInterval = (props = this.props) => {
    const {period, start, end} = props;

    if (typeof period === 'string') {
      return period.endsWith('h') || period === '1d';
    }

    return moment(end).diff(start, 'hours') <= 24;
  };

  render() {
    const {period, utc, query} = this.props;

    const useHourly = this.useHourlyInterval();

    let interval = '30m';
    let xAxisOptions = {
      axisLabel: {
        formatter: (value, index, ...rest) => {
          const firstItem = index === 0;
          const format = useHourly && !firstItem ? 'LT' : 'lll';
          return getFormattedDate(value, format, {local: !utc});
        },
      },
    };

    // TODO(billy): For now only include previous period when we use relative time

    return (
      <div>
        <EventsRequest
          {...this.props}
          interval={interval}
          showLoading
          query={query}
          getCategory={DEFAULT_GET_CATEGORY}
          includePrevious={!!period}
        >
          {({timeseriesData, previousTimeseriesData}) => {
            return (
              <LineChartWithZoom
                isGroupedByDate
                series={timeseriesData}
                seriesOptions={{
                  showSymbol: false,
                }}
                previousPeriod={previousTimeseriesData}
                grid={{
                  left: '30px',
                  right: '18px',
                }}
                tooltip={{
                  formatAxisLabel: (value, isTimestamp, isUtc) => {
                    if (!isTimestamp) {
                      return value;
                    }
                    return getFormattedDate(value, 'lll', {local: !isUtc});
                  },
                }}
              />
            );
          }}
        </EventsRequest>
      </div>
    );
  }
}

const EventsChartContainer = withRouter(
  withApi(
    class EventsChartWithParams extends React.Component {
      render() {
        return (
          <EventsContext.Consumer>
            {context => (
              <EventsChart
                {...context}
                project={context.project || []}
                environment={context.environment || []}
                {...this.props}
              />
            )}
          </EventsContext.Consumer>
        );
      }
    }
  )
);

export default EventsChartContainer;
export {EventsChart};
