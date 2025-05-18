import React, { useEffect, useState } from 'react';
import api from '../api';

function ProjectList() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.get('/fetch-projects')
      .then(res => setProjects(res.data))
      .catch(err => console.error('Error fetching projects:', err));
  }, []);

  return (
    <div>
      <h2>Projects</h2>
      <ul>
        {projects.map(project => (
          <li key={project.id}>
            <strong>{project.pkey}</strong>: {project.pname}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProjectList;
