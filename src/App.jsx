import React, { useState } from 'react';
import { Box, Button, Typography, TextField, Modal, Card, CardContent, List, ListItemButton, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import mockProjects from './mockProjects';
import IssueList from './components/IssueList';

const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '80%',
  maxWidth: 700,
  bgcolor: 'background.paper',
  borderRadius: '12px',
  boxShadow: 24,
  p: 4,
};

const App = () => {
  const [selectedProject, setSelectedProject] = useState(null);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const handleProjectClick = (project) => {
    setSelectedProject(project);
    setSearchTerm('');
    setSelectedIssue(null);
  };

  const handleIssueClick = (issue) => {
    setSelectedIssue(issue);
  };

  const handleCloseModal = () => {
    setSelectedIssue(null);
  };

  const handleBackToProjects = () => {
    setSelectedProject(null);
    setSearchTerm('');
    setSelectedIssue(null);
  };

  return (
    <Box sx={{ p: 4, fontFamily: 'Arial' }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>Jira Archive Viewer</Typography>

      {!selectedProject ? (
        <Card sx={{ p: 3, maxWidth: 400 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>Select a Project</Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {mockProjects.map((project, idx) => (
              <Button key={idx} variant="outlined" onClick={() => handleProjectClick(project)}>
                {project.name}
              </Button>
            ))}
          </Box>
        </Card>
      ) : (
        <>
          <Button onClick={handleBackToProjects} sx={{ mb: 2 }} variant="outlined">← Back to Projects</Button>
          <Typography variant="h5" sx={{ mb: 2 }}>{selectedProject.name} - Issues</Typography>
          <TextField
            variant="outlined"
            fullWidth
            placeholder="Search by key or summary"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ mb: 3 }}
          />
          <IssueList
            issues={selectedProject.issues}
            searchTerm={searchTerm}
            onIssueClick={handleIssueClick}
          />
        </>
      )}

      <Modal open={Boolean(selectedIssue)} onClose={handleCloseModal}>
        <Box sx={modalStyle}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">{selectedIssue?.key}: {selectedIssue?.summary}</Typography>
            <IconButton onClick={handleCloseModal}><CloseIcon /></IconButton>
          </Box>
          <Box sx={{ mt: 2 }}>
            {Object.entries(selectedIssue?.customFields || {}).map(([field, value], idx) => (
              <Typography key={idx} sx={{ mb: 1 }}><strong>{field}:</strong> {value}</Typography>
            ))}
          </Box>
        </Box>
      </Modal>
    </Box>
  );
};

export default App;
