import React from "react";
import { Button, Stack, Typography } from "@mui/material";

const ProjectList = ({ projects, onProjectSelect }) => {
  return (
    <div>
      <Typography variant="h5" sx={{ mb: 2 }}>Projects</Typography>
      <Stack spacing={1}>
        {projects.map((project) => (
          <Button
            key={project.id}
            variant="outlined"
            onClick={() => onProjectSelect(project.id)}
          >
            {project.name}
          </Button>
        ))}
      </Stack>
    </div>
  );
};

export default ProjectList;
