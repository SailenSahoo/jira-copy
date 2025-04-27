import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Avatar,
  Chip,
  Box
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import dayjs from "dayjs";

const IssueCard = ({ issue }) => {
  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case "done":
        return "success";
      case "in progress":
        return "primary";
      case "to do":
        return "default";
      default:
        return "default";
    }
  };

  return (
    <Card elevation={2} sx={{ borderRadius: 2, backgroundColor: "#f9f9f9", mb: 4, p: 2 }}>
      <CardContent>
        {/* Header */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
          <Typography variant="h6">{issue.key} - {issue.summary}</Typography>
          <Chip
            label={issue.status}
            color={getStatusColor(issue.status)}
            size="small"
            sx={{ fontWeight: "bold" }}
          />
        </Box>

        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          {issue.type} | Created: {dayjs(issue.created).format("DD MMM YYYY")}
        </Typography>

        <Divider sx={{ my: 2 }} />

        {/* Description */}
        <Typography variant="subtitle1" sx={{ fontWeight: "bold", mb: 1 }}>Description</Typography>
        <Typography variant="body2" sx={{ mb: 2 }}>{issue.description}</Typography>

        <Divider sx={{ my: 2 }} />

        {/* Details Section */}
        <Typography variant="subtitle1" sx={{ fontWeight: "bold", mb: 1 }}>Details</Typography>
        <Grid container spacing={2}>
          <Grid item xs={6}>
            <Box display="flex" alignItems="center">
              <Avatar sx={{ width: 32, height: 32, mr: 1 }}>
                {issue.assignee?.charAt(0)}
              </Avatar>
              <Typography><strong>Assignee:</strong> {issue.assignee}</Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box display="flex" alignItems="center">
              <Avatar sx={{ width: 32, height: 32, mr: 1, bgcolor: "secondary.main" }}>
                {issue.reporter?.charAt(0)}
              </Avatar>
              <Typography><strong>Reporter:</strong> {issue.reporter}</Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Typography><strong>Priority:</strong> {issue.priority}</Typography>
          </Grid>
        </Grid>

        <Divider sx={{ my: 2 }} />

        {/* Custom Fields */}
        {issue.customFields?.length > 0 && (
          <>
            <Typography variant="subtitle1" sx={{ fontWeight: "bold", mb: 1 }}>Custom Fields</Typography>
            <Grid container spacing={2}>
              {issue.customFields.map((field, index) => (
                <Grid item xs={6} key={index}>
                  <Typography><strong>{field.name}:</strong> {field.value}</Typography>
                </Grid>
              ))}
            </Grid>
            <Divider sx={{ my: 2 }} />
          </>
        )}

        {/* Comments */}
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>Comments ({issue.comments.length})</Typography>
          </AccordionSummary>
          <AccordionDetails>
            {issue.comments.map((comment, idx) => (
              <Box
                key={idx}
                sx={{
                  padding: 1.5,
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  mb: 1,
                  backgroundColor: "#fff"
                }}
              >
                <Typography variant="body2" color="text.secondary">
                  {comment.author} • {dayjs(comment.date).format("DD MMM YYYY")}
                </Typography>
                <Typography variant="body1">{comment.text}</Typography>
              </Box>
            ))}
            {issue.comments.length === 0 && (
              <Typography variant="body2" color="text.secondary">No comments</Typography>
            )}
          </AccordionDetails>
        </Accordion>
      </CardContent>
    </Card>
  );
};

export default IssueCard;
