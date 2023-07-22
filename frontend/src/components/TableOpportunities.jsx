import React from 'react';
import { Box, Typography, CircularProgress, useTheme} from "@mui/material";
import { tokens } from "../theme";
import config from '../config';
import useFetchData from '../hooks/useFetchData';


const TableOpportunities = ({ isDashboard = false }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const { data, loading, error } = useFetchData(`${config.BASE_URL}/current_opp`);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <Box>
      {data.map((opportunity, i) => (
        <Box
          key={`${opportunity.token}-${i}`}
          display="flex"
          justifyContent="space-between"
          alignItems="center"
          borderBottom={`4px solid ${colors.primary[500]}`}
          p="15px"
        >
          <Box>
            <Typography
              color={colors.greenAccent[500]}
              variant="h5"
              fontWeight="600"
            >
              {opportunity.token}
            </Typography>
          </Box>
          <Box
            backgroundColor={colors.greenAccent[500]}
            ml="center"
            p="5px 10px"
            borderRadius="4px"
          >
            ${(Number(opportunity.amount).toFixed(2))}
          </Box>
        </Box>
      ))}
    </Box>
  );
};

export default TableOpportunities;
