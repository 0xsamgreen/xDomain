import { Box, useTheme } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";

const FAQ = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box m="20px">
      <Header title="FAQ" subtitle="Frequently Asked Questions Page" />

      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            What is this?
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            This is a visualization tool for historical cross-domain arbitrage. The data is provided by www.odos.xyz. We currently have some older data being displayed here. We will add recent data soon.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            Who built this?
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
            This was built by <a href="https://twitter.com/PoupouWeb3">Guillaume Poullain</a> and <a href="https://twitter.com/0xsamgreen">Sam Green</a> as part of the ETHGlobal Paris 2023 hackathon.
          </Typography>
        </AccordionDetails>
      </Accordion>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography color={colors.greenAccent[500]} variant="h5">
            Where can I find the code and source files?
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Typography>
          <a href="https://github.com/0xsamgreen/xDomain">https://github.com/0xsamgreen/xDomain</a>
          </Typography>
        </AccordionDetails>
      </Accordion>
    </Box>
  );
};

export default FAQ;
