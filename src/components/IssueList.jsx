import React from 'react';
import { List, ListItemButton, ListItemText, Paper, Typography } from '@mui/material';

const IssueList = ({ issues, searchTerm, onIssueClick }) => {
  const filtered = issues.filter(issue =>
    issue.key.toLowerCase().includes(searchTerm.toLowerCase()) ||
    issue.summary.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Paper sx={{ p: 2 }}>
      {filtered.length === 0 ? (
        <Typography variant="body1">No issues match your search.</Typography>
      ) : (
        <List>
          {filtered.map((issue, index) => (
            <ListItemButton key={index} onClick={() => onIssueClick(issue)}>
              <ListItemText primary={`${issue.key}: ${issue.summary}`} />
            </ListItemButton>
          ))}
        </List>
      )}
    </Paper>
  );
};

export default IssueList;
