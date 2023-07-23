import { CircularProgress, useTheme } from "@mui/material";
import { ResponsiveBar } from "@nivo/bar";
import { tokens } from "../theme";
import useFetchData from '../hooks/useFetchData';
import config from '../config';

const BarChartTokenSize = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const { data, loading, error } = useFetchData(`${config.BASE_URL}/token_totals_paths`);
  const { data: keys, loading: loadingKeys, error: errorKeys } = useFetchData(`${config.BASE_URL}/token_paths`);

  if (loading || loadingKeys) {
    return <CircularProgress />;
  }

  if (error || errorKeys) {
    return <div>Error: {error}</div>;
  }

  const minY = 0;
  let maxY = -Infinity;
  data.forEach(obj => {
    Object.values(obj).forEach(val => {
      // check if the value is a number
      if (typeof val === 'number' && val > maxY) {
        maxY = val;
      }
    });
  });

  const maxTickY = Math.ceil(maxY * 0.95);

  const numTicks = 7;
  const tickValuesY = Array.from({ length: numTicks }, (_, i) => minY + ((maxTickY - minY) / (numTicks - 1)) * i);
  const tickValuesYRounded = tickValuesY.map(value => Math.round(value));


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
      }}
      keys={keys}
      indexBy="token"
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
        legend: isDashboard ? undefined : "token", // changed
        legendPosition: "middle",
        legendOffset: 32,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 2,
        tickRotation: 0,
        legend: "Total Opportunity $",
        legendPosition: "middle",
        legendOffset: -40,
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

export default BarChartTokenSize;
