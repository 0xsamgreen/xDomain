import React from 'react';
import { CircularProgress, useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../theme";
import config from '../config';
import useFetchData from '../hooks/useFetchData';

const BarChartDailySize = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const { data, loading, error } = useFetchData(`${config.BASE_URL}/data_daily_opp?epoch_start=1668658046`);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  function getEveryNth(data, n) {
    return data.filter((_, i) => i % n === 0).map(d => d.date);
  }

  const tickValues = getEveryNth(data, 3);

  const minY = 0;
  const maxY = Math.floor(Math.max(...data.map(d => d.amount)));
  const maxTickY = Math.ceil(maxY * 0.95);

  const numTicks = 7;
  const tickValuesY = Array.from({ length: numTicks }, (_, i) => minY + ((maxTickY - minY) / (numTicks - 1)) * i);
  const tickValuesYRounded = tickValuesY.map(value => Math.round(value));
  const formattedTickValuesY = tickValuesYRounded.map(value => value.toLocaleString('en-US'));


  console.log('tickValuesY', tickValuesY)
  console.log('formattedTickValuesY', formattedTickValuesY)




  return (
    <ResponsiveBar
      data={data}
      theme={{
        // added
        axis: {
          domain: {
            line: {
              stroke: colors.grey[100],
            },
          },
          legend: {
            text: {
              fill: colors.grey[100],
            },
          },
          ticks: {
            line: {
              stroke: colors.grey[100],
              strokeWidth: 1,
            },
            text: {
              fill: colors.grey[100],
            },
          },
        },
        legends: {
          text: {
            fill: colors.grey[100],
          },
        },
      }}
      keys={["amount"]}
      indexBy="date"
      margin={{ top: 50, right: 60, bottom: 50, left: 70 }}
      padding={0.3}
      valueScale={{ type: "linear" }}
      indexScale={{ type: "band", round: true }}
      colors={{ scheme: "nivo" }}
      defs={[
        {
          id: "dots",
          type: "patternDots",
          background: "inherit",
          color: "#38bcb2",
          size: 4,
          padding: 1,
          stagger: true,
        },
        {
          id: "lines",
          type: "patternLines",
          background: "inherit",
          color: "#eed312",
          rotation: -45,
          lineWidth: 6,
          spacing: 10,
        },
      ]}
      borderColor={{
        from: "color",
        modifiers: [["darker", "1.6"]],
      }}
      axisTop={null}
      axisRight={null}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legendPosition: "middle",
        legendOffset: 32,
        tickValues: tickValues,
      }}
      gridYValues={tickValuesY}
      axisLeft={{
        tickSize: 5,
        tickPadding: 2,
        tickRotation: 0,
        legend: "Total Opportunity $",
        legendPosition: "middle",
        legendOffset: -55,
        tickValues: tickValuesY,
        format: d => Math.round(d),
      }}
      enableLabel={false}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{
        from: "color",
        modifiers: [["darker", 1.6]],
      }}
      role="application"
    />
  );
};

export default BarChartDailySize;
