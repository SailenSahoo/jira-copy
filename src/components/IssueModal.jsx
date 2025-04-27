import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  Typography,
  Box,
  Divider,
  Stack,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import AssignmentIcon from "@mui/icons-material/Assignment";
import PersonIcon from "@mui/icons-material/Person";
import BugReportIcon from "@mui/icons-material/BugReport";
import FlagIcon from "@mui/icons-material/Flag";
import EventIcon from "@mui/icons-material/Event";
import DescriptionIcon from "@mui/icons-material/Description";

const IssueModal = ({ issue, onClose }) => {
  if (!issue) return null;

  return (
    <Dialog open={Boolean(issue)} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ m: 0, p: 2, bgcolor: "#f4f6f8" }}>
        <Typography variant="h6" sx={{ display: "flex", alignItems: "center" }}>
          <AssignmentIcon sx={{ mr: 1 }} />
          {issue.key}: {issue.summary}
        </Typography>
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: "absolute",
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500]
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent dividers sx={{ bgcolor: "#ffffff" }}>
        <Stack spacing={2}>
          <Box display="flex" alignItems="center">
            <BugReportIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle2">Type:</Typography>&nbsp;
            <Typography>{issue.type}</Typography>
          </Box>

          <Box display="flex" alignItems="center">
            <PersonIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle2">Assignee:</Typography>&nbsp;
            <Typography>{issue.assignee || "Unassigned"}</Typography>
          </Box>

          <Box display="flex" alignItems="center">
            <PersonIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle2">Reporter:</Typography>&nbsp;
            <Typography>{issue.reporter}</Typography>
          </Box>

          <Box display="flex" alignItems="center">
            <FlagIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle2">Priority:</Typography>&nbsp;
            <Typography>{issue.priority}</Typography>
          </Box>

          <Box display="flex" alignItems="center">
            <EventIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle2">Created:</Typography>&nbsp;
            <Typography>{issue.created}</Typography>
          </Box>

          <Box>
            <Typography variant="subtitle2" sx={{ mb: 1 }}>
              Status:
            </Typography>
            <Chip
              label={issue.status}
              color={
                issue.status === "Done"
                  ? "success"
                  : issue.status === "In Progress"
                  ? "warning"
                  : "default"
              }
              variant="outlined"
            />
          </Box>

          <Divider />

          <Box display="flex" alignItems="flex-start">
            <DescriptionIcon sx={{ mr: 1, mt: 0.5 }} />
            <Box>
              <Typography variant="subtitle2">Description</Typography>
              <Typography variant="body2">{issue.description}</Typography>
            </Box>
          </Box>

          {issue.customFields && issue.customFields.length > 0 && (
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="subtitle2">Custom Fields</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={1}>
                  {issue.customFields.map((cf, index) => (
                    <Typography key={index}>
                      <strong>{cf.name}:</strong> {cf.value}
                    </Typography>
                  ))}
                </Stack>
              </AccordionDetails>
            </Accordion>
          )}

          {issue.comments && issue.comments.length > 0 && (
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="subtitle2">Comments</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={1}>
                  {issue.comments.map((comment, index) => (
                    <Typography key={index} variant="body2">
                      • {comment}
                    </Typography>
                  ))}
                </Stack>
              </AccordionDetails>
            </Accordion>
          )}
        </Stack>
      </DialogContent>
    </Dialog>
  );
};

export default IssueModal;
