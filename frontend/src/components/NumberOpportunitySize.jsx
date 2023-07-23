import { Box, Typography, useTheme, CircularProgress } from "@mui/material";
import { tokens } from "../theme";
import config from '../config';
import useFetchData from '../hooks/useFetchData';

const NumberOpportunitySize = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const { data, loading, error } = useFetchData(`${config.BASE_URL}/total_opportunity`);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <Box>
    <Typography
      variant="h5"
      fontWeight="600"
      color={colors.grey[100]}
    >
      Total Opportunity Detected
    </Typography>
    <Typography
      variant="h3"
      fontWeight="bold"
      color={colors.greenAccent[500]}
    >
      ${Number(data).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
    </Typography>
  </Box>
  );
};

export default NumberOpportunitySize;
